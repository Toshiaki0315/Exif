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
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        self.assertEqual(exif_data._byte_order, exif_data.BYTE_ORDER_BIG_ENDIAN)
        data = struct.pack('4s2B2s', b'Exif', 0, 0, b'II')
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        self.assertEqual(exif_data._byte_order, exif_data.BYTE_ORDER_LITTLE_ENDIAN)
        data = struct.pack('4s2B2s', b'Exif', 0, 0, b'MI')
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        self.assertEqual(exif_data._byte_order, exif_data.BYTE_ORDER_ERROR)
        data = struct.pack('4s2B2s', b'Exif', 0, 0, b'IM')
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        self.assertEqual(exif_data._byte_order, exif_data.BYTE_ORDER_ERROR)

    def test_get_0th_offset(self):
        exif_data = AnalyzeExifData()
        data = struct.pack('>4s2B2s2BL', b'Exif', 0, 0, b'MM', 0, 0, 0x12345678)
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        exif_data.get_0th_offset(data)
        self.assertEqual(exif_data._offset["0th"], 0x12345678)
        data = struct.pack('<4s2B2s2BL', b'Exif', 0, 0, b'II', 0, 0, 0x12345678)
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        exif_data.get_0th_offset(data)
        self.assertEqual(exif_data._offset["0th"], 0x12345678)
        
    def test_get_tag_number(self):
        exif_data = AnalyzeExifData()
        data = struct.pack('>4s2B2s2BLH', b'Exif', 0, 0, b'MM', 0x00, 0x2a, 0x00000008, 0x000b)
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        exif_data.get_0th_offset(data)
        self.assertEqual(exif_data.get_tag_number(data, "0th"), 0x000b)
        data = struct.pack('<4s2B2s2BLH', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x000b)
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        exif_data.get_0th_offset(data)
        self.assertEqual(exif_data.get_tag_number(data, "0th"), 0x000b)

    def test_get_tag_info(self):
        exif_data = AnalyzeExifData()
        data = struct.pack('>4s2B2s2BL3H2L', b'Exif', 0, 0, b'MM', 0x00, 0x2a, 0x00000008, 0x0001, 0x0002, 0x0003, 0x11223344, 0xaabbccdd)
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        exif_data.get_0th_offset(data)
        tag_info = exif_data.get_tag_info(data, "0th", 0) #TAGナンバー分（+2）ずらす
        self.assertEqual(tag_info[0], 0x0002)
        self.assertEqual(tag_info[1], 0x0003)
        self.assertEqual(tag_info[2], 0x11223344)
        self.assertEqual(tag_info[3], 0xaabbccdd)
        data = struct.pack('<4s2B2s2BL3H2L', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x0001, 0x0002, 0x0003, 0x11223344, 0xaabbccdd)
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        exif_data.get_0th_offset(data)
        tag_info = exif_data.get_tag_info(data, "0th", 0) #TAGナンバー分（+2）ずらす
        self.assertEqual(tag_info[0], 0x0002)
        self.assertEqual(tag_info[1], 0x0003)
        self.assertEqual(tag_info[2], 0x11223344)
        self.assertEqual(tag_info[3], 0xaabbccdd)

    def test_get_1st_ifd_offset(self):
        exif_data = AnalyzeExifData()
        data = struct.pack('>4s2B2s2BL3H3L', b'Exif', 0, 0, b'MM', 0x00, 0x2a, 0x00000008, 0x0001, 0x0002, 0x0003, 0x11223344, 0xaabbccdd, 0x55667788)
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        exif_data.get_0th_offset(data)
        exif_data.get_1st_ifd_offset(data, 1)
        self.assertEqual(exif_data._offset["1st"], 0x55667788)
        data = struct.pack('<4s2B2s2BL3H3L', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x0001, 0x0002, 0x0003, 0x11223344, 0xaabbccdd, 0x55667788)
        exif_data.check_exif_string(data)
        exif_data.check_byte_order(data)
        exif_data.get_0th_offset(data)
        exif_data.get_1st_ifd_offset(data, 1)
        self.assertEqual(exif_data._offset["1st"], 0x55667788)

    def test_set_offset(self):
        exif_data = AnalyzeExifData()
        exif_data.set_offset("0th", 1111)
        self.assertEqual(exif_data._offset["0th"], 1111)
        self.assertNotEqual(exif_data._offset["1st"], 1111)
        self.assertNotEqual(exif_data._offset["exif"], 1111)
        self.assertNotEqual(exif_data._offset["gps"], 1111)
        exif_data.set_offset("1st", 2222)
        self.assertEqual(exif_data._offset["0th"], 1111)
        self.assertEqual(exif_data._offset["1st"], 2222)
        self.assertNotEqual(exif_data._offset["exif"], 1111)
        self.assertNotEqual(exif_data._offset["gps"], 1111)
        exif_data.set_offset("exif", 3333)
        self.assertEqual(exif_data._offset["0th"], 1111)
        self.assertEqual(exif_data._offset["1st"], 2222)
        self.assertEqual(exif_data._offset["exif"], 3333)
        self.assertNotEqual(exif_data._offset["gps"], 1111)
        exif_data.set_offset("gps", 4444)
        self.assertEqual(exif_data._offset["0th"], 1111)
        self.assertEqual(exif_data._offset["1st"], 2222)
        self.assertEqual(exif_data._offset["exif"], 3333)
        self.assertEqual(exif_data._offset["gps"], 4444)
        
if __name__ == '__main__':
    unittest.main()