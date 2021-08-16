import inspect

import coffee
from proto import generate_proto


def run():
    messages = []
    for name, data in inspect.getmembers(coffee):
        if not getattr(data, '__serializable__', False):
            continue

        for splitter in data.splitters:
            fields = []
            for (param_name, param_type) in splitter.message_parameters:
                print(param_name, param_type)
                # if type(param_type) is tuple:
                #     param_type = param_type[0]
                # if param_type == VariableLengthBytestring or param_type == bytes:
                #     field_type = 'bytes'
                # elif param_type == int:
                #     field_type = 'int32'
                # else:
                #     field_type = None
                field_type = 'bytes'
                fields.append((param_name, field_type))

            msg_name = splitter.receiver.__name__
            m = {'name': msg_name, 'fields': fields}
            messages.append(m)
            print(m)

    p = generate_proto(messages)
    with open("beverage.proto", "w") as f:
        f.write(p)


if __name__ == '__main__':
    run()
