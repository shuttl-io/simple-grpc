from simple.gRPC.Fields import Fixed
import unittest

class TestFixedField(unittest.TestCase):
    def test_unmarshalls(self):
        ##Parses 32 bit correctly
        b = b'\x02\x00\x00\x00'
        f = Fixed(2)
        f.unmarshall(b)
        self.assertEquals(1, f.data)
        
        b = b'\x01\x00\x00\x00'
        f.unmarshall(b)
        self.assertEquals(-1, f.data)

        b = bytes([0x46, 0xaa, 0x25, 0x00])
        f.unmarshall(b)
        self.assertEquals(1234211, f.data)

        ##Parses 64 bit correctly
        b = b'\x02\x00\x00\x00\x00\x00\x00\x00'

        f = Fixed(2, size=64)
        f.unmarshall(b)
        self.assertEquals(1, f.data)
        
        b = b'\x01\x00\x00\x00\x00\x00\x00\x00'
        f.unmarshall(b)
        self.assertEquals(-1, f.data)

        b = bytes([0x46, 0xaa, 0x25, 0x00, 0x00, 0x00, 0x00, 0x00])
        f.unmarshall(b)
        self.assertEquals(1234211, f.data)

    def test_marshal(self):
        f = Fixed(2)
        f.data = 1
        p = f.serialize()
        self.assertEqual(4, len(p[1:]))
        self.assertEqual(b'\x02\x00\x00\x00', p[1:])

        f.data = -1
        p = f.serialize()
        self.assertEqual(4, len(p[1:]))
        self.assertEqual(b'\x01\x00\x00\x00', p[1:])

        f.data = 1234211
        p = f.serialize()
        self.assertEqual(4, len(p[1:]))
        self.assertEqual(bytes([0x46, 0xaa, 0x25, 0x00]), p[1:])

        ## Serializes 64 bits
        f = Fixed(2, size=64)
        f.data = 1
        p = f.serialize()
        self.assertEqual(8, len(p[1:]))
        self.assertEqual(b'\x02\x00\x00\x00\x00\x00\x00\x00', p[1:])

        f.data = -1
        p = f.serialize()
        self.assertEqual(8, len(p[1:]))
        self.assertEqual(b'\x01\x00\x00\x00\x00\x00\x00\x00', p[1:])

        f.data = 1234211
        p = f.serialize()
        self.assertEqual(8, len(p[1:]))
        self.assertEqual(bytes([0x46, 0xaa, 0x25, 0x00, 0x00, 0x00, 0x00, 0x00]), p[1:])