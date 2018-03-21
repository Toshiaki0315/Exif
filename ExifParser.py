import struct

class AnalyzeExifData:
    
    BYTE_ORDER_NONE          = 0
    BYTE_ORDER_LITTLE_ENDIAN = 1
    BYTE_ORDER_BIG_ENDIAN    = 2
    BYTE_ORDER_ERROR         = -1

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
        if self._byte_order == self.BYTE_ORDER_BIG_ENDIAN:
            self._0th_ifd_offset = struct.unpack_from(">L", data, offset+4)[0]
        elif self._byte_order == self.BYTE_ORDER_LITTLE_ENDIAN:
            self._0th_ifd_offset = struct.unpack_from("<L", data, offset+4)[0]
        return

    def get_tag_number(self, data, offset_base):
        if self._byte_order == self.BYTE_ORDER_BIG_ENDIAN:
            return struct.unpack_from(">H", data, offset_base+self._0th_ifd_offset)[0]
        elif self._byte_order == self.BYTE_ORDER_LITTLE_ENDIAN:
            return struct.unpack_from("<H", data, offset_base+self._0th_ifd_offset)[0]
        return -1
    
    def get_tag_info(self, data, offset_base, offset_info):
        if self._byte_order == self.BYTE_ORDER_BIG_ENDIAN:
            return struct.unpack_from(">2H2L", data, offset_base+self._0th_ifd_offset+2+offset_info)
        elif self._byte_order == self.BYTE_ORDER_LITTLE_ENDIAN:
            return struct.unpack_from("<2H2L", data, offset_base+self._0th_ifd_offset+2+offset_info)
        return -1

        