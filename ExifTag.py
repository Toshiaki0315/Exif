import struct

class ExifTagInfomation:

    def __init__(self):
        pass

    EXIF_TAG_ID = {
        # TIFF
        0x0100:"画像の幅",
        0x0101:"画像の高さ",
        0x0102:"画像のビットの深さ",
        0x0103:"圧縮の種類",
        0x0106:"画素構成",
        0x0112:"画像方向",
        0x0115:"コンポーネント数",
        0x011C:"画像データの並び",
        0x0212:"YCCの面構成(C)",
        0x0213:"YCCの面構成(YC)",
        0x011A:"画像の幅の解像度",
        0x011B:"画像の高さの解像度",
        0x0128:"画像の幅と高さの解像度の単位",
        0x0111:"画像データのロケーション",
        0x0116:"ストリップ中のライン数",
        0x0117:"ストリップのデータ量",
        0x0201:"JPEGのSOIへのオフセット",
        0x0202:"JPEGデータのバイト数",
        0x012D:"再生階調カーブ特性",
        0x013E:"参照白色点の色度座標値",
        0x013F:"減色の色度座標値",
        0x0211:"色変換マトリックス係数",
        0x0214:"参照黒色点値と参照白色点値",
        0x0132:"ファイル更新日時",
        0x010E:"画像タイトル",
        0x010F:"メーカー名",
        0x0110:"モデル名",
        0x0131:"使用ソフトウェア名",
        0x013B:"作者名",
        0x8298:"撮影著作権者",
        #
        0x8769:"Exif IFDのオフセット",
        0x8825:"GPS IFDのオフセット",
        0xA005:"互換性IFDのオフセット",
        0xC4A5:"PIM II/PIM III",
        # EXIF TAG
        0x9000:"Exifバージョン",
        0xA000:"対応FlashPixバージョン",

        0xA001:"色空間情報",
        0xA500:"再生ガンマ",

        0x9101:"各コンポーネントの意味",
        0x9102:"画像圧縮モード",
        0xA002:"実行画像幅",
        0xA003:"実行画像高さ",

        0x927C:"メーカー・ノート",
        0x9286:"ユーザー・コメント",

        0xA004:"関連音声ファイル",

        0x9003:"原画像データの生成日時",
        0x9004:"ディジタル・データの生成日時",
        0x9290:"DateTimeのサブセック",
        0x9291:"DateTimeOriginalのサブセック",
        0x9292:"DateTimeDigitizedのサブセック",

        0xA420:"画像ユニークID",
        0xA430:"カメラ所有者名",
        0xA431:"カメラシリアル番号",
        0xA432:"レンズの仕様情報",
        0xA433:"レンズのメーカー名",
        0xA434:"レンズのモデル名",
        0xA435:"レンズのシリアル番号",

        0x829A:"露出時間",
        0x829D:"Fナンバー",
        0x8822:"露出プログラム",
        0x8824:"スペクトル感度",
        0x8827:"ISOスピード。レート",
        0x8828:"光電変換係数",
        0x8830:"感度種別",
        0x8831:"標準出力感度",
        0x8832:"推奨露光指数",
        0x8833:"ISOスピード",
        0x8834:"ISOスピードラチチュードyyy",
        0x8835:"ISOスピードラチチュードzzz",
        0x9201:"シャッター・スピード",
        0x9202:"絞り値",
        0x9203:"輝度値",
        0x9204:"露出補正値",
        0x9205:"レンズ最小F値",
        0x9206:"被写体距離",
        0x9207:"測光方式",
        0x9208:"光源",
        0x9209:"フラッシュ",
        0x920A:"レンズ焦点距離",
        0x9214:"被写体エリア",
        0xA20B:"フラッシュ強度",
        0xA20C:"空間周波数応答",
        0xA20E:"焦点面の幅の解像度",
        0xA20F:"焦点面の高さの解像度",
        0xA210:"焦点面解像度単位",
        0xA214:"被写体位置",
        0xA215:"露出インデックス",
        0xA217:"センサー方式",
        0xA300:"ファイル・ソース",
        0xA301:"シーン・タイプ",
        0xA302:"CFAパターン",
        0xA401:"スペシャル・エフェクト",
        0xA402:"露光モード",
        0xA403:"ホワイト・バランス",
        0xA404:"デジタル・ズーム比",
        0xA405:"35mm換算焦点距離",
        0xA406:"撮影シーン・タイプ",
        0xA407:"ゲイン・コントロール",
        0xA408:"コントラスト",
        0xA409:"飽和状態",
        0xA40A:"シャープネス",
        0xA40B:"撮影コンディション",
        0xA40C:"被写体撮影モード",
        0x010A:"フィル・オーダー",
        0x010D:"ドキュメント名",
        0x0156:"転送レンジ",
        0x0200:"JPEGProc",
        0x828F:"バッテリ・レベル",
        0x83BB:"IPTC/NAA",
        0x8773:"InterColorProfile",
        # Exif 2.3で未定義のタグ
        0xC6D2:"Panasonic Title(1)",
        0xC6D3:"Panasonic Title(2)"
    }

    GPS_TAG_ID = {
        # GPS TAB
        0x0000:"GPSタグバージョン",
        0x0001:"北緯(N) or 南緯(S)",
        0x0002:"緯度（数値）",
        0x0003:"東経(E) or 西経(W)",
        0x0004:"軽度（数値）",
        0x0005:"高度の基準",
        0x0006:"高度（数値）",
        0x0007:"GPS時間（原子時計の時間）",
        0x0008:"測位に使った衛星信号",
        0x0009:"GPS受信機の状態",
        0x000A:"GPSの測位方法",
        0x000B:"測位の信頼性",
        0x000C:"速度の単位",
        0x000D:"速度（数値）",
        0x000E:"進行方向の単位",
        0x000F:"進行方向（数値）",
        0x0010:"撮影した画像の方向の単位",
        0x0011:"撮影した画像の方向（数値）",
        0x0012:"測位に用いた地図データ",
        0x0013:"目的地の北緯(N) or 南緯(S)",
        0x0014:"目的地の緯度（数値）",
        0x0015:"目的地の東経(E) or 西経(W)",
        0x0016:"目的地の軽度（数値）",
        0x0017:"目的地の方角の単位",
        0x0018:"目的地の方角（数値）",
        0x0019:"目的地までの距離の単位",
        0x001A:"目的地までの距離（数値）",
        0x001B:"測位方式の名称",
        0x001C:"測位地点の名称",
        0x001D:"GPS日付",
        0x001E:"GPS補正測位",
        0x001F:"水平方向測位誤差"
    }

    INTR_TAG_ID = {
        # TAG INTR
        0x0001:"互換性インデックス",
        0x0002:"互換性バージョン",
        0x1000:"関連画像フォーマット",
        0x1001:"関連画像幅",
        0x1002:"関連画像高さ",
    }

    def change_id_to_string(self, ifd, tag_id):
        if ifd == "gps":
            exif_tag_id = self.GPS_TAG_ID
        elif ifd == "intr":
            exif_tag_id = self.INTR_TAG_ID
        else:
            exif_tag_id = self.EXIF_TAG_ID
        
        if tag_id in exif_tag_id:
            return exif_tag_id[tag_id]
        else:
            return "unkown ID"
    
    EXIF_TAG_FORMAT = {
        1:"BYTE",
        2:"ASCII",
        3:"SHORT",
        4:"LONG",
        5:"RATIONAL",
        6:"SBYTE",
        7:"UNDEFINED",
        8:"SSHORT",
        9:"SLONG",
        10:"SRATIONAL",
        11:"SINGLE FLOAT",
        12:"DOUBLE FLOAT",
    }

    def change_format_to_string(self, format):
        
        if format in self.EXIF_TAG_FORMAT:
            return self.EXIF_TAG_FORMAT[format]
        else:
            return "unkown format"


    def int_to_string( self, length, value ):
        return value.to_bytes(length, byteorder='big').decode("ascii").strip('\x00')


    def change_ascii_to_value( self, value_type, length, value, data, offset ):
        if length <= 4:
            value_string = self.int_to_string(length, value)
        else:
            fmt = str(length)+"s"
            value_string = "".join(map(str, struct.unpack_from(fmt, data, offset+value)))
        return value_string


    def change_undefined_to_value( self, value_type, length, value, data, offset ):
        if length <= 4:
            value_string = self.int_to_string(length, value)
        else:
#            fmt = str(length)+"s"
#            value_string = "".join(map(str, struct.unpack_from(fmt, data, offset+value)))
            value_string = ""
        return value_string
        
    def change_value( self, value_type, length, value, data, offset ):
        # valueには4byte以下であれば値、5byte以上であればオフセットが入ってる
        # オフセットはtiffヘッダの先頭からのオフセット
        if self.EXIF_TAG_FORMAT[value_type] == "ASCII":
            value_string = self.change_ascii_to_value( value_type, length, value, data, offset )
        elif self.EXIF_TAG_FORMAT[value_type] == "UNDEFINED":
            value_string = self.change_undefined_to_value( value_type, length, value, data, offset )
        else:
            value_string = str(value)

        return value_string
