# Exif

Pythonのみで実装された、画像ファイル（JPEG等）からExif情報を抽出・解析するためのツールです。外部のライブラリ（ExifToolなど）に依存せず、軽量かつシンプルにメタデータを取得できます。

## 特徴

- **ピュアPython実装**: 外部の依存ツールを必要とせず、標準のPython環境のみで動作します。
- **コマンドライン実行**: ターミナルから対象の画像ファイルを指定するだけで、即座にExif情報をパースして表示できます。
- **構造的な解析**: `ExifParser` や `ExifTag` クラスを用いて、バイナリデータから構造的にタグ情報を読み解きます。

## リポジトリ構成

- `Exif.py` : コマンドラインから実行するためのメインスクリプト（エントリーポイント）。
- `ExifParser.py` : 画像のバイナリデータからIFD（Image File Directory）をパースするコアロジック。
- `ExifTag.py` / `ExifTagData.py` : Exifの各タグ定義や、パースしたデータ値のフォーマットを行うモジュール。
- `ExifParserTest.py` / `ExifTagTest.py` : 解析機能およびタグ機能の動作確認用テストコード。
- `sample/` : 動作検証用のサンプル画像ディレクトリ。

## 前提条件

- Python 3.x

## インストール

リポジトリをクローンするだけで使用可能です。

```bash
git clone [https://github.com/Toshiaki0315/Exif.git](https://github.com/Toshiaki0315/Exif.git)
cd Exif
```

## 使い方

ターミナル（コマンドプロンプト）で `Exif.py` を実行し、引数として解析したい画像ファイルのパスを渡します。

```bash
# 基本的な実行方法
python Exif.py [画像ファイルのパス]

# 実行例（同梱のサンプル画像を使用する場合）
python Exif.py sample/IMG_1406.JPG
```

実行すると、対象画像に含まれるカメラメーカー、撮影日時、露出設定などのExifタグ情報がターミナル上に解析・表示されます。

## テストの実行

開発や改修を行った際は、以下のコマンドで同梱されているユニットテストを実行して動作確認を行えます。

```bash
python -m unittest ExifParserTest.py ExifTagTest.py
```
