#!/usr/bin/env bash
# I know it's bad but there is no other way to keep docstring working with this decorator
SCRIPT_PATH=`dirname "$0"`
sed -i.bak '/@warn_if_equal_symbol_in_url/d' ${SCRIPT_PATH}/../src/RequestsLibrary/RequestsOnSessionKeywords.py
python -m robot.libdoc ${SCRIPT_PATH}/../src/RequestsLibrary ${SCRIPT_PATH}/RequestsLibrary.html
mv ${SCRIPT_PATH}/../src/RequestsLibrary/RequestsOnSessionKeywords.py.bak ${SCRIPT_PATH}/../src/RequestsLibrary/RequestsOnSessionKeywords.py
