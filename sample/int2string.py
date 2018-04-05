import unittest

class Int2String:
     
    def int_to_string(self, int_value):
        return int_value.to_bytes(6, byteorder='big').decode("ascii").strip('\x00')

class Binary2String:
    def binary_to_string(self, binary_value):
        return binary_value.decode('sjis').strip('\x00')

class Int2StringTest(unittest.TestCase):

    def test_binary_to_string(self):
        self.assertEqual( Binary2String().binary_to_string(b'abcd\x00'), "abcd")
        self.assertEqual( Binary2String().binary_to_string(b'1234\x00'), "1234")

    def test_int_to_string(self):
        self.assertEqual( Int2String().int_to_string( 0x30313233 ), "0123" )
        self.assertEqual( Int2String().int_to_string( 0x61626364 ), "abcd" )
        self.assertEqual( Int2String().int_to_string( 0x41424344 ), "ABCD" )

if __name__ == '__main__':
    unittest.main()
