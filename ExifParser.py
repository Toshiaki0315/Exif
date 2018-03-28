import struct

class ParseExifData:
    
    BYTE_ORDER_NONE          = ""
    BYTE_ORDER_LITTLE_ENDIAN = "<"
    BYTE_ORDER_BIG_ENDIAN    = ">"
    BYTE_ORDER_ERROR         = "ERR"

    _offset = {"0th":0, "1st":0, "exif":0, "gps":0, "intr":0}
    _byte_order      = BYTE_ORDER_NONE
    _base_offset  = -1
    _exif_info = {}

    def __init__(self):
        pass

    def check_exif_string(self, data):
        self._base_offset = data.decode(encoding='ascii',errors='replace').find('Exif')
        if self._base_offset >= 0:
            self._base_offset += (len('Exif')+2)
            self.check_byte_order(data)
        return self._base_offset
    
    def check_byte_order(self, data):
        bye_orders = {b'MM':self.BYTE_ORDER_BIG_ENDIAN, b'II':self.BYTE_ORDER_LITTLE_ENDIAN}

        byte_order = struct.unpack_from("2s", data, self._base_offset)
        if byte_order[0] in bye_orders:
            self._byte_order = bye_orders[byte_order[0]]
        else:
            self._byte_order = self.BYTE_ORDER_ERROR

        return

    def get_0th_offset(self, data):
        self._offset["0th"] = struct.unpack_from(self._byte_order+"L", data, self._base_offset+4)[0]
        return
 
    def get_1st_ifd_offset(self, data, tag_num):
        self._offset["1st"] = struct.unpack_from(self._byte_order+"L", data, self._base_offset+self._offset["0th"]+2+tag_num*12)[0]
        return

    def set_offset(self, key, offset):
        self._offset[key] = offset

    def get_offset(self, ifd):
        return self._offset[ifd]

    def get_tag_number(self, data, ifd):
        tag_number = struct.unpack_from(self._byte_order+"H", data, self._base_offset+self._offset[ifd])[0]
        return tag_number
    
    def get_tag_info(self, data, ifd, count):
        tag_id_ifds = {0x8769:"exif", 0x8825:"gps", 0xA005:"intr"}

        tag_info = struct.unpack_from(self._byte_order+"2H2L", data, self._base_offset+self._offset[ifd]+2+count*12)
        self._exif_info.setdefault(ifd, [] ).append({"id":tag_info[0], "type":tag_info[1], "len":tag_info[2], "value":tag_info[3]})

        if tag_info[0] in tag_id_ifds:
            self._offset[tag_id_ifds[tag_info[0]]] = tag_info[3]

        return tag_info

    def parse_ifd(self, data, ifd):

        for count in range(self.get_tag_number(data, ifd)):
            self.get_tag_info(data, ifd, count)
        
        return

    def parse_0th_ifd(self, data):

        self.get_0th_offset(data)

        self.parse_ifd(data, "0th")

        self.get_1st_ifd_offset(data, len(self._exif_info["0th"]))
        
        return
