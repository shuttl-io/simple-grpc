import unittest
from simple.gRPC.Fields import Integer

class TestIntegerField(unittest.TestCase):

    def test_deserialize(self):
        b = bytes([0x96, 0x01])
        f = Integer(1)
        f.unmarshall(b)
        self.assertEqual(150, f.data)

        b = bytes([0b10101100, 0b00000010])
        f.unmarshall(b)
        self.assertEqual(300, f.data)

        b = bytes([0xfa, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x01])
        f.unmarshall(b)
        self.assertEqual(-6, f.data)

    def test_serializing(self):
        b = bytes([0x08, 0x96, 0x01])
        f = Integer(1)
        f.data = 150
        self.assertEqual(b, f.serialize())

        b = bytes([0x08, 0b10101100, 0b00000010])
        f.data = 300
        self.assertEqual(b, f.serialize())

        b = bytes([0x08, 0xfa, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x01])
        f.data = -6
        self.assertEqual(b, f.serialize())
