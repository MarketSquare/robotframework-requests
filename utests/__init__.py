import os
import sys


PY3 = sys.version_info > (3,)
SCRIPT_DIR = os.path.dirname(__file__)

if PY3:
    from unittest import mock  # noqa
else:
    import mock  # noqa

