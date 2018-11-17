import unittest
from simple.gRPC.Fields import String

class TestStringField(unittest.TestCase):
    def test_serializes_correctly(self):
        stringVal = String(2)
        stringVal.data = "testing"
        serialized = stringVal.serialize()
        self.assertEqual(bytes([0x12, 0x07, 0x74, 0x65, 0x73, 0x74, 0x69, 0x6e, 0x67]), serialized)
    
    def test_unserializes_correctly(self):
        stringVal = String(2)
        stringVal.unmarshall(bytes([0x74, 0x65, 0x73, 0x74, 0x69, 0x6e, 0x67]))
        self.assertEqual(stringVal.data, "testing")
        pass
