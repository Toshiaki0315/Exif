import unittest
from ExifTag import ExifTagInformation

class ExifParserTest(unittest.TestCase):
    def test_change_id_to_string(self):
        self.assertEqual(ExifTagInformation().change_id_to_string("0th", 0x0000), "unkown ID")
        self.assertEqual(ExifTagInformation().change_id_to_string("exif", 0x0100), "画像の幅")
        self.assertEqual(ExifTagInformation().change_id_to_string("0th", 0x0100), "画像の幅")
        self.assertEqual(ExifTagInformation().change_id_to_string("1st", 0x0100), "画像の幅")
        self.assertEqual(ExifTagInformation().change_id_to_string("gps", 0x0100), "unkown ID")
        self.assertEqual(ExifTagInformation().change_id_to_string("gps", 0x0001), "北緯(N) or 南緯(S)")
        self.assertEqual(ExifTagInformation().change_id_to_string("intr", 0x0100), "unkown ID")
        self.assertEqual(ExifTagInformation().change_id_to_string("intr", 0x0001), "互換性インデックス")

    def test_change_value_to_string(self):
        self.assertEqual(ExifTagInformation().change_value_to_string("0th", 0x0103, 1), "非圧縮")
        self.assertEqual(ExifTagInformation().change_value_to_string("0th", 0x0103, 6), "JPEG 圧縮(サムネイルのみ)")
        self.assertEqual(ExifTagInformation().change_value_to_string("0th", 0x0103, 0), "予約")
        self.assertEqual(ExifTagInformation().change_value_to_string("intr", 0x1001, 1), "1")

    def test_change_format_to_string(self):
        self.assertEqual(ExifTagInformation().change_format_to_string(0), "unkown format")
        self.assertEqual(ExifTagInformation().change_format_to_string(1), "BYTE")
        self.assertEqual(ExifTagInformation().change_format_to_string(2), "ASCII")
        self.assertEqual(ExifTagInformation().change_format_to_string(3), "SHORT")
        self.assertEqual(ExifTagInformation().change_format_to_string(4), "LONG")
        self.assertEqual(ExifTagInformation().change_format_to_string(5), "RATIONAL")
        self.assertEqual(ExifTagInformation().change_format_to_string(6), "SBYTE")
        self.assertEqual(ExifTagInformation().change_format_to_string(7), "UNDEFINED")
        self.assertEqual(ExifTagInformation().change_format_to_string(8), "SSHORT")
        self.assertEqual(ExifTagInformation().change_format_to_string(9), "SLONG")
        self.assertEqual(ExifTagInformation().change_format_to_string(10), "SRATIONAL")
        self.assertEqual(ExifTagInformation().change_format_to_string(11), "SINGLE FLOAT")
        self.assertEqual(ExifTagInformation().change_format_to_string(12), "DOUBLE FLOAT")

    def test_change_int_to_string(self):
        self.assertEqual(ExifTagInformation().change_int_to_string(4, 0x31323334), "1234")
        
    def test_change_ascii_to_value(self):
        self.assertEqual(ExifTagInformation().change_ascii_to_value(6, 0, b'\x31\x32\x33\x34\x35\x00', 0), "12345")
        self.assertEqual(ExifTagInformation().change_ascii_to_value(6, 0, b'\x61\x62\x63\x64\x65\x00', 0), "abcde")

if __name__ == '__main__':
    unittest.main()
