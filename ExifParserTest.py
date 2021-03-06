# ToDoリスト
# ■ バイナリデータから'Exif'の文字列を検出する
# ■ バイナリデータから'MM'の文字列を検出する
# ■ バイナリデータから'II'の文字列を検出する
# ■ バイナリデータに'MM'かII'が無い場合はエラーにする
# ■ ビッグエンディアンで0thのオフセットを取得できる
# ■ リトルエンディアンで0thのオフセットを取得できる
# ■ ビッグエンディアンで0thのデータ数を取得できる
# ■ リトルエンディアンで0thのデータ数を取得できる
# ■ ビッグエンディアンで0thのTAGデータを取得できる
# ■ リトルエンディアンで0thのTAGデータを取得できる
# ■ ビッグエンディアンで1stのオフセットを取得できる
# ■ リトルエンディアンで1stのオフセットを取得できる
# ■ ビッグエンディアンでexifのオフセットを取得できる
# ■ リトルエンディアンでexifのオフセットを取得できる
# ■ ビッグエンディアンでgpsのオフセットを取得できる
# ■ リトルエンディアンでgpsのオフセットを取得できる
# ■ ビッグエンディアンでintrのオフセットを取得できる
# ■ リトルエンディアンでintrのオフセットを取得できる
# × ビッグエンディアンで0th,1st,exif,gps,intrのオフセットを設定できる
# × リトルエンディアンで0th,1st,exif,gps,intrのオフセットを設定できる


