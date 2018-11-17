from ..Fields import Field
from ..Fields import Parser

class MessageBase(type):
    def __new__(cls,  name, bases, attrs, **kwargs):
        super_new = super().__new__#_(name, bases, attrs, **kwargs)
        parents = [b for b in bases if isinstance(b, MessageBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)
        new_class = super_new(cls, name, bases, attrs)
        new_class.GRPC_NAME = attrs.pop("GRPC_NAME", None) or name
        new_class.fields = {}
        new_class.field_names = dict()
        print(attrs)
        for name, field in attrs.items():
            if issubclass(type(field), Field):
                field.name = name
                new_class.fields[field.index] = field
                new_class.field_names[field.name] = field
                pass
        #print(inspect.getmembers(new_class, lambda field: issubclass(type(field), Field)))
        return new_class

class Message(metaclass=MessageBase):

    def __init__(self):
        print (self.__dict__)
        pass

    @classmethod
    def FromProto(cls, bytez):
        msg = cls()
        parser = Parser(bytez)
        fields = parser.parse()
        for index, data in fields.items():
            msg.field_names[cls.field[index]].unmarshal(data)
            pass
        return msg

    def ToProto(self):
        data = []
        for _, field in self.fields.items():
            data.extend(field.serialize())
            pass
        return data

    @classmethod
    def Form(cls, **kwargs):
        msg = cls()
        for fieldName, value in kwargs.items():
            field = msg.field_names.get(fieldName)#getattr(msg, fieldName)
            if field is None:
                raise ValueError(fieldName + "no field with that name found")
            field.data = value
            msg.field_names[fieldName] = field
            pass
        return msg

    def __setattr__(self, name, value):
        print("setting")
        field = self.field_name.get(name)
        if isinstance(field, Field):
            field.data = value
            self.field_names[name] = field
            return
        self.__dict__[name] = value

    def __getattr__(self, name):
        print("getting")
        if name in self.field_names:
            return self.field_names[name]
        return self.__dict__[name]
