import struct

class AnalyzeExifData:
    
    BYTE_ORDER_LITTLE_ENDIAN = 1
    BYTE_ORDER_BIG_ENDIAN    = 2
    BYTE_ORDER_ERROR         = 0

    _0th_ifd_offset  = 0
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
            return self.BYTE_ORDER_BIG_ENDIAN
        elif byte_order[0] == b'II':
            return self.BYTE_ORDER_LITTLE_ENDIAN
        return self.BYTE_ORDER_ERROR

    def byte_order(self, endian, data):
        if endian == self.BYTE_ORDER_BIG_ENDIAN:
            return int.from_bytes(data, 'big')
        elif endian == self.BYTE_ORDER_LITTLE_ENDIAN:
            return int.from_bytes(data, 'little')
        return -1

    def get_0th_offset(self, endian, data, offset):
        if endian == self.BYTE_ORDER_BIG_ENDIAN:
            return struct.unpack_from(">L", data, offset+4)[0]
        elif endian == self.BYTE_ORDER_LITTLE_ENDIAN:
            return struct.unpack_from("<L", data, offset+4)[0]
        return -1

    def get_tag_number(self, endian, data, offset_base, offset_0th_ifd):
        if endian == self.BYTE_ORDER_BIG_ENDIAN:
            return struct.unpack_from(">H", data, offset_base+offset_0th_ifd)[0]
        elif endian == self.BYTE_ORDER_LITTLE_ENDIAN:
            return struct.unpack_from("<H", data, offset_base+offset_0th_ifd)[0]
        return -1
    
    def get_tag_info(self, endian, data, offset_base, offset_0th_ifd):
        if endian == self.BYTE_ORDER_BIG_ENDIAN:
            return struct.unpack_from(">2H2L", data, offset_base+offset_0th_ifd+2)
        elif endian == self.BYTE_ORDER_LITTLE_ENDIAN:
            return struct.unpack_from("<2H2L", data, offset_base+offset_0th_ifd+2)
        return -1
        