import unittest
from simple.gRPC.Fields import Parser, REMOVE_FIRST_BIT

class TesParser(unittest.TestCase):
    def test_parse_string(self):
        data = bytes([0x12, 0x07, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6e, 0x67])
        p = Parser(data)
        fields = p.parse()
        self.assertTrue(2 in fields)
        self.assertEqual(bytes([0x74, 0x65, 0x73, 0x74, 0x69, 0x6e, 0x67]), fields[2])
        pass

    def test_parse_varint(self):
        def rFirstBit(bytearray: bytes):
            return bytes([b &REMOVE_FIRST_BIT for b in bytearray])

        data = bytes([0x08, 0x96, 0x01])
        p = Parser(data)
        fields = p.parse()
        self.assertTrue(1 in fields)
        self.assertEqual(rFirstBit(data[1:]), fields[1])
        data = bytes([0x08, 0b10101100, 0b00000010])
        p = Parser(data)
        fields = p.parse()
        self.assertEqual(rFirstBit(data[1:]), fields[1])

        data = bytes([0x08, 0xfa, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x01])
        p = Parser(data)
        fields = p.parse()
        self.assertEqual(rFirstBit(data[1:]), fields[1])

    def test_parse_type_1(self):
        d = [(1 << 3 | 1), 0x33, 0x56, 0x12, 0x54, 0x45, 0xfa, 0x43, 0xba, (2 << 3), 0x00] 
        data = bytes(d)
        p = Parser(data)
        fields = p.parse()
        self.assertEqual(d[1:-2], fields[1])
        pass

    def test_parse_type_5(self):
        d = [(1 << 3 | 5), 0x33, 0x56, 0x12, 0x54, (2 << 3), 0x00] 
        data = bytes(d)
        p = Parser(data)
        fields = p.parse()
        self.assertEqual(d[1:-2], fields[1])
        pass
