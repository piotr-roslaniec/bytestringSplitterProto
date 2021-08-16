from bytestring_splitter import VariableLengthBytestring, VersionedBytestringKwargifier, VersionedBytestringSplitter


def serializable(cls):
    splitters = getattr(cls, 'splitters', [])
    if not splitters:
        return cls
    cls.__serializable__ = True
    return cls


class DeliciousCoffee():
    def __init__(self, blend, milk_type, size):
        self.blend = blend
        self.milk_type = milk_type
        self.size = size

    def sip(self):
        return "Mmmm"


class CaffeinatedBeverage:

    def __bytes__(self):
        mybytes = b''
        for arg in self.args:
            mybytes += getattr(self, arg)
        return BeverageFactory.add_version(self, mybytes)


class OldFashionedCoffee(CaffeinatedBeverage, DeliciousCoffee):
    version = 1
    args = ['blend', 'milk_type', 'size']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blend = VariableLengthBytestring(self.blend)


class EnergyDrink(CaffeinatedBeverage):
    version = 2
    args = ['name', 'warning_label', 'active_ingredient', 'size']

    def __init__(self, name, warning_label, active_ingredient, size):
        self.name = VariableLengthBytestring(name)
        self.warning_label = VariableLengthBytestring(warning_label)
        self.active_ingredient = active_ingredient
        self.size = size


@serializable
class BeverageFactory:
    splitters = [
        VersionedBytestringKwargifier(
            OldFashionedCoffee,
            blend=VariableLengthBytestring,
            milk_type=(bytes, 13),
            size=(int, 2, {"byteorder": "big"}),
            version=1
        ),
        VersionedBytestringKwargifier(
            EnergyDrink,
            name=VariableLengthBytestring,
            warning_label=VariableLengthBytestring,
            active_ingredient=(bytes, 11),
            size=(int, 2, {"byteorder": "big"}),
            version=2
        )
    ]

    @staticmethod
    def from_bytes(some_bytes):
        version = VersionedBytestringSplitter.get_metadata(some_bytes)['version']
        return BeverageFactory.splitters[version - 1](some_bytes)

    @staticmethod
    def add_version(instance, instance_bytes):
        return BeverageFactory.splitters[instance.version - 1].assign_version(instance_bytes, instance.version)


if __name__ == '__main__':
    import beverage_pb2

    coffee = OldFashionedCoffee(b"I'm better without milk", b'local_oatmilk', int(1).to_bytes(2, byteorder="big"))

    coffee_ = beverage_pb2.OldFashionedCoffee(blend=bytes(coffee.blend), milk_type=coffee.milk_type, size=coffee.size)
    coffee_str = coffee_.SerializeToString()

    from_str_coffee = beverage_pb2.OldFashionedCoffee()
    from_str_coffee.ParseFromString(coffee_str)
    assert coffee_ == from_str_coffee

    print(coffee_str)
    print(coffee_str.hex())
