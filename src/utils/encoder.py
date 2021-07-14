from io import StringIO


def convert_into_bytearray(data: StringIO) -> bytes:
    content = data.getvalue()
    return content.encode('UTF-8')


def convert_into_stringio(data: bytes) -> StringIO:
    transform_to_str = str(data, 'UTF-8')
    return StringIO(transform_to_str)
