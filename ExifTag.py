import struct
import math
import ExifTagData as etd

class ExifTagInformation:

    __ifd         = ""
    __byte_order  = ""
    __base_offset = 0
    __id          = 0
    __type        = 0
    __length      = 0
    __value       = 0
    def __init__(self, ifd:str, byte_order:str, base_offset:int, exif_info:dict):
        self.__ifd         = ifd
        self.__byte_order  = byte_order
        self.__base_offset = base_offset
        self.__id          = exif_info["id"]
        self.__type        = exif_info["type"]
        self.__length      = exif_info["len"]
        self.__value       = exif_info["value"]

    TAG_LIST = {
        "0th":etd.EXIF_TAG_ID,
        "1st":etd.EXIF_TAG_ID,
        "exif":etd.EXIF_TAG_ID,
        "gps":etd.GPS_TAG_ID,
        "intr":etd.INTR_TAG_ID,
    }
    

    def __check_ifd_and_id(self)->[bool,str]:
        """IFDとIDの存在チェック"""

        if self.__ifd not in self.TAG_LIST:
            return False, "Unkown IFD"
        
        if self.__id not in self.TAG_LIST[self.__ifd]:
            return False, "Unkown ID"
        
        return True, ""
    

    def change_id_to_string(self)->str:
        """IDを文字列に変換する"""

        check_result = self.__check_ifd_and_id()
        if check_result[0] is False:
            return check_result[1]

        return self.TAG_LIST[self.__ifd][self.__id]["mes"]


    def change_value_to_string(self)->str:
        """値を文字列に変換する"""

        check_result = self.__check_ifd_and_id()
        if check_result[0] is False:
            return check_result[1]

        if "value" not in self.TAG_LIST[self.__ifd][self.__id]:
            return str(self.__value)

        if self.__value in self.TAG_LIST[self.__ifd][self.__id]["value"]:
            return self.TAG_LIST[self.__ifd][self.__id]["value"][self.__value]

        return "Unkown value"
        

    def is_offset(self)->bool:
        """値がオフセットかどうかチェックする"""

        if self.__length <= 4:
            return False
        return True
    

    def change_format_to_string(self)->str:
        """フォーマットタイプを文字列に変換する"""

        exif_tag_formats = {
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
        
        if self.__type in exif_tag_formats:
            return exif_tag_formats[self.__type]
        return "Unkown Format"


    def change_int_to_string(self)->str:
        """数字を文字列に変換する"""

        byte_oders = {"<":'little', ">":'big'}
        return self.__value.to_bytes(self.__length,
                                     byteorder=byte_oders[self.__byte_order]).decode("ascii").strip('\x00')


    def change_ascii_to_value(self, jpeg_data:bytes)->str:
        """ASCIIの値を文字列に変換する"""

        if self.is_offset():
            start_number = self.__base_offset + self.__value
            end_number   = start_number + self.__length
            return jpeg_data.decode(encoding='ascii', errors='replace')[start_number:end_number].strip('\x00')

        return self.change_int_to_string()


    def change_undefined_components_conf(self)->str:
        """RATIONALの値を各コンポーネントの意味に変換"""

        value_chars = {0:"", 1:"Y", 2:"Cb", 3:"Cr", 4:"R", 5:"G", 6:"B"}
        value_string =""
        for shift_length in {0, 8, 16, 24}:
            value_string += value_chars[(self.__value >> shift_length)&0x000000ff]
        
        return value_string


    def change_value_to_makernote(self, jpeg_data:bytes)->str:
        """メーカーノートを返す（予定）"""

        return "省略"


    def _value_to_pim_header(self, jpeg_data:bytes)->str:
        """PIMの文字列を返す"""

        value = struct.unpack_from(self.__byte_order+"8s", jpeg_data, self.__base_offset + self.__value)[0]
        return value.decode(encoding='ascii', errors='replace').strip('\x00')
    

    def _value_to_pim_version(self, jpeg_data:bytes)->str:
        """PIMのバージョンを返す"""

        byte_oders = {"<":'little', ">":'big'}
        value = struct.unpack_from(self.__byte_order+"1L",
                                    jpeg_data,
                                    self.__base_offset + self.__value + 8)[0]
        return value.to_bytes(4, byteorder=byte_oders[self.__byte_order]).decode("ascii").strip('\x00')


    def _value_to_pim_entry_count(self, jpeg_data:bytes)->int:
        """PIMのデータの数を返す"""

        return struct.unpack_from(self.__byte_order+"1h",
                                    jpeg_data,
                                    self.__base_offset + self.__value + 14)[0]


    def _value_to_pim_entry_id(self, jpeg_data:bytes, count:int)->int:
        """指定されたPIMのIDを返す"""

        return struct.unpack_from(self.__byte_order+"1H1L",
                                    jpeg_data,
                                    self.__base_offset + self.__value + 16 + count * 6)[0]
    

    def _value_to_pim_entry_value(self, jpeg_data:bytes, count:int)->int:
        """指定されたPIMの設定値を返す"""

        return struct.unpack_from(self.__byte_order+"1H1L",
                                    jpeg_data,
                                    self.__base_offset + self.__value + 16 + count * 6)[1]


    def change_value_to_pim(self, jpeg_data:bytes)->str:
        """PIMのデータを文字列に変換する"""

        pim_entry_count = self._value_to_pim_entry_count(jpeg_data)
        pim_string = "{:s} : {:4s} : length = {:d}\n\t--- PrintIM Data ---".format(self._value_to_pim_header(jpeg_data),
                                                                                    self._value_to_pim_version(jpeg_data),
                                                                                    pim_entry_count)

        for i in range(pim_entry_count):
            pim_string = pim_string + "\n\t  {:04x} : {:08x}".format(self._value_to_pim_entry_id(jpeg_data, i),
                                                                        self._value_to_pim_entry_value(jpeg_data, i))
        return pim_string
    
    
    def _undefined_data_to_string(self, jpeg_data:bytes)->str:
        """UNDEFINEDの値（不明）を文字列に変換する"""

        value_list = struct.unpack_from(self.__byte_order+str(self.__length)+"B",
                                    jpeg_data,
                                    self.__base_offset + self.__value)
        
        value_string = "\n\t"
        for count, value in enumerate(value_list):
            value_string = value_string + "0x{:02x}, ".format(value)
            if ((count+1) % 10) is 0:
                value_string = value_string + "\n\t"

        return value_string


    def change_undefined_to_value(self, jpeg_data:bytes)->str:
        """UNDEFINEDの値を文字列に変換する"""

        change_undefined_functions= {
            0xa300:self.change_value_to_string,           # ファイル・ソース
            0x927c:self.change_value_to_makernote,        # Makernote
            0xc4a5:self.change_value_to_pim,              # PIM II/PIM III
            0x9101:self.change_undefined_components_conf, # Components Conf
        }
        
        if self.__id in change_undefined_functions:
            if self.is_offset():
                return change_undefined_functions[self.__id](jpeg_data)
            return change_undefined_functions[self.__id]()
            
        if self.is_offset():
            return self._undefined_data_to_string(jpeg_data)

        return self.change_int_to_string()


    def change_short_to_value(self, jpeg_data:bytes)->str:
        """SHORTの値を文字列に変換する"""

        if self.is_offset():
            return str(self.__value)

        return self.change_value_to_string()


    def change_rational_to_f_number(self, values:tuple)->str:
        """RATIONALの値をF値に変換する"""

        return "F{:.1f}".format(values[0]/values[1])


    def change_rational_to_exposure_time(self, values:tuple)->str:
        """RATIONALの値を露出時間に変換する"""

        return "{:f}sec".format(values[0]/values[1])


    def change_rational_to_exposure_bias(self, values:tuple)->str:
        """RATIONALの値を露出バイアスに変換する"""
        
        if values[1] == 0:
            return "0.0"
        
        exposure_bias = values[0]/values[1]
        if exposure_bias > 0.0:
            return "+{:.1f}".format(exposure_bias)

        return "{:.1f}".format(exposure_bias)


    def change_rational_to_focal_len(self, values:tuple)->str:
        """RATIONALの値を焦点距離に変換する"""

        return "{:.0f}mm".format(values[0]/values[1])


    def change_rational_to_distance(self, values:tuple)->str:
        """RATIONALの値を距離に変換する"""

        return "{:.1f}m".format(values[0]/values[1])


    def change_rational_to_aperture(self, values:tuple)->str:
        """RATIONALの値を絞り値に変換する"""

        div = math.exp((values[0]/values[1])*math.log(2.0)/2)
        value = math.pow(math.sqrt(2.0), values[0]/values[1])
        return "F{:.1f} (F{:f})".format(value, div)


    def change_rational_to_string(self, values:tuple)->str:
        """RATIONALの値を文字列に変換する"""

        # RATIONALの場合は、1つめに分子、2つめに分母が入っているので、lengthを2倍にして値を取得している
        if values[0] == 0 and values[1] == 0:
            return "{:d}.{:d}".format(values[0], values[1])
        
        if values[1] == 1:
            return "{:d}".format(values[0])
        
        return "{:d} / {:d}".format(values[0], values[1])


    def change_rational_to_shutter_speed(self, values:tuple)->str:
        """SRATIONALの値をシャッター・スピードに変換する"""

        div = math.exp((values[0]/values[1])*math.log(2.0)/-1)
        value = math.pow(2.0, values[0]/values[1])
        return "1/{:.0f} ({:f}sec)".format(value, div)
        
        
    def change_rational_to_brightness(self, values:tuple)->str:
        """SRATIONALの値を、輝度に変換する"""

        div = math.exp((values[0]/values[1])*math.log(2.0))
        return "{:f}(B/NK)".format(div)


    def change_srational_to_string(self, values:tuple)->str:
        """SRATIONALの値を文字列に変換する"""

        print(type(values))
        if values[0] == 0 and values[1] == 0:
            return "{:d}.{:d}".format(values[0], values[1])
        
        if values[1] == 1:
            return "{:d}".format(values[0])
        
        return "{:f}".format(values[0]/values[1])


    def change_rational_to_value(self, jpeg_data:bytes)->str:
        """RATIONALタイプの値を文字列に変更する"""

        change_rational_functions = {
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

        if self.__id in change_rational_functions:
            return change_rational_functions[self.__id](values)
            
        return self.change_rational_to_string(values)


    def change_srational_to_value(self, jpeg_data:bytes)->str:
        """SRATIONALタイプの値を文字列に変更する"""

        change_srational_functions = {
            0x9204:self.change_rational_to_exposure_bias,         # Exposure Bias
            0x9201:self.change_rational_to_shutter_speed,         # Shutter Speed
            0x9203:self.change_rational_to_brightness,            # Brightness
        }

        # RATIONALの場合は、1つめに分子、2つめに分母が入っているので、lengthを2倍にして値を取得している
        values = struct.unpack_from(self.__byte_order+str(self.__length*2)+"l", \
                                    jpeg_data, \
                                    self.__base_offset + self.__value)

        if self.__id in change_srational_functions:
            return change_srational_functions[self.__id](values)

        return self.change_srational_to_string(values)


    def change_tag_value_to_string(self, jpeg_data:bytes)->str:
        """タグの値を文字列に変換する"""

        change_value_functions = {
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
        if self.__type in change_value_functions:
            return change_value_functions[self.__type](jpeg_data)

        return str(self.__value)


    def exif_tag_length(self)->int:
        """Exifタグの長さを返す"""

        return self.__length


    def exif_tag_value(self)->int:
        """Exifタグの値を返す"""

        return self.__value

