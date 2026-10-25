import io
import json
import mimetypes
import os

from RequestsLibrary.utils import get_multipart_file_descriptors, is_list_or_tuple, is_string_type

DEFAULT_CONTENT_TYPE = "application/octet-stream"


def _rewindable_multipart_encoder_class():
    try:
        from requests_toolbelt import MultipartEncoder
    except ImportError:
        raise ImportError(
            "Multipart data requires the requests-toolbelt package, install it with: "
            "pip install robotframework-requests[multipart]"
        )

    class RewindableMultipartEncoder(MultipartEncoder):
        """
        MultipartEncoder that can be rewound to its start, so that urllib3 retries
        and requests redirects send the whole body again instead of its remaining part.
        """

        def __init__(self, fields, boundary=None, encoding="utf-8"):
            super().__init__(fields, boundary=boundary, encoding=encoding)
            self._position = 0

        def read(self, size=-1):
            data = super().read(size)
            self._position += len(data)
            return data

        def __iter__(self):
            # requests only records the body position, needed to rewind it on redirects, for iterable bodies
            return iter(lambda: self.read(8192), b"")

        def tell(self):
            return self._position

        def seek(self, offset, whence=io.SEEK_SET):
            if offset != 0 or whence != io.SEEK_SET:
                raise io.UnsupportedOperation("Multipart data can only be rewound to its start")
            for file_descriptor in get_multipart_file_descriptors(self):
                file_descriptor.seek(0)
            self.__init__(self.fields, boundary=self.boundary_value, encoding=self.encoding)
            return 0

    return RewindableMultipartEncoder


def create_multipart_encoder(fields=None, files=None, files_first=False):
    """
    Builds a rewindable requests_toolbelt MultipartEncoder from form ``fields`` and ``files``.
    Fields are added before files, unless ``files_first`` is true, and duplicated names are preserved.
    """
    MultipartEncoder = _rewindable_multipart_encoder_class()

    field_parts = [(name, _format_field_value(value)) for name, value in _to_pairs(fields)]
    file_parts = []
    opened = []
    try:
        for file_part in _to_file_list(files):
            name, path, filename, content_type = _parse_file_part(file_part)
            file_descriptor = open(path, "rb")
            opened.append(file_descriptor)
            file_parts.append((name, (filename, file_descriptor, content_type)))
        parts = file_parts + field_parts if files_first else field_parts + file_parts
        return MultipartEncoder(fields=parts)
    except Exception:
        for file_descriptor in opened:
            file_descriptor.close()
        raise


def _to_pairs(fields):
    if not fields:
        return []
    if isinstance(fields, dict):
        return list(fields.items())
    pairs = []
    for field in fields:
        if not is_list_or_tuple(field) or len(field) != 2:
            raise ValueError(
                "Multipart fields must be a dictionary or a list of (name, value) pairs, got: %r" % (field,)
            )
        pairs.append(tuple(field))
    return pairs


def _format_field_value(value):
    if isinstance(value, (str, bytes)):
        return value
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _to_file_list(files):
    if not files:
        return []
    if isinstance(files, dict):
        files = list(files.items())
    file_list = []
    for file_part in files:
        # (name, [path, ...]) sends several files with the same name
        if is_list_or_tuple(file_part) and len(file_part) == 2 and is_list_or_tuple(file_part[1]):
            file_list.extend((file_part[0], path) for path in file_part[1])
        else:
            file_list.append(file_part)
    return file_list


def _parse_file_part(file_part):
    if isinstance(file_part, dict):
        name = file_part.get("name")
        path = file_part.get("path")
        filename = file_part.get("filename")
        content_type = file_part.get("content_type")
    elif is_list_or_tuple(file_part) and 2 <= len(file_part) <= 4:
        name, path, content_type, filename = (list(file_part) + [None, None])[:4]
    else:
        raise ValueError(
            "Multipart files must be (name, path[, content_type[, filename]]) "
            "or a dictionary with name and path keys, got: %r" % (file_part,)
        )
    if not name or not is_string_type(path):
        raise ValueError("Multipart file needs a name and a path, got: %r" % (file_part,))
    filename = filename or os.path.basename(path)
    content_type = content_type or mimetypes.guess_type(filename)[0] or DEFAULT_CONTENT_TYPE
    return name, path, filename, content_type
