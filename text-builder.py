#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from argparse import ArgumentParser
from collections import OrderedDict

import jinja2
import csv
import sys
import os.path
import re

def store_keyval(src_dict, key, val):
    if key is None:
        return val
    if type(src_dict) is not OrderedDict:
        src_dict = OrderedDict()

    matched = re.match(r'^([^\.\[\]]+?)(?:\[([\d]+|@?)\])?(?:\.(.+))?$', key)
    if matched is None:
        print(f'Invalid key name: {key}')
        return src_dict

    key_name = matched.group(1)
    key_index_str = matched.group(2)
    key_dict = matched.group(3)

    is_array = key_index_str is not None
    is_dict = key_dict is not None
    key_exists = key_name in src_dict.keys()

    if is_array and not key_exists:
        src_dict[key_name] = [None]
    elif is_dict and not key_exists:
        src_dict[key_name] = OrderedDict()

    if is_array:
        if key_index_str == '@':
            key_index = len(src_dict[key_name]) - 1
        elif not key_index_str and src_dict[key_name][0] is None:
            key_index = 0
        elif not key_index_str:
            key_index = len(src_dict[key_name])
        else:
            key_index = int(key_index_str)

        key_len = len(src_dict[key_name])
        if key_len < key_index + 1:
            src_dict[key_name].extend([None] * (key_index - key_len + 1))
        src_dict[key_name][key_index] = store_keyval(src_dict[key_name][key_index], key_dict, val)
    elif is_dict:
        src_dict[key_name] = store_keyval(src_dict[key_name], key_dict, val)
    else:
        src_dict[key_name] = val

    return src_dict

def build_templates(args):
    if args.DEBUG:
        print('* === text-builder execute. ===')

    templateLoader = jinja2.FileSystemLoader(searchpath='.', encoding=args.ENCODING)
    templateEnv = jinja2.Environment( loader=templateLoader )
    templateEnv.trim_blocks = True

    newline = args.NEWLINE.replace(r'\r', "\r").replace(r'\n', "\n")

    if args.DEBUG:
        sys.stdout.write('* Loading INVENTORY file ... ')

    f = open(args.INVENTORY, 'rt', encoding=args.ENCODING, newline=newline)

    if args.DEBUG:
        print('Done.')

    try:
        if args.DEBUG:
            print('* Loading header.')

        reader = list(csv.reader(f))

        header = reader.pop(0)
        header_cols = len(header)

        parsed_files = 0
        for row in reader:

            if args.DEBUG:
                sys.stdout.write(f'* Building row({parsed_files + 2}): ')

            dict_row = OrderedDict()
            cols = len(row)

            for i in range(cols if cols > header_cols else header_cols):
                if header_cols <= i:
                    continue
                elif cols <= i:
                    col = ""
                else:
                    col = row[i]

                dict_row = store_keyval(dict_row, header[i], col)

            if args.DEBUG:
                print(dict_row)

            template = templateEnv.get_template(args.TEMPLATE)
            outputText = template.render(dict_row)

            output_dir = args.OUTPUTS_DIR
            if 'output_dir' in dict_row and dict_row['output_dir'].strip() != '':
                output_dir = f"{output_dir}/{dict_row['output_dir'].strip()}"

            os.makedirs(output_dir, exist_ok=True)

            filename = dict_row['filename'] if 'filename' in dict_row else f"parsed_{parsed_files}.txt"

            output_filename = f"{output_dir}/{filename}"
            with open(output_filename, 'w', newline=newline, encoding=args.ENCODING) as output_file:
                output_file.write(outputText)
            print("wrote file: %s" % output_filename)
            parsed_files += 1

        print(f"\nDone. output {parsed_files} files in \"{output_dir}\" directory.")

    finally:
        f.close()

def cmd_options():
    usage = f"text-builder <TEMPLATE> <INVENTORY> [-ehno]"
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument(
        'TEMPLATE',
        type=str,
        help='Template text file.')
    argparser.add_argument(
        'INVENTORY',
        type=str,
        help='Paramaters CSV file.')
    argparser.add_argument(
        '-d', '--debug',
        dest='DEBUG',
        action='store_true',
        help='Output debug message.')
    argparser.add_argument(
        '-e', '--encoding',
        type=str,
        dest='ENCODING',
        default='cp932',
        help='Set encoding charset of template and inventory file. (default: "cp932")')
    argparser.add_argument(
        '-n', '--new-line',
        type=str,
        dest='NEWLINE',
        default="\r\n",
        help='Set new line charcode. (default: "\\r\\n")')
    argparser.add_argument(
        '-o', '--output-path',
        type=str,
        default='output',
        dest='OUTPUTS_DIR',
        help='Set output files path.')
    args = argparser.parse_args()
    return args

if __name__ == "__main__":
    args = cmd_options()
    build_templates(args)
