from .parser import Parser, HAS_MORE_BYTES, IS_NEGATIVE, NEGATE

class Field:
    Type = -1

    def __init__(self, index):
        self.index = index
        self.data = None
        pass

    @classmethod
    def FromMessage(cls, index, data):
        f = cls(index)
        f.unmarshall(data)
        return f
    
    def serialize(self):
        d = self._serialize()
        msg = bytes([(self.index << 3) | self.Type, *d])
        return msg
    
    def _serialize(self):
        raise NotImplementedError()

    def unmarshall(self, data):
        raise NotImplementedError()

class String(Field):
    Type = 2

    def _serialize(self):
        lenStr = len(self.data)
        return bytes([lenStr, *self.data.encode("utf-8")])
    
    def unmarshall(self, data):
        self.data = data.decode("utf-8")
        pass

class Integer(Field):
    Type = 0

    def _handleNegative(self):
        num = self.data
        self.data = -((num ^ NEGATE)) - 1
        return self._serialize()

    def _serialize(self):
        if self.data < 0:
            return self._handleNegative()
        FULL = 0xFF
        num = self.data
        index = 0
        data = list() 
        while num & FULL:
            currentNum = (num >> index) & (FULL)
            num >>= (index + 1) * 7
            if num & FULL:
                currentNum |= HAS_MORE_BYTES
                pass
            data.append(currentNum)
        return data 

    def unmarshall(self, data):
        b = HAS_MORE_BYTES
        num = 0
        index = 0
        while b & HAS_MORE_BYTES:
            b = data[index]
            currVal = (b & 0b01111111)
            num |= currVal << index * 7
            index += 1
        if num & IS_NEGATIVE:
            num = -((num ^ NEGATE) + 1)
            pass
        self.data = num

class Fixed(Field):
    def __init__(self, index, size=32, signed=True):
        super().__init__(index)
        self.size = size
        self.signed = signed
        self.Type = 1 if size == 64 else 5
        pass
    
    def unmarshall(self, data):
        self.data = int.from_bytes(data, "little", signed=False)
        if self.signed:
            self.data = (self.data >> 1) ^ -(self.data & 1)

    def _serialize(self):
        num = self.data
        if self.signed:
            num = (self.data << 1) ^ (self.data >> self.size -1)
        return num.to_bytes(self.size // 8, "little", signed=False)