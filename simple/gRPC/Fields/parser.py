HAS_MORE_BYTES = 0x80
IS_NEGATIVE = 0x8000000000000000
NEGATE = 0xffffffffffffffff
REMOVE_FIRST_BIT = 0b01111111

class ByteStream:
    def __init__(self, stream):
        self.rawStream = stream
        self.index = 0
        pass
    
    def pop(self):
        data = self.rawStream[self.index]
        self.index += 1
        return data

    def rewind(self, by=-1):
        self.index -= by
        pass

    def reset(self):
        self.index = 0
        pass
    
    def peek(self):
        return self.rawStream[self.index]

    def at(self, ndx):
        return self.rawStream[ndx]

    def done(self):
        return self.index == len(self.rawStream)

class Parser:
    '''
    A note on the silly names:
        the functions are called parseWireX because protobufs use a single type for 
        multiple "types". For example, protobuf wiretype 2 can refer to either a 
        string, a JSON blob, or an embedded message. It is up to the Message object 
        that instantiated the parser to reconsitute the parsed message into its correct
        field. 
    '''
    def __init__(self, stream):
        self.stream = ByteStream(stream)
        pass

    def parse(self):
        parsedMessage = dict()
        while not self.stream.done():
            firstByte = self.stream.pop()
            index = firstByte >> 3
            tp = firstByte & 0b111
            parseFunc = getattr(self, "parseWire" + str(tp), None)
            if parseFunc is None:
                raise NotImplementedError("Wire type " + str(tp) + " is not implmented")
            parsedData = parseFunc()
            if index in parsedMessage:
                raise ValueError("index appears in message twice: "+ index)
            parsedMessage[index] = parsedData
        return parsedMessage

    def parseWire0(self):
        num = 0
        b = HAS_MORE_BYTES
        chunk = []
        index = 0 
        while b & HAS_MORE_BYTES:
            b = self.stream.pop()
            chunk.append(b & REMOVE_FIRST_BIT)
        return bytes(chunk)
        #    currVal = (b & 0b01111111) 
        #    num |= currVal << index
        #    index += 7 
        #if num & IS_NEGATIVE:
        #    num = -((num ^ NEGATE) + 1)
        #    pass
        #return num
    
    def parseWire1(self):
        chunk = []
        for i in range(8):
            b = self.stream.pop()
            chunk.append(b)
            pass
        return chunk
        pass

    def parseWire2(self):
        data = []
        l = self.stream.pop()
        for _ in range(l):
            data.append(self.stream.pop())
            pass
        return bytes(data)

    def parseWire5(self):
        chunk = []
        for _ in range(4):
            chunk.append(self.stream.pop())
        return chunk
        pass
