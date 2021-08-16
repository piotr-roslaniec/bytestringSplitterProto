package_template = """
syntax = "proto2";

package {package};

{messages}
"""

message_template = """
message {name} {{
{fields}
}}\n
"""


def generate_proto(messages):
    messages_str = ""
    for msg in messages:
        fields_str = ""
        for i, field in enumerate(msg['fields']):
            name, type_ = field
            if type_ not in [
                'bytes',
                # 'int32'
            ]:
                raise ValueError(f'Unknown field type {type_}')
            f = f"\trequired {type_} {name} = {i + 1};\n"
            fields_str += f

        m = message_template.format(name=msg['name'], fields=fields_str)
        messages_str += m

    return package_template.format(package='coffee', messages=messages_str)


if __name__ == '__main__':
    messages = [
        {'name': 'test', 'fields': [
            ('test_bytes', 'bytes'),
            # ('test_int', 'int32')
        ]}
    ]
    p = generate_proto(messages)
