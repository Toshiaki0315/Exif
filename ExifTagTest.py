import unittest
import struct
from ExifTag import ExifTagInformation as eti

class ExifParserTest(unittest.TestCase):
    def test_change_id_to_string(self):
        exif_data = {"id":0x0000, "type":0, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "Unkown ID")
        exif_data = {"id":0x0100, "type":0, "value":0, "len":0}
        exif_info = eti("exif", ">", 0, exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "画像の幅")
        exif_data = {"id":0x0100, "type":0, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "画像の幅")
        exif_data = {"id":0x0100, "type":0, "value":0, "len":0}
        exif_info = eti("1st", ">", 0, exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "画像の幅")
        exif_data = {"id":0x0100, "type":0, "value":0, "len":0}
        exif_info = eti("gps", ">", 0, exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "Unkown ID")
        exif_data = {"id":0x0001, "type":0, "value":0, "len":0}
        exif_info = eti("gps", ">", 0, exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "北緯(N) or 南緯(S)")
        exif_data = {"id":0x0100, "type":0, "value":0, "len":0}
        exif_info = eti("intr", ">", 0, exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "Unkown ID")
        exif_data = {"id":0x0001, "type":0, "value":0, "len":0}
        exif_info = eti("intr", ">", 0, exif_data)
        self.assertEqual(exif_info.change_id_to_string(), "互換性インデックス")
        
    def test_change_value_to_string(self):
        exif_data = {"id":0x0103, "type":0, "value":1, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_value_to_string(), "非圧縮")
        exif_data = {"id":0x0103, "type":0, "value":6, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_value_to_string(), "JPEG 圧縮(サムネイルのみ)")
        exif_data = {"id":0x0103, "type":0, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_value_to_string(), "Unkown value")
        exif_data = {"id":0x1001, "type":0, "value":1, "len":0}
        exif_info = eti("intr", ">", 0, exif_data)
        self.assertEqual(exif_info.change_value_to_string(), "1")

    def test_change_format_to_string(self):
        exif_data = {"id":0, "type":0, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "Unkown Format")
        exif_data = {"id":0, "type":1, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "BYTE")
        exif_data = {"id":0, "type":2, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "ASCII")
        exif_data = {"id":0, "type":3, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SHORT")
        exif_data = {"id":0, "type":4, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "LONG")
        exif_data = {"id":0, "type":5, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "RATIONAL")
        exif_data = {"id":0, "type":6, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SBYTE")
        exif_data = {"id":0, "type":7, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "UNDEFINED")
        exif_data = {"id":0, "type":8, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SSHORT")
        exif_data = {"id":0, "type":9, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SLONG")
        exif_data = {"id":0, "type":10, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SRATIONAL")
        exif_data = {"id":0, "type":11, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "SINGLE FLOAT")
        exif_data = {"id":0, "type":12, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_format_to_string(), "DOUBLE FLOAT")

    def test_change_int_to_string(self):
        exif_data = {"id":0, "type":0, "value":0x31323334, "len":4}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_int_to_string(), "1234")
        
    def test_change_ascii_to_value(self):
        exif_data = {"id":0, "type":0, "value":0, "len":6}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.change_ascii_to_value(b'\x31\x32\x33\x34\x35\x00'), "12345")
        self.assertEqual(exif_info.change_ascii_to_value(b'\x61\x62\x63\x64\x65\x00'), "abcde")

    def test_exif_tag_length(self):
        exif_data = {"id":0, "type":0, "value":0, "len":6}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.exif_tag_length(), 6)
        exif_data = {"id":0, "type":0, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.exif_tag_length(), 0)
        
    def test_exif_tag_value(self):
        exif_data = {"id":0, "type":0, "value":0, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.exif_tag_value(), 0)
        exif_data = {"id":0, "type":0, "value":0xffff, "len":0}
        exif_info = eti("0th", ">", 0, exif_data)
        self.assertEqual(exif_info.exif_tag_value(), 0xffff)

    def test_change_rational_to_value(self):
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = struct.pack('>2L', 0x00000002, 0x00000001)
        self.assertEqual(exif_info.change_rational_to_value(data), "2")
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", "<", 0, exif_data)
        data = struct.pack('<2L', 0x00000002, 0x00000001)
        self.assertEqual(exif_info.change_rational_to_value(data), "2")

    def test_change_rational_to_f_number(self):
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = (0x00000002, 0x00000001)
        self.assertEqual(exif_info.change_rational_to_f_number(data), "F2.0")

    def test_change_rational_to_exposure_time(self):
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = (0x00000002, 0x00000001)
        self.assertEqual(exif_info.change_rational_to_exposure_time(data), "2.000000sec")

    def test_change_rational_to_exposure_bias(self):
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = (0x00000002, 0x00000001)
        self.assertEqual(exif_info.change_rational_to_exposure_bias(data), "+2.0")
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = (0x00000000, 0x00000000)
        self.assertEqual(exif_info.change_rational_to_exposure_bias(data), "0.0")
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = (-2, 1)
        self.assertEqual(exif_info.change_rational_to_exposure_bias(data), "-2.0")

    def test_change_rational_to_focal_len(self):
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = (0x00000002, 0x00000001)
        self.assertEqual(exif_info.change_rational_to_focal_len(data), "2mm")

    def test_change_rational_to_distance(self):
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = (0x00000002, 0x00000001)
        self.assertEqual(exif_info.change_rational_to_distance(data), "2.0m")

    def test_change_rational_to_aperture(self):
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = (0x00000002, 0x00000001)
        self.assertEqual(exif_info.change_rational_to_aperture(data), "F2.0 (F2.000000)")

    def test_change_rational_to_shutter_speed(self):
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = (0x00000002, 0x00000001)
        self.assertEqual(exif_info.change_rational_to_shutter_speed(data), "1/4 (0.250000sec)")

    def test_change_rational_to_brightness(self):
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = (0x00000002, 0x00000001)
        self.assertEqual(exif_info.change_rational_to_brightness(data), "4.000000(B/NK)")

    def test_value_to_pim(self):
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = struct.pack('>7s1B1L2B2H1L1H1L', b'PrintIM', 0x00, 0x30313233, 0x00, 0x00, 0x0002, 0x0001, 0x0000000a, 0x0002, 0x0000000b )
        self.assertEqual( exif_info._value_to_pim_header( data ), 'PrintIM' )
        self.assertEqual( exif_info._value_to_pim_version( data ), '0123' )
        self.assertEqual( exif_info._value_to_pim_entry_count( data ), 2 )
        self.assertEqual( exif_info._value_to_pim_entry_id( data, 0 ), 0x0001 )
        self.assertEqual( exif_info._value_to_pim_entry_value( data, 0 ), 0x0000000a )
        self.assertEqual( exif_info._value_to_pim_entry_id( data, 1 ), 0x0002 )
        self.assertEqual( exif_info._value_to_pim_entry_value( data, 1 ), 0x0000000b )

    def test_change_value_to_pim(self):
        exif_data = {"id":0, "type":5, "value":0, "len":1}
        exif_info = eti("0th", ">", 0, exif_data)
        data = struct.pack('>7s1B1L2H1L1H1L', b'PrintIM', 0x00, 0x30313233, 0x0002, 0x0001, 0x0000000a, 0x0002, 0x0000000b )
        self.assertEqual( exif_info.change_value_to_pim(data), 'PrintIM : 0123 : length = 1\n\t--- PrintIM Data ---\n\t  0000 : 000a0002' )
    
    def test_undefined_data_to_string(self):
        exif_data = {"id":0, "type":5, "value":0, "len":5}
        exif_info = eti("0th", ">", 0, exif_data)
        data = struct.pack('>5B', 0x01, 0x02, 0x03, 0x04, 0x05)
        self.assertEqual( exif_info._undefined_data_to_string(data), '\n\t0x01, 0x02, 0x03, 0x04, 0x05, ' )
        exif_data = {"id":0, "type":5, "value":0, "len":11}
        exif_info = eti("0th", ">", 0, exif_data)
        data = struct.pack('>11B', 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, 0x0a)
        self.assertEqual( exif_info._undefined_data_to_string(data), '\n\t0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10, \n\t0x0a, ' )
    
if __name__ == '__main__':
    unittest.main()
