import struct

class ExifTagInfomation:

    def __init__(self):
        pass

    EXIF_TAG_ID = {
        # TIFF
        0x0100:{"mes":"画像の幅"},
        0x0101:{"mes":"画像の高さ"},
        0x0102:{"mes":"画像のビットの深さ"},
        0x0103:{"mes":"圧縮の種類"},
        0x0106:{"mes":"画素構成"},
        0x0112:{"mes":"画像方向"},
        0x0115:{"mes":"コンポーネント数"},
        0x011C:{"mes":"画像データの並び"},
        0x0212:{"mes":"YCCの面構成(C)"},
        0x0213:{"mes":"YCCの面構成(YC)"},
        0x011A:{"mes":"画像の幅の解像度"},
        0x011B:{"mes":"画像の高さの解像度"},
        0x0128:{"mes":"画像の幅と高さの解像度の単位"},
        0x0111:{"mes":"画像データのロケーション"},
        0x0116:{"mes":"ストリップ中のライン数"},
        0x0117:{"mes":"ストリップのデータ量"},
        0x0201:{"mes":"JPEGのSOIへのオフセット"},
        0x0202:{"mes":"JPEGデータのバイト数"},
        0x012D:{"mes":"再生階調カーブ特性"},
        0x013E:{"mes":"参照白色点の色度座標値"},
        0x013F:{"mes":"減色の色度座標値"},
        0x0211:{"mes":"色変換マトリックス係数"},
        0x0214:{"mes":"参照黒色点値と参照白色点値"},
        0x0132:{"mes":"ファイル更新日時"},
        0x010E:{"mes":"画像タイトル"},
        0x010F:{"mes":"メーカー名"},
        0x0110:{"mes":"モデル名"},
        0x0131:{"mes":"使用ソフトウェア名"},
        0x013B:{"mes":"作者名"},
        0x8298:{"mes":"撮影著作権者"},
        #
        0x8769:{"mes":"Exif IFDのオフセット"},
        0x8825:{"mes":"GPS IFDのオフセット"},
        0xA005:{"mes":"互換性IFDのオフセット"},
        0xC4A5:{"mes":"PIM II/PIM III"},
        # EXIF TAG
        0x9000:{"mes":"Exifバージョン"},
        0xA000:{"mes":"対応FlashPixバージョン"},

        0xA001:{"mes":"色空間情報"},
        0xA500:{"mes":"再生ガンマ"},

        0x9101:{"mes":"各コンポーネントの意味"},
        0x9102:{"mes":"画像圧縮モード"},
        0xA002:{"mes":"実行画像幅"},
        0xA003:{"mes":"実行画像高さ"},

        0x927C:{"mes":"メーカー・ノート"},
        0x9286:{"mes":"ユーザー・コメント"},

        0xA004:{"mes":"関連音声ファイル"},

        0x9003:{"mes":"原画像データの生成日時"},
        0x9004:{"mes":"ディジタル・データの生成日時"},
        0x9290:{"mes":"DateTimeのサブセック"},
        0x9291:{"mes":"DateTimeOriginalのサブセック"},
        0x9292:{"mes":"DateTimeDigitizedのサブセック"},

        0xA420:{"mes":"画像ユニークID"},
        0xA430:{"mes":"カメラ所有者名"},
        0xA431:{"mes":"カメラシリアル番号"},
        0xA432:{"mes":"レンズの仕様情報"},
        0xA433:{"mes":"レンズのメーカー名"},
        0xA434:{"mes":"レンズのモデル名"},
        0xA435:{"mes":"レンズのシリアル番号"},

        0x829A:{"mes":"露出時間"},
        0x829D:{"mes":"Fナンバー"},
        0x8822:{"mes":"露出プログラム"},
        0x8824:{"mes":"スペクトル感度"},
        0x8827:{"mes":"ISOスピード。レート"},
        0x8828:{"mes":"光電変換係数"},
        0x8830:{"mes":"感度種別"},
        0x8831:{"mes":"標準出力感度"},
        0x8832:{"mes":"推奨露光指数"},
        0x8833:{"mes":"ISOスピード"},
        0x8834:{"mes":"ISOスピードラチチュードyyy"},
        0x8835:{"mes":"ISOスピードラチチュードzzz"},
        0x9201:{"mes":"シャッター・スピード"},
        0x9202:{"mes":"絞り値"},
        0x9203:{"mes":"輝度値"},
        0x9204:{"mes":"露出補正値"},
        0x9205:{"mes":"レンズ最小F値"},
        0x9206:{"mes":"被写体距離"},
        0x9207:{"mes":"測光方式"},
        0x9208:{"mes":"光源"},
        0x9209:{"mes":"フラッシュ"},
        0x920A:{"mes":"レンズ焦点距離"},
        0x9214:{"mes":"被写体エリア"},
        0xA20B:{"mes":"フラッシュ強度"},
        0xA20C:{"mes":"空間周波数応答"},
        0xA20E:{"mes":"焦点面の幅の解像度"},
        0xA20F:{"mes":"焦点面の高さの解像度"},
        0xA210:{"mes":"焦点面解像度単位"},
        0xA214:{"mes":"被写体位置"},
        0xA215:{"mes":"露出インデックス"},
        0xA217:{"mes":"センサー方式"},
        0xA300:{"mes":"ファイル・ソース"},
        0xA301:{"mes":"シーン・タイプ"},
        0xA302:{"mes":"CFAパターン"},
        0xA401:{"mes":"スペシャル・エフェクト"},
        0xA402:{"mes":"露光モード"},
        0xA403:{"mes":"ホワイト・バランス"},
        0xA404:{"mes":"デジタル・ズーム比"},
        0xA405:{"mes":"35mm換算焦点距離"},
        0xA406:{"mes":"撮影シーン・タイプ"},
        0xA407:{"mes":"ゲイン・コントロール"},
        0xA408:{"mes":"コントラスト"},
        0xA409:{"mes":"飽和状態"},
        0xA40A:{"mes":"シャープネス"},
        0xA40B:{"mes":"撮影コンディション"},
        0xA40C:{"mes":"被写体撮影モード"},
        0x010A:{"mes":"フィル・オーダー"},
        0x010D:{"mes":"ドキュメント名"},
        0x0156:{"mes":"転送レンジ"},
        0x0200:{"mes":"JPEGProc"},
        0x828F:{"mes":"バッテリ・レベル"},
        0x83BB:{"mes":"IPTC/NAA"},
        0x8773:{"mes":"InterColorProfile"},
        # Exif 2.3で未定義のタグ
        0xC6D2:{"mes":"Panasonic Title(1)"},
        0xC6D3:{"mes":"Panasonic Title(2)"},
    }

    GPS_TAG_ID = {
        # GPS TAB
        0x0000:{"mes":"GPSタグバージョン"},
        0x0001:{"mes":"北緯(N) or 南緯(S)"},
        0x0002:{"mes":"緯度（数値）"},
        0x0003:{"mes":"東経(E) or 西経(W)"},
        0x0004:{"mes":"軽度（数値）"},
        0x0005:{"mes":"高度の基準"},
        0x0006:{"mes":"高度（数値）"},
        0x0007:{"mes":"GPS時間（原子時計の時間）"},
        0x0008:{"mes":"測位に使った衛星信号"},
        0x0009:{"mes":"GPS受信機の状態"},
        0x000A:{"mes":"GPSの測位方法"},
        0x000B:{"mes":"測位の信頼性"},
        0x000C:{"mes":"速度の単位"},
        0x000D:{"mes":"速度（数値）"},
        0x000E:{"mes":"進行方向の単位"},
        0x000F:{"mes":"進行方向（数値）"},
        0x0010:{"mes":"撮影した画像の方向の単位"},
        0x0011:{"mes":"撮影した画像の方向（数値）"},
        0x0012:{"mes":"測位に用いた地図データ"},
        0x0013:{"mes":"目的地の北緯(N) or 南緯(S)"},
        0x0014:{"mes":"目的地の緯度（数値）"},
        0x0015:{"mes":"目的地の東経(E) or 西経(W)"},
        0x0016:{"mes":"目的地の軽度（数値）"},
        0x0017:{"mes":"目的地の方角の単位"},
        0x0018:{"mes":"目的地の方角（数値）"},
        0x0019:{"mes":"目的地までの距離の単位"},
        0x001A:{"mes":"目的地までの距離（数値）"},
        0x001B:{"mes":"測位方式の名称"},
        0x001C:{"mes":"測位地点の名称"},
        0x001D:{"mes":"GPS日付"},
        0x001E:{"mes":"GPS補正測位"},
        0x001F:{"mes":"水平方向測位誤差"},
    }

    INTR_TAG_ID = {
        # TAG INTR
        0x0001:{"mes":"互換性インデックス"},
        0x0002:{"mes":"互換性バージョン"},
        0x1000:{"mes":"関連画像フォーマット"},
        0x1001:{"mes":"関連画像幅"},
        0x1002:{"mes":"関連画像高さ"},
    }

    def change_id_to_string(self, ifd, tag_id):
        tag_lists = {"0th":self.EXIF_TAG_ID, "1st":self.EXIF_TAG_ID, "gps":self.GPS_TAG_ID, "intr":self.INTR_TAG_ID, }

        if ifd in tag_lists:
            exif_tag_id = tag_lists[ifd]
            if tag_id in exif_tag_id:
                return exif_tag_id[tag_id]["mes"]
            else:
                return "unkown ID"
        else:
            return "unkown IFD"
    
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
