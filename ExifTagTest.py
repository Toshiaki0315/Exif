import unittest
from ExifTag import ExifTagInfomation

class ExifParserTest(unittest.TestCase):
    def test_change_id_to_string(self):
        self.assertEqual(ExifTagInfomation().change_id_to_string("0th", 0x0000), "unkown ID")
        self.assertEqual(ExifTagInfomation().change_id_to_string("exif", 0x0100), "unkown IFD")
        self.assertEqual(ExifTagInfomation().change_id_to_string("0th", 0x0100), "画像の幅")
        self.assertEqual(ExifTagInfomation().change_id_to_string("1st", 0x0100), "画像の幅")
        self.assertEqual(ExifTagInfomation().change_id_to_string("gps", 0x0100), "unkown ID")
        self.assertEqual(ExifTagInfomation().change_id_to_string("gps", 0x0001), "北緯(N) or 南緯(S)")
        self.assertEqual(ExifTagInfomation().change_id_to_string("intr", 0x0100), "unkown ID")
        self.assertEqual(ExifTagInfomation().change_id_to_string("intr", 0x0001), "互換性インデックス")

    def test_change_format_to_string(self):
        self.assertEqual(ExifTagInfomation().change_format_to_string(0), "unkown format")
        self.assertEqual(ExifTagInfomation().change_format_to_string(1), "BYTE")
        self.assertEqual(ExifTagInfomation().change_format_to_string(2), "ASCII")
        self.assertEqual(ExifTagInfomation().change_format_to_string(3), "SHORT")
        self.assertEqual(ExifTagInfomation().change_format_to_string(4), "LONG")
        self.assertEqual(ExifTagInfomation().change_format_to_string(5), "RATIONAL")
        self.assertEqual(ExifTagInfomation().change_format_to_string(6), "SBYTE")
        self.assertEqual(ExifTagInfomation().change_format_to_string(7), "UNDEFINED")
        self.assertEqual(ExifTagInfomation().change_format_to_string(8), "SSHORT")
        self.assertEqual(ExifTagInfomation().change_format_to_string(9), "SLONG")
        self.assertEqual(ExifTagInfomation().change_format_to_string(10), "SRATIONAL")
        self.assertEqual(ExifTagInfomation().change_format_to_string(11), "SINGLE FLOAT")
        self.assertEqual(ExifTagInfomation().change_format_to_string(12), "DOUBLE FLOAT")

if __name__ == '__main__':
    unittest.main()