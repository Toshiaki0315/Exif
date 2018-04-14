import struct
import math

class ExifTagInformation:

    __ifd         = ""
    __byte_order  = ""
    __base_offset = 0
    __id          = 0
    __type        = 0
    __length      = 0
    __value       = 0
    def __init__(self, ifd, byte_order, base_offset, exif_info):
        self.__ifd         = ifd
        self.__byte_order  = byte_order
        self.__base_offset = base_offset
        self.__id          = exif_info["id"]
        self.__type        = exif_info["type"]
        self.__length      = exif_info["len"]
        self.__value       = exif_info["value"]

    EXIF_TAG_ID = {
        # TIFF
        0x0100:{"mes":"画像の幅"},
        0x0101:{"mes":"画像の高さ"},
        0x0102:{"mes":"画像のビットの深さ"},
        0x0103:{"mes":"圧縮の種類", "value":{0x01:"非圧縮", 0x6:"JPEG 圧縮(サムネイルのみ)"}},
        0x0106:{"mes":"画素構成", "value":{0x02:"RGB", 0x06:"YCbCr"}},
        0x0112:{"mes":"画像方向", "value":{0x01:"visual top    / visual left-hand side",  \
                                          0x02:"visual top    / visual right-hand side", \
                                          0x03:"visual bottom / visual right-hand side", \
                                          0x04:"visual bottom / visual left-hand side",  \
                                          0x05:"visual left-hand side  / visual top",    \
                                          0x06:"visual right-hand side / visual top",    \
                                          0x07:"visual right-hand side / visual bottom", \
                                          0x08:"visual left-hand side  / visual bottom" }},
        0x0115:{"mes":"コンポーネント数"},
        0x011C:{"mes":"画像データの並び", "value":{0x01:"点順次(chunky)フォーマット", 0x02:"面順次(planar)フォーマット"}},
        0x0212:{"mes":"YCCの面構成(C)"},
        0x0213:{"mes":"YCCの面構成(YC)", "value":{0x01:"中心", 0x02:"一致(co-sited)"}},
        0x011A:{"mes":"画像の幅の解像度"},
        0x011B:{"mes":"画像の高さの解像度"},
        0x0128:{"mes":"画像の幅と高さの解像度の単位", "value":{0x01:"単位無し", 0x02:"インチ", 0x03:"センチメートル"}},
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

        0xA001:{"mes":"色空間情報", "value":{0x0001:"sRGB", 0xffff:"Uncalibrated"}},
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
        0x8822:{"mes":"露出プログラム", "value":{0x00:"未定義", \
                                               0x01:"マニュアル", \
                                               0x02:"ノーマルプログラム", \
                                               0x03:"絞り優先", \
                                               0x04:"シャッター優先", \
                                               0x05:"低速プログラム", \
                                               0x06:"高速プログラム", \
                                               0x07:"ポートレートモード", \
                                               0x08:"風景モード"}},
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
        0x9207:{"mes":"測光方式", "value":{0x00:"不明",
                                          0x01:"平均(Average)", \
                                          0x02:"中央重点(Center Weight Average)", \
                                          0x03:"スポット(Spot)", \
                                          0x04:"マルチスポット(Multi Spot)", \
                                          0x05:"分割測光(Pattern)", \
                                          0x06:"部分測光(Partial)", \
                                          0xff:"その他"}},
        0x9208:{"mes":"光源", "value":{0x00:"不明", \
                                       0x01:"昼光", \
                                       0x02:"蛍光灯", \
                                       0x03:"タングステン(Incandescvent light)", \
                                       0x4:"フラッシュ", \
                                       0x09:"晴れ", \
                                       0x0a:"曇り", \
                                       0x0b:"日陰", \
                                       0x0c:"Daylight 蛍光灯(D 5700-7100K)", \
                                       0x0d:"Day White 蛍光灯(N 4600-5400K)", \
                                       0x0e:"Cool White 蛍光灯(W 3900-4500K)", \
                                       0x0f:"White 蛍光灯(WW 3200-3700K)", \
                                       0x11:"標準光 A", \
                                       0x12:"標準光 B", \
                                       0x13:"標準光 C", \
                                       0x14:"D55", \
                                       0x15:"D65", \
                                       0x16:"D75", \
                                       0x17:"D50", \
                                       0x18:"ISOスタジオ・タングステン", \
                                       0xff:"その他"}},
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
        0xA217:{"mes":"センサー方式", "value":{0x01:"未定義", \
                                             0x02:"単版カラーセンサー", \
                                             0x03:"2版カラーセンサー", \
                                             0x04:"3版カラーセンサー", \
                                             0x05:"色順次カラーセンサー", \
                                             0x07:"3線リニアセンサー", \
                                             0x08:"色順次リニアセンサー"}},
        0xA300:{"mes":"ファイル・ソース", "value":{0x03:"デジタルカメラ"}},
        0xA301:{"mes":"シーン・タイプ", "value":{0x01:"直接撮影された画像"}},
        0xA302:{"mes":"CFAパターン"},
        0xA401:{"mes":"スペシャル・エフェクト", "value":{0x00:"ノーマル処理", 0x01:"エフェクトあり"}},
        0xA402:{"mes":"露光モード", "value":{0x00:"自動露光", 0x01:"マニュアル露光", 0x02:"自動ブラケット"}},
        0xA403:{"mes":"ホワイト・バランス", "value":{0x00:"自動ホワイト・バランス", 0x01:"マニュアル・ホワイト・バランス"}},
        0xA404:{"mes":"デジタル・ズーム比"},
        0xA405:{"mes":"35mm換算焦点距離"},
        0xA406:{"mes":"撮影シーン・タイプ", "value":{0x00:"スタンダード", \
                                                  0x01:"ランドスケープ", \
                                                  0x02:"ポートレート", \
                                                  0x03:"夜景"}},
        0xA407:{"mes":"ゲイン・コントロール", "value":{0x00:"コントロール無し", \
                                                    0x01:"低ゲイン・アップ", \
                                                    0x02:"高ゲイン・アップ", \
                                                    0x03:"低ゲイン・ダウン", \
                                                    0x04:"高ゲイン・ダウン"}},
        0xA408:{"mes":"コントラスト", "value":{0x00:"ノーマル", \
                                             0x01:"ソフト", \
                                             0x02:"ハード"}},
        0xA409:{"mes":"飽和状態", "value":{0x00:"ノーマル",
                                          0x01:"低飽和", \
                                          0x02:"高飽和"}},
        0xA40A:{"mes":"シャープネス", "value":{0x00:"ノーマル", \
                                             0x01:"ソフト", \
                                             0x02:"ハード"}},
        0xA40B:{"mes":"撮影コンディション"},
        0xA40C:{"mes":"被写体撮影モード", "value":{0x00:"不明", \
                                                 0x01:"マクロ", \
                                                 0x02:"近景", \
                                                 0x03:"遠景"}},
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

    TAG_LIST = {
        "0th":EXIF_TAG_ID,
        "1st":EXIF_TAG_ID,
        "exif":EXIF_TAG_ID,
        "gps":GPS_TAG_ID,
        "intr":INTR_TAG_ID,
    }
    
    def change_id_to_string(self):

        if self.__ifd not in self.TAG_LIST:
            return "Unkown IFD"
        
        if self.__id in self.TAG_LIST[self.__ifd]:
            return self.TAG_LIST[self.__ifd][self.__id]["mes"]

        return "Unkown ID"
            

    def change_value_to_string(self):
        if self.__ifd not in self.TAG_LIST:
            return "Unkown IFD"

        if self.__id not in self.TAG_LIST[self.__ifd]:
            return "Unkown ID"

        if "value" not in self.TAG_LIST[self.__ifd][self.__id]:
            return str(self.__value)

        if self.__value in self.TAG_LIST[self.__ifd][self.__id]["value"]:
            return self.TAG_LIST[self.__ifd][self.__id]["value"][self.__value]

        return "Unkown value"
        

    def is_offset(self):
        if self.__length <= 4:
            return False
        return True
    
    def change_format_to_string(self):
        exif_tag_format_lists = {
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
        
        if self.__type in exif_tag_format_lists:
            return exif_tag_format_lists[self.__type]
        return "Unkown Format"


    def change_int_to_string(self):
        byte_oders = {"<":'little', ">":'big'}
        return self.__value.to_bytes(self.__length, byteorder=byte_oders[self.__byte_order]).decode("ascii").strip('\x00')


    def change_ascii_to_value(self, jpeg_data):
        if self.is_offset():
            start_number = self.__base_offset + self.__value
            end_number   = start_number + self.__length
            return jpeg_data.decode(encoding='ascii', errors='replace')[start_number:end_number].strip('\x00')
        return self.change_int_to_string()

    def change_undefined_components_conf(self):
        value_chars = {0:"", 1:"Y", 2:"Cb", 3:"Cr", 4:"R", 5:"G", 6:"B"}
        value_string =""
        for shift_length in {0, 8, 16, 24}:
            value_string += value_chars[(self.__value >> shift_length)&0x000000ff]
        return value_string

    def change_value_to_makernote(self, jpeg_data):
        return "省略"

    def value_to_pim_header( self, jpeg_data ):
        value = struct.unpack_from(self.__byte_order+"8s", jpeg_data, self.__base_offset + self.__value)[0]
        return value.decode(encoding='ascii', errors='replace').strip('\x00')
    
    def value_to_pim_version( self, jpeg_data ):
        byte_oders = {"<":'little', ">":'big'}
        value = struct.unpack_from(self.__byte_order+"1L", jpeg_data, self.__base_offset + self.__value + 8)[0]
        return value.to_bytes(4, byteorder=byte_oders[self.__byte_order]).decode("ascii").strip('\x00')

    def value_to_pim_entry_count( self, jpeg_data ):
        return struct.unpack_from(self.__byte_order+"1h", jpeg_data, self.__base_offset + self.__value + 14)[0]

    def value_to_pim_entry_id( self, jpeg_data, count ):
        return struct.unpack_from(self.__byte_order+"1H1L", jpeg_data, self.__base_offset + self.__value + 16 + count * 6)[0]
    
    def value_to_pim_entry_value( self, jpeg_data, count ):
        return struct.unpack_from(self.__byte_order+"1H1L", jpeg_data, self.__base_offset + self.__value + 16 + count * 6)[1]

    def change_value_to_pim(self, jpeg_data):
        pim_header = self.value_to_pim_header(jpeg_data)
        pim_version = self.value_to_pim_version(jpeg_data)
        pim_entry_count = self.value_to_pim_entry_count(jpeg_data)
        pim_string = "{:s} : {:4s} : length = {:d}\n\t--- PrintIM Data ---".format(pim_header, pim_version, pim_entry_count)
        for i in range(pim_entry_count):
            pim_string = pim_string + "\n\t  {:04x} : {:08x}".format(self.value_to_pim_entry_id(jpeg_data, i), self.value_to_pim_entry_value(jpeg_data, i))
        return pim_string
    
    
    def undefined_data_to_string(self, jpeg_data):
        value_list = struct.unpack_from(self.__byte_order+str(self.__length)+"B",
                                    jpeg_data,
                                    self.__base_offset + self.__value)
        value_string = "\n\t"
        for i in range(len(value_list)):
            value_string = value_string + "0x{:02x}, ".format(value_list[i])
            if ((i+1) % 10) is 0:
                value_string = value_string + "\n\t"
        return value_string
        
    def change_undefined_to_value(self, jpeg_data):
        change_undefined_lists = {
            0xa300:self.change_value_to_string,           # ファイル・ソース
            0x927c:self.change_value_to_makernote,        # Makernote
            0xc4a5:self.change_value_to_pim,              # PIM II/PIM III
            0x9101:self.change_undefined_components_conf, # Components Conf
        }
        
        if self.__id in change_undefined_lists:
            if self.is_offset():
                return change_undefined_lists[self.__id](jpeg_data)
            else:
                return change_undefined_lists[self.__id]()
            
        if self.is_offset():
            return self.undefined_data_to_string(jpeg_data)

        return self.change_int_to_string()


    def change_short_to_value(self, jpeg_data):
        if self.is_offset():
            return str(self.__value)

        return self.change_value_to_string()

    def change_rational_to_f_number(self, values):
        return "F{:.1f}".format(values[0]/values[1])

    def change_rational_to_exposure_time(self, values):
        return "{:f}sec".format(values[0]/values[1])

    def change_rational_to_exposure_bias(self, values):
        if values[1] == 0:
            return "0.0"
        
        exposure_bias = values[0]/values[1]
        if exposure_bias > 0.0:
            return "+{:.1f}".format(exposure_bias)

        return "{:.1f}".format(exposure_bias)

    def change_rational_to_focal_len(self, values):
        return "{:.0f}mm".format(values[0]/values[1])
        
    def change_rational_to_distance(self, values):
        return "{:.1f}m".format(values[0]/values[1])
    
    def change_rational_to_aperture(self, values):
        div = math.exp((values[0]/values[1])*math.log(2.0)/2)
        value = math.pow(math.sqrt(2.0), values[0]/values[1])
        return "F{:.1f} (F{:f})".format(value, div)

    def change_rational_to_string(self, values):
        # RATIONALの場合は、1つめに分子、2つめに分母が入っているので、lengthを2倍にして値を取得している
        if values[0] == 0 and values[1] == 0:
            return "{:d}.{:d}".format(values[0], values[1])
        
        if values[1] == 1:
            return "{:d}".format(values[0])
        
        return "{:d} / {:d}".format(values[0], values[1])

    def change_rational_to_shutter_speed(self, values):
        div = math.exp((values[0]/values[1])*math.log(2.0)/-1)
        value = math.pow(2.0, values[0]/values[1])
        return "1/{:.0f} ({:f}sec)".format(value, div)
        
        
    def change_rational_to_brightness(self, values):
        div = math.exp((values[0]/values[1])*math.log(2.0))
        return "{:f}(B/NK)".format(div)
        
    def change_srational_to_string(self, values):
        if values[0] == 0 and values[1] == 0:
            return "{:d}.{:d}".format(values[0], values[1])
        
        if values[1] == 1:
            return "{:d}".format(values[0])
        
        return "{:f}".format(values[0]/values[1])


    def change_rational_to_value(self, jpeg_data):
        change_rational_lists = {
            0x829a:self.change_rational_to_exposure_time, # Exposure Time
            0x829d:self.change_rational_to_f_number,         # F Number
            0x920a:self.change_rational_to_focal_len,        # Focal Len
            0x9206:self.change_rational_to_distance,         # Distance
            0x9205:self.change_rational_to_aperture,         # Max Aperture
            0x9202:self.change_rational_to_aperture,         # Aperture            
        }
        # RATIONALの場合は、1つめに分子、2つめに分母が入っているので、lengthを2倍にして値を取得している
        values = struct.unpack_from(self.__byte_order+str(self.__length*2)+"L", \
                                    jpeg_data, \
                                    self.__base_offset + self.__value)

        if self.__id in change_rational_lists:
            return change_rational_lists[self.__id](values)
            
        return self.change_rational_to_string(values)

    def change_srational_to_value(self, jpeg_data):
        change_srational_lists = {
            0x9204:self.change_rational_to_exposure_bias,         # Exposure Bias
            0x9201:self.change_rational_to_shutter_speed,         # Shutter Speed
            0x9203:self.change_rational_to_brightness,            # Brightness
        }
        # RATIONALの場合は、1つめに分子、2つめに分母が入っているので、lengthを2倍にして値を取得している
        values = struct.unpack_from(self.__byte_order+str(self.__length*2)+"l", \
                                    jpeg_data, \
                                    self.__base_offset + self.__value)

        if self.__id in change_srational_lists:
            return change_srational_lists[self.__id](values)

        return self.change_srational_to_string(values)

    def change_value(self, jpeg_data):
        change_value_lists = {
            # 1:byte
            2:self.change_ascii_to_value,
            3:self.change_short_to_value,
            # 4:long
            5:self.change_rational_to_value,
            # 6:sbyte
            7:self.change_undefined_to_value,
            # 8:sshort
            # 9:slong
            10:self.change_srational_to_value,
            # 11: single float
            # 12: double float
        }
        if self.__type in change_value_lists:
            return change_value_lists[self.__type](jpeg_data)

        return str(self.__value)

    def exif_tag_length(self):
        return self.__length

    def exif_tag_value(self):
        return self.__value

