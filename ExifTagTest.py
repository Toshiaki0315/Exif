import unittest
from ExifTag import ExifTagInformation

class ExifParserTest(unittest.TestCase):
    def test_change_id_to_string(self):
        exif_data = {"id":0x0000, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "unkown ID")
        exif_data = {"id":0x0100, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("exif", exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "画像の幅")
        exif_data = {"id":0x0100, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "画像の幅")
        exif_data = {"id":0x0100, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("1st", exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "画像の幅")
        exif_data = {"id":0x0100, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("gps", exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "unkown ID")
        exif_data = {"id":0x0001, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("gps", exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "北緯(N) or 南緯(S)")
        exif_data = {"id":0x0100, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("intr", exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "unkown ID")
        exif_data = {"id":0x0001, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("intr", exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "互換性インデックス")

    def test_change_value_to_string(self):
        exif_data = {"id":0x0103, "type":0, "value":1, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_value_to_string(), "非圧縮")
        exif_data = {"id":0x0103, "type":0, "value":6, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_value_to_string(), "JPEG 圧縮(サムネイルのみ)")
        exif_data = {"id":0x0103, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_value_to_string(), "予約")
        exif_data = {"id":0x1001, "type":0, "value":1, "len":0}
        exif_info = ExifTagInformation("intr", exif_data)
        self.assertEqual(exif_info.change_value_to_string(), "1")

    def test_change_format_to_string(self):
        exif_data = {"id":0, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "unkown format")
        exif_data = {"id":0, "type":1, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "BYTE")
        exif_data = {"id":0, "type":2, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "ASCII")
        exif_data = {"id":0, "type":3, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SHORT")
        exif_data = {"id":0, "type":4, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "LONG")
        exif_data = {"id":0, "type":5, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "RATIONAL")
        exif_data = {"id":0, "type":6, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SBYTE")
        exif_data = {"id":0, "type":7, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "UNDEFINED")
        exif_data = {"id":0, "type":8, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SSHORT")
        exif_data = {"id":0, "type":9, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SLONG")
        exif_data = {"id":0, "type":10, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SRATIONAL")
        exif_data = {"id":0, "type":11, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SINGLE FLOAT")
        exif_data = {"id":0, "type":12, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "DOUBLE FLOAT")

    def test_change_int_to_string(self):
        exif_data = {"id":0, "type":0, "value":0x31323334, "len":4}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_int_to_string(), "1234")
        
    def test_change_ascii_to_value(self):
        exif_data = {"id":0, "type":0, "value":0, "len":6}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.change_ascii_to_value(b'\x31\x32\x33\x34\x35\x00', 0), "12345")
        self.assertEqual(exif_info.change_ascii_to_value(b'\x61\x62\x63\x64\x65\x00', 0), "abcde")

    def test_exif_tag_length(self):
        exif_data = {"id":0, "type":0, "value":0, "len":6}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.exif_tag_length(), 6)
        exif_data = {"id":0, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.exif_tag_length(), 0)
        
    def test_exif_tag_value(self):
        exif_data = {"id":0, "type":0, "value":0, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.exif_tag_value(), 0)
        exif_data = {"id":0, "type":0, "value":0xffff, "len":0}
        exif_info = ExifTagInformation("0th", exif_data)
        self.assertEqual(exif_info.exif_tag_value(), 0xffff)
        
if __name__ == '__main__':
    unittest.main()
