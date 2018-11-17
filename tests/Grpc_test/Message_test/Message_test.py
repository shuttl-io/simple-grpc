import unittest
from simple.gRPC.Message import Message
from simple.gRPC.Fields import String, Integer


class TestMessage(Message):
    testMessage = String(1)
    testInteger = Integer(2)


class MessageTest(unittest.TestCase):
    def test_message_works(self):
        self.assertTrue(TestMessage.fields is not None)
        print(TestMessage.fields)
        print(TestMessage.field_names)
        msg = TestMessage()
        print(msg.field_names)
        msg.testMessage = "name"
        self.assertEqual("name", msg.testMessage.data)
        pass
