import struct

class AnalyzeExifData:
    
    BYTE_ORDER_NONE          = ""
    BYTE_ORDER_LITTLE_ENDIAN = "<"
    BYTE_ORDER_BIG_ENDIAN    = ">"
    BYTE_ORDER_ERROR         = "ERR"

    _byte_order      = BYTE_ORDER_NONE
    _base_offset  = -1

    def __init__(self):
        pass

    def check_exif_string(self, data):
        self._base_offset = data.decode(encoding='ascii',errors='replace').find('Exif')
        if self._base_offset >= 0:
            self._base_offset += (len('Exif')+2)
        return self._base_offset
    
    def check_byte_order(self, data):
        byte_order = struct.unpack_from("2s", data, self._base_offset)
        if byte_order[0] == b'MM':
            self._byte_order = self.BYTE_ORDER_BIG_ENDIAN
        elif byte_order[0] == b'II':
            self._byte_order = self.BYTE_ORDER_LITTLE_ENDIAN
        else:
            self._byte_order = self.BYTE_ORDER_ERROR
        return

    def get_0th_offset(self, data):
        return struct.unpack_from(self._byte_order+"L", data, self._base_offset+4)[0]
 
    def get_tag_number(self, data, offset):
        return struct.unpack_from(self._byte_order+"H", data, self._base_offset+offset)[0]
    
    def get_tag_info(self, data, offset):
        return struct.unpack_from(self._byte_order+"2H2L", data, self._base_offset+offset)
    
    def get_1st_ifd_offset(self, data, offset):
        return struct.unpack_from(self._byte_order+"L", data, self._base_offset+offset)[0]

        