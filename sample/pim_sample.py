import unittest
import struct

class Value2Pim():
     
    def value_to_pim_header( self, value ):
        return struct.unpack_from(">8s", value, 0)[0]

    def value_to_pim_version( self, value ):
        return struct.unpack_from(">1L", value, 8)[0]

    def value_to_pim_entry_count( self, value ):
        return struct.unpack_from(">1H", value, 12)[0]

    def value_to_pim_entry_id( self, value, count ):
        return struct.unpack_from(">1H1L", value, 14 + count * 6)[0]
    
    def value_to_pim_entry_value( self, value, count ):
        return struct.unpack_from(">1H1L", value, 14 + count * 6)[1]

class Value2PimTest(unittest.TestCase):

    def test_value_to_pim(self):
        data = struct.pack('>7s1B1L2H1L1H1L', b'PrintIM', 0x00, 0x30313233, 0x0002, 0x0001, 0x0000000a, 0x0002, 0x0000000b )
        self.assertEqual( Value2Pim().value_to_pim_header( data ), b'PrintIM\x00' )
        self.assertEqual( Value2Pim().value_to_pim_version( data ), 0x30313233 )
        self.assertEqual( Value2Pim().value_to_pim_entry_count( data ), 2 )
        self.assertEqual( Value2Pim().value_to_pim_entry_id( data, 0 ), 0x0001 )
        self.assertEqual( Value2Pim().value_to_pim_entry_value( data, 0 ), 0x0000000a )
        self.assertEqual( Value2Pim().value_to_pim_entry_id( data, 1 ), 0x0002 )
        self.assertEqual( Value2Pim().value_to_pim_entry_value( data, 1 ), 0x0000000b )

if __name__ == '__main__':
    unittest.main()