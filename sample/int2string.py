import unittest

class Int2String:
     
    def int_to_string(self, int_value):
        return int_value.to_bytes(6, byteorder='big').decode("ascii").strip('\x00')

class Binary2String:
    def binary_to_string(self, binary_value):
        return binary_value.decode(encoding='sjis').strip('\x00')

class Ascii2String:
    def change_ascii_to_value( self, length, value, data, offset ):
        return data.decode(encoding='ascii', errors='replace').strip('\x00')[offset:offset+length]

class Int2StringTest(unittest.TestCase):

    def test_binary_to_string(self):
        self.assertEqual( Binary2String().binary_to_string(b'abcd\x00'), "abcd")
        self.assertEqual( Binary2String().binary_to_string(b'1234\x00'), "1234")

    def test_int_to_string(self):
        self.assertEqual( Int2String().int_to_string( 0x30313233 ), "0123" )
        self.assertEqual( Int2String().int_to_string( 0x61626364 ), "abcd" )
        self.assertEqual( Int2String().int_to_string( 0x41424344 ), "ABCD" )

    def test_change_ascii_to_value(self):
        self.assertEqual(Ascii2String().change_ascii_to_value(6, 0, b'\x31\x32\x33\x34\x35\x00', 0), "12345")
        self.assertEqual(Ascii2String().change_ascii_to_value(6, 0, b'\x61\x62\x63\x64\x65\x00', 0), "abcde")
        self.assertEqual(Ascii2String().change_ascii_to_value(3, 0, b'\x61\x62\x63\x64\x65\x00', 0), "abc")

if __name__ == '__main__':
    unittest.main()
