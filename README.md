# テキスト生成ツール text-builder

*The documents in this repository are written in Japanese. If you need other languages, please write to the issue.*

## なにこれ

CSVファイルとjinja2テンプレートファイルを混ぜ合わせてテキストファイルを生成するためのツールです。

インフラエンジニア向けにコンフィグファイルを作成することを目的として書きました。

This is utils that builds templated text files using from a CSV file and a jinja2 template file.

I wrote for infrastructure engineer to make configuration files.

## 使い方

releasesからパッケージをダウンロードして展開し、コマンドプロンプトやターミナルから以下のように実行してください。

```shell
$ text-builder <テンプレートファイル> <CSVファイル>
```

CSVの1行につき1ファイル出力します。テンプレートエンジンの変数は、CSVのカラム名が参照されます。

text-builderは様々なオプションを用意しています。詳しくはヘルプ( `-h` オプション)で確認してください。

## CSVファイルの独自仕様について

一般的なCSVファイルを読み込むことができますが、ヘッダー行にいくつかの独自仕様を作っています。

### `output_dir` と `filename` カラム

このカラムを指定することで、出力先のディレクトリとファイル名を個別に指定することができます。

`output_dir` カラムの指定がない場合は `output` ディレクトリに出力されます。

`filename` カラムの指定がない場合は `parsed_[0からの連番].txt` に出力されます。

### list、dict表記

当ツールはCSV1行につき1ファイルが出力される仕様のため、カラム名でlistとdictを表現できるようにしてあります。

| filename    | hoge[0] | hoge[1] | fuga.foo | fuga.bar |
| ----------- | ------- | ------- | -------- | -------- |
| example.txt | aaaa    | bbbb    | cccc     | dddd     |

上記のようなCSVの場合、以下のように展開されます。

```yaml
filename: "example.txt"
hoge: 
  - aaaa
  - bbbb
fuga: 
  foo: cccc
  bar: dddd
```

- list表記
  キーとなる文字列の末尾に `[数値または@]` と入力します。
  数値を省略すると、リストの末尾に要素を追加します。
  @を指定すると、現在のリストの最後の要素となります。
- dict表記
  子要素となるキーをピリオドで数珠つなぎにすることでそのキーをdict形式にすることができます。

## 開発者向け

そんな大したコード書いてるわけではないので、簡単に

### ソースコードからの実行

多分jinja2入れればいけます。

### Windowsでexe化するときの注意

備忘。

[pythonスクリプトをexeに変換する（つまづきポイントまとめ） - Qiita](https://qiita.com/pocket_kyoto/items/80a1ac0e46819d90737f)

### ライセンス

無駄にAGPL3.0