import struct

class AnalyzeExifData:
    
    BYTE_ORDER_NONE          = ""
    BYTE_ORDER_LITTLE_ENDIAN = "<"
    BYTE_ORDER_BIG_ENDIAN    = ">"
    BYTE_ORDER_ERROR         = "ERR"

    _byte_order      = BYTE_ORDER_NONE
    _0th_ifd_offset  = -1
    _1st_ifd_offset  = 0
    _intr_ifd_offset = 0
    _gps_idf_offset  = 0
    _exif_ifd_offset = 0

    def __init__(self):
        pass

    def check_exif_string(self, data):
        offset = data.decode(errors='replace').find('Exif')
        if offset >= 0:
            offset += (len('Exif')+2)
        return offset
    
    def check_byte_order(self, data, offset):
        byte_order = struct.unpack_from("2s", data, offset)
        if byte_order[0] == b'MM':
            self._byte_order = self.BYTE_ORDER_BIG_ENDIAN
        elif byte_order[0] == b'II':
            self._byte_order = self.BYTE_ORDER_LITTLE_ENDIAN
        else:
            self._byte_order = self.BYTE_ORDER_ERROR
            
        return

    def get_0th_offset(self, data, offset):
        self._0th_ifd_offset = struct.unpack_from(self._byte_order+"L", data, offset+4)[0]
        return

    def get_tag_number(self, data, offset_base):
        return struct.unpack_from(self._byte_order+"H", data, offset_base+self._0th_ifd_offset)[0]
    
    def get_tag_info(self, data, offset_base):
        return struct.unpack_from(self._byte_order+"2H2L", data, offset_base+self._0th_ifd_offset)
    
    def get_1st_ifd_offset(self, data, offset):
        return struct.unpack_from(self._byte_order+"L", data, offset+self._0th_ifd_offset)[0]

        