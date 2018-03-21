# ToDoリスト
# ■ バイナリデータから'Exif'の文字列を検出する
# □ バイナリデータから'MM'の文字列を検出する

import unittest
import struct
from ExifParser import AnalyzeExifData

class ExifParserTest(unittest.TestCase):
    def setUp(self):
        # Exif ファイルを読み込んでおく
#        with open('./IMG_3294.jpg', 'rb') as infile:
#            self.data = infile.read()
        pass

    def tearDown(self):
        # 後処理
        pass
    
    # データの中からExifの文字列を探し、そこまでのオフセットが返ってくるかのテスト
    def test_exif_string(self):
        exif_data = AnalyzeExifData()
        data = b'Exif'
        self.assertEqual(exif_data.check_exif_string(data), 6)
        data = b'aaaExif'
        self.assertEqual(exif_data.check_exif_string(data), 9)
        data = b'aaa'
        self.assertEqual(exif_data.check_exif_string(data), -1)

    def test_binary_format(self):
        exif_data = AnalyzeExifData()
        data = struct.pack('4s2B2s', b'Exif', 0, 0, b'MM')
        offset = exif_data.check_exif_string(data)
        exif_data.check_byte_order(data, offset)
        self.assertEqual(exif_data._byte_order, exif_data.BYTE_ORDER_BIG_ENDIAN)
        data = struct.pack('4s2B2s', b'Exif', 0, 0, b'II')
        offset = exif_data.check_exif_string(data)
        exif_data.check_byte_order(data, offset)
        self.assertEqual(exif_data._byte_order, exif_data.BYTE_ORDER_LITTLE_ENDIAN)
        data = struct.pack('4s2B2s', b'Exif', 0, 0, b'MI')
        offset = exif_data.check_exif_string(data)
        exif_data.check_byte_order(data, offset)
        self.assertEqual(exif_data._byte_order, exif_data.BYTE_ORDER_ERROR)
        data = struct.pack('4s2B2s', b'Exif', 0, 0, b'IM')
        offset = exif_data.check_exif_string(data)
        exif_data.check_byte_order(data, offset)
        self.assertEqual(exif_data._byte_order, exif_data.BYTE_ORDER_ERROR)

    def test_get_0th_offset(self):
        exif_data = AnalyzeExifData()
        data = struct.pack('>4s2B2s2BL', b'Exif', 0, 0, b'MM', 0, 0, 0x12345678)
        offset = exif_data.check_exif_string(data)
        exif_data.check_byte_order(data, offset)
        exif_data.get_0th_offset(data, offset)
        self.assertEqual(exif_data._0th_ifd_offset, 0x12345678)
        data = struct.pack('<4s2B2s2BL', b'Exif', 0, 0, b'II', 0, 0, 0x12345678)
        offset = exif_data.check_exif_string(data)
        exif_data.check_byte_order(data, offset)
        exif_data.get_0th_offset(data, offset)
        self.assertEqual(exif_data._0th_ifd_offset, 0x12345678)
        

    def test_get_tag_number(self):
        exif_data = AnalyzeExifData()
        data = struct.pack('>4s2B2s2BLH', b'Exif', 0, 0, b'MM', 0x00, 0x2a, 0x00000008, 0x000b)
        offset_base = exif_data.check_exif_string(data)
        exif_data.check_byte_order(data, offset_base)
        exif_data.get_0th_offset(data, offset_base)
        self.assertEqual(exif_data.get_tag_number(data, offset_base), 0x000b)
        data = struct.pack('<4s2B2s2BLH', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x000b)
        offset_base = exif_data.check_exif_string(data)
        exif_data.check_byte_order(data, offset_base)
        exif_data.get_0th_offset(data, offset_base)
        self.assertEqual(exif_data.get_tag_number(data, offset_base), 0x000b)

    def test_get_tag_info(self):
        exif_data = AnalyzeExifData()
        data = struct.pack('>4s2B2s2BL3H2L', b'Exif', 0, 0, b'MM', 0x00, 0x2a, 0x00000008, 0x0001, 0x0002, 0x0003, 0x11223344, 0xaabbccdd)
        offset_base = exif_data.check_exif_string(data)
        exif_data.check_byte_order(data, offset_base)
        exif_data.get_0th_offset(data, offset_base)
        tag_info = exif_data.get_tag_info(data, offset_base, 0)
        self.assertEqual(tag_info[0], 0x0002)
        self.assertEqual(tag_info[1], 0x0003)
        self.assertEqual(tag_info[2], 0x11223344)
        self.assertEqual(tag_info[3], 0xaabbccdd)
        data = struct.pack('<4s2B2s2BL3H2L', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x0001, 0x0002, 0x0003, 0x11223344, 0xaabbccdd)
        offset_base = exif_data.check_exif_string(data)
        exif_data.check_byte_order(data, offset_base)
        exif_data.get_0th_offset(data, offset_base)
        tag_info = exif_data.get_tag_info(data, offset_base, 0)
        self.assertEqual(tag_info[0], 0x0002)
        self.assertEqual(tag_info[1], 0x0003)
        self.assertEqual(tag_info[2], 0x11223344)
        self.assertEqual(tag_info[3], 0xaabbccdd)

if __name__ == '__main__':
    unittest.main()