import unittest
import struct
from ExifParser import ParseExifData

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
        exif_header = ParseExifData(struct.pack('4s2B2s', b'Exif', 0, 0, b'MM'))
        self.assertEqual(exif_header.check_exif_string(), 6)

        exif_header = ParseExifData(struct.pack('7s2B2s', b'aaaExif', 0, 0, b'MM'))
        self.assertEqual(exif_header.check_exif_string(), 9)

        exif_header = ParseExifData(struct.pack('3s', b'aaa'))
        self.assertEqual(exif_header.check_exif_string(), -1)

    def test_binary_format(self):
        exif_header = ParseExifData(struct.pack('4s2B2s', b'Exif', 0, 0, b'MM'))
        exif_header.check_exif_string()
        self.assertEqual(exif_header.exif_byte_order(), exif_header.BYTE_ORDER_BIG_ENDIAN)

        exif_header = ParseExifData(struct.pack('4s2B2s', b'Exif', 0, 0, b'II'))
        exif_header.check_exif_string()
        self.assertEqual(exif_header.exif_byte_order(), exif_header.BYTE_ORDER_LITTLE_ENDIAN)

        exif_header = ParseExifData(struct.pack('4s2B2s', b'Exif', 0, 0, b'MI'))
        exif_header.check_exif_string()
        self.assertEqual(exif_header.exif_byte_order(), exif_header.BYTE_ORDER_ERROR)

        exif_header = ParseExifData(struct.pack('4s2B2s', b'Exif', 0, 0, b'IM'))
        exif_header.check_exif_string()
        self.assertEqual(exif_header.exif_byte_order(), exif_header.BYTE_ORDER_ERROR)

    def test_ifd_0th_offset(self):
        exif_header = ParseExifData(struct.pack('>4s2B2s2BL', b'Exif', 0, 0, b'MM', 0, 0, 0x12345678))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        self.assertEqual(exif_header.ifd_offset("0th"), 0x12345678)

        exif_header = ParseExifData(struct.pack('<4s2B2s2BL', b'Exif', 0, 0, b'II', 0, 0, 0x12345678))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        self.assertEqual(exif_header.ifd_offset("0th"), 0x12345678)
        
    def test_tag_number(self):
        exif_header = ParseExifData(struct.pack('>4s2B2s2BLH', b'Exif', 0, 0, b'MM', 0x00, 0x2a, 0x00000008, 0x000b))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        self.assertEqual(exif_header.tag_number("0th"), 0x000b)

        exif_header = ParseExifData(struct.pack('<4s2B2s2BLH', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x000b))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        self.assertEqual(exif_header.tag_number("0th"), 0x000b)

    def test_get_tag_info(self):
        exif_header = ParseExifData(struct.pack('>4s2B2s2BL3H2L', b'Exif', 0, 0, b'MM', 0x00, 0x2a, 0x00000008, 0x0001, 0x0002, 0x0003, 0x11223344, 0xaabbccdd))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        tag_info = exif_header.get_tag_info("0th", 0)
        self.assertEqual(tag_info[0], 0x0002)
        self.assertEqual(tag_info[1], 0x0003)
        self.assertEqual(tag_info[2], 0x11223344)
        self.assertEqual(tag_info[3], 0xaabbccdd)

        exif_header = ParseExifData(struct.pack('<4s2B2s2BL3H2L', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x0001, 0x0002, 0x0003, 0x11223344, 0xaabbccdd))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        tag_info = exif_header.get_tag_info("0th", 0) 
        self.assertEqual(tag_info[0], 0x0002)
        self.assertEqual(tag_info[1], 0x0003)
        self.assertEqual(tag_info[2], 0x11223344)
        self.assertEqual(tag_info[3], 0xaabbccdd)

    def test_ifd_1st_offset(self):
        exif_header = ParseExifData(struct.pack('>4s2B2s2BL3H3L', b'Exif', 0, 0, b'MM', 0x00, 0x2a, 0x00000008, 0x0001, 0x0002, 0x0003, 0x11223344, 0xaabbccdd, 0x55667788))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        exif_header.ifd_1st_offset(1)
        self.assertEqual(exif_header.ifd_offset("1st"), 0x55667788)

        exif_header = ParseExifData(struct.pack('<4s2B2s2BL3H3L', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x0001, 0x0002, 0x0003, 0x11223344, 0xaabbccdd, 0x55667788))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        exif_header.ifd_1st_offset(1)
        self.assertEqual(exif_header.ifd_offset("1st"), 0x55667788)

    def test_exif_offset(self):
        exif_header = ParseExifData(struct.pack('>4s2B2s2BL3H3L', b'Exif', 0, 0, b'MM', 0x00, 0x2a, 0x00000008, 0x0001, 0x8769, 0x0003, 0x11223344, 0xaabbccdd, 0x55667788))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        exif_header.ifd_1st_offset(1)
        exif_header.get_tag_info("0th", 0)
        self.assertEqual(exif_header.ifd_offset("exif"), 0xaabbccdd)

        exif_header = ParseExifData(struct.pack('<4s2B2s2BL3H3L', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x0001, 0x8769, 0x0003, 0x11223344, 0xaabbccdd, 0x55667788))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        exif_header.ifd_1st_offset(1)
        exif_header.get_tag_info("0th", 0)
        self.assertEqual(exif_header.ifd_offset("exif"), 0xaabbccdd)
        
    def test_gps_offset(self):
        exif_header = ParseExifData(struct.pack('>4s2B2s2BL3H3L', b'Exif', 0, 0, b'MM', 0x00, 0x2a, 0x00000008, 0x0001, 0x8825, 0x0003, 0x11223344, 0xaabbccdd, 0x55667788))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        exif_header.ifd_1st_offset(1)
        exif_header.get_tag_info("0th", 0)
        self.assertEqual(exif_header.ifd_offset("gps"), 0xaabbccdd)

        exif_header = ParseExifData(struct.pack('<4s2B2s2BL3H3L', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x0001, 0x8825, 0x0003, 0x11223344, 0xaabbccdd, 0x55667788))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        exif_header.ifd_1st_offset(1)
        exif_header.get_tag_info("0th", 0)
        self.assertEqual(exif_header.ifd_offset("gps"), 0xaabbccdd)
        
    def test_intr_offset(self):
        exif_header = ParseExifData(struct.pack('>4s2B2s2BL3H3L', b'Exif', 0, 0, b'MM', 0x00, 0x2a, 0x00000008, 0x0001, 0xA005, 0x0003, 0x11223344, 0xaabbccdd, 0x55667788))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        exif_header.ifd_1st_offset(1)
        exif_header.get_tag_info("0th", 0)
        self.assertEqual(exif_header.ifd_offset("intr"), 0xaabbccdd)

        exif_header = ParseExifData(struct.pack('<4s2B2s2BL3H3L', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x0001, 0xA005, 0x0003, 0x11223344, 0xaabbccdd, 0x55667788))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        exif_header.ifd_1st_offset(1)
        exif_header.get_tag_info("0th", 0)
        self.assertEqual(exif_header.ifd_offset("intr"), 0xaabbccdd)

    def test_parse_ifd_tag_info(self):
        exif_header = ParseExifData(struct.pack('<4s2B2s2BL3H3L1H', b'Exif', 0, 0, b'II', 0x00, 0x2a, 0x00000008, 0x0001, 0x8825, 0x0003, 0x11223344, 26, 0xaabbccdd, 0x0))
        exif_header.check_exif_string()
        exif_header.ifd_0th_offset()
        exif_header.ifd_1st_offset(1)
        exif_header.get_tag_info("0th", 0)
        self.assertEqual(exif_header.ifd_offset("gps"), 26)
        self.assertEqual(exif_header.tag_number("gps"), 0x0)
        for count in range(exif_header.tag_number("gps")):
            exif_header.get_tag_info("gps", count)
        self.assertEqual(exif_header.exif_info_length("gps"), 0)
                                                    
if __name__ == '__main__':
    unittest.main()
