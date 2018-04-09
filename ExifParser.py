import struct

class ParseExifData:
    
    BYTE_ORDER_NONE          = ""
    BYTE_ORDER_LITTLE_ENDIAN = "<"
    BYTE_ORDER_BIG_ENDIAN    = ">"
    BYTE_ORDER_ERROR         = "ERR"

    __offset = {"0th":0, "1st":0, "exif":0, "gps":0, "intr":0}
    __byte_order      = BYTE_ORDER_NONE
    __base_offset  = -1
    __data = None

    _exif_info = {}

    def __init__(self, data):
        self.__data = data

    def check_exif_string(self):
        self.__base_offset = self.__data.decode(encoding='ascii',errors='replace').find('Exif')
        if self.__base_offset >= 0:
            self.__base_offset += (len('Exif')+2)
            self.check_byte_order()
        return self.__base_offset
    
    def check_byte_order(self):
        bye_orders = {b'MM':self.BYTE_ORDER_BIG_ENDIAN, b'II':self.BYTE_ORDER_LITTLE_ENDIAN}

        byte_order = struct.unpack_from("2s", self.__data, self.__base_offset)
        if byte_order[0] in bye_orders:
            self.__byte_order = bye_orders[byte_order[0]]
        else:
            self.__byte_order = self.BYTE_ORDER_ERROR

        return

    def get_0th_offset(self):
        self.__offset["0th"] = struct.unpack_from(self.__byte_order+"L", self.__data, self.__base_offset+4)[0]
        return
 
    def get_1st_ifd_offset(self, tag_num):
        self.__offset["1st"] = struct.unpack_from(self.__byte_order+"L", self.__data, self.__base_offset+self.__offset["0th"]+2+tag_num*12)[0]
        return

    def get_offset(self, ifd):
        return self.__offset[ifd]

    def get_tag_number(self, ifd):
        return struct.unpack_from(self.__byte_order+"H", self.__data, self.__base_offset+self.__offset[ifd])[0]
    
    def get_tag_info(self, ifd, count):
        tag_id_ifds = {0x8769:"exif", 0x8825:"gps", 0xA005:"intr"}

        tag_info = struct.unpack_from(self.__byte_order+"2H2L", self.__data, self.__base_offset+self.__offset[ifd]+2+count*12)
        self._exif_info.setdefault(ifd, [] ).append({"id":tag_info[0], "type":tag_info[1], "len":tag_info[2], "value":tag_info[3]})

        if tag_info[0] in tag_id_ifds:
            self.__offset[tag_id_ifds[tag_info[0]]] = tag_info[3]

        return tag_info

    def parse_ifd(self, ifd):

        for count in range(self.get_tag_number(ifd)):
            self.get_tag_info(ifd, count)
        
        return

    def parse_0th_ifd(self):

        self.get_0th_offset()

        self.parse_ifd("0th")

        self.get_1st_ifd_offset(len(self._exif_info["0th"]))
        
        return

    def exif_byte_order(self):
        return self.__byte_order
    
    def exif_info(self, ifd, count):
        return self._exif_info[ifd][count]
    
    def exif_info_length(self, ifd):
        return len(self._exif_info[ifd])
    
    def exif_base_offset(self):
        return self.__base_offset

