*** Settings ***
Library     RequestsLibrary
Library     OperatingSystem


*** Test Cases ***
Test Post Dictionary On Session Multipart
    ${file_1}=    Get File For Streaming Upload    atests/randombytes.bin
    ${file_2}=    Get File For Streaming Upload    atests/randombytes.bin
    ${files}=    Create Dictionary    randombytes1    ${file_1}    randombytes2    ${file_2}

    Should Not Be True    ${file_1.closed}
    Should Not Be True    ${file_2.closed}

    ${resp}=    POST On Session    ${GLOBAL_SESSION}    /anything    files=${files}

    Should Be True    ${file_1.closed}
    Should Be True    ${file_2.closed}

    Should Contain    ${resp.json()}[headers][Content-Type]    multipart/form-data; boundary=
    Should Contain    ${resp.json()}[headers][Content-Length]    480
    Should Contain    ${resp.json()}[files]    randombytes1
    Should Contain    ${resp.json()}[files]    randombytes2

Test Post List On Session Multipart
    ${file_1}=    Get File For Streaming Upload    atests/randombytes.bin
    ${file_2}=    Get File For Streaming Upload    atests/randombytes.bin
    ${file_1_tuple}=    Create List     file1.bin   ${file_1}
    ${file_2_tuple}=    Create List     file2.bin   ${file_2}
    ${file_1_upload}=    Create List    randombytes    ${file_1_tuple}
    ${file_2_upload}=    Create List    randombytes    ${file_2_tuple}
    ${files}=    Create List    ${file_1_upload}    ${file_2_upload}

    Should Not Be True    ${file_1.closed}
    Should Not Be True    ${file_2.closed}

    ${resp}=    POST On Session    ${GLOBAL_SESSION}    /anything    files=${files}

    Should Be True    ${file_1.closed}
    Should Be True    ${file_2.closed}

    Should Contain    ${resp.json()}[headers][Content-Type]    multipart/form-data; boundary=
    Should Contain    ${resp.json()}[headers][Content-Length]    466
    Should Contain    ${resp.json()}[files]    randombytes
    Length Should Be    ${resp.json()}[files][randombytes]    2

Test Post Multipart Data With Fields And Files On Session
    ${settings}=    Create Dictionary    everything=${True}
    ${fields}=    Create Dictionary    action=add    settings=${settings}
    ${files}=    Create Dictionary    document=${CURDIR}${/}data.json
    ${multipart}=    Create Multipart Data    fields=${fields}    files=${files}
    ${file}=    Set Variable    ${multipart.fields}[2][1][1]

    Should Not Be True    ${file.closed}

    ${resp}=    POST On Session    ${GLOBAL_SESSION}    /anything    data=${multipart}

    Should Be True    ${file.closed}
    Should Be Equal    ${resp.json()}[headers][Content-Type]    ${multipart.content_type}
    Should Be Equal    ${resp.json()}[form][action]    add
    Should Be Equal    ${resp.json()}[form][settings]    {"everything": true}
    # raw bytes: Get File would turn the CRLF line endings of a Windows checkout into LF
    ${expected}=    Get Binary File    ${CURDIR}${/}data.json
    Should Be Equal    ${resp.json()}[files][document]    ${expected.decode('utf-8')}

Test Put Multipart Data With Repeated Fields And Files On Session
    ${tag_1}=    Create List    tag    one
    ${tag_2}=    Create List    tag    two
    ${fields}=    Create List    ${tag_1}    ${tag_2}
    ${file_1}=    Create List    attachments    ${CURDIR}${/}data.json
    ${file_2}=    Create List    attachments    ${CURDIR}${/}index.html    text/html    renamed.html
    ${files}=    Create List    ${file_1}    ${file_2}
    ${multipart}=    Create Multipart Data    fields=${fields}    files=${files}

    ${resp}=    PUT On Session    ${GLOBAL_SESSION}    /anything    data=${multipart}

    Should Contain    ${resp.json()}[headers][Content-Type]    multipart/form-data; boundary=
    Should Be Equal    ${resp.json()}[form][tag]    ${{['one', 'two']}}
    Length Should Be    ${resp.json()}[files][attachments]    2

Test Post Large Multipart Data With Fields
    ${large_file}=    Set Variable    ${OUTPUT_DIR}${/}large_multipart.bin
    Create Binary File    ${large_file}    ${{os.urandom(50000)}}
    ${fields}=    Create Dictionary    name=large
    ${files}=    Create Dictionary    file=${large_file}
    ${multipart}=    Create Multipart Data    fields=${fields}    files=${files}

    ${resp}=    POST    ${HTTP_LOCAL_SERVER}/anything    data=${multipart}

    Should Be Equal    ${resp.json()}[form][name]    large
    Should Be True    int($resp.json()['headers']['Content-Length']) > 50000
    [Teardown]    Remove File    ${large_file}

Test Post Multipart Data Keeps Explicit Content Type
    ${files}=    Create Dictionary    document=${CURDIR}${/}data.json
    ${multipart}=    Create Multipart Data    files=${files}
    ${headers}=    Create Dictionary    Content-Type=${multipart.content_type}; charset=utf-8

    ${resp}=    POST On Session    ${GLOBAL_SESSION}    /anything    data=${multipart}    headers=${headers}

    Should Be Equal    ${resp.json()}[headers][Content-Type]    ${multipart.content_type}; charset=utf-8

Test Post Multipart Data With Files First And A List Of Paths
    ${fields}=    Create Dictionary    action=add
    ${paths}=    Create List    ${CURDIR}${/}data.json    ${CURDIR}${/}index.html
    ${attachments}=    Create List    attachments    ${paths}
    ${files}=    Create List    ${attachments}
    ${multipart}=    Create Multipart Data    fields=${fields}    files=${files}    files_first=${True}

    Should Be Equal    ${multipart.fields}[0][0]    attachments
    Should Be Equal    ${multipart.fields}[1][0]    attachments
    Should Be Equal    ${multipart.fields}[2][0]    action

    ${resp}=    POST On Session    ${GLOBAL_SESSION}    /anything    data=${multipart}

    Should Be Equal    ${resp.json()}[form][action]    add
    Length Should Be    ${resp.json()}[files][attachments]    2

Test Post Multipart Data Keeps Session Headers
    ${session_headers}=    Create Dictionary    Authorization=Bearer some-token    Content-Type=application/json
    Create Session    bearer_session    ${HTTP_LOCAL_SERVER}    headers=${session_headers}
    ${files}=    Create Dictionary    document=${CURDIR}${/}data.json
    ${multipart}=    Create Multipart Data    files=${files}

    ${resp}=    POST On Session    bearer_session    /anything    data=${multipart}

    Should Be Equal    ${resp.json()}[headers][Authorization]    Bearer some-token
    Should Be Equal    ${resp.json()}[headers][Content-Type]    ${multipart.content_type}

Test Post Multipart Data Is Sent Whole Again After A 307 Redirect
    ${fields}=    Create Dictionary    action=add
    ${files}=    Create Dictionary    document=${CURDIR}${/}data.json
    ${multipart}=    Create Multipart Data    fields=${fields}    files=${files}

    ${resp}=    POST On Session    ${GLOBAL_SESSION}    /redirect-to    params=url=/anything&status_code=307    data=${multipart}

    Should Be Equal As Strings    ${resp.history[0].status_code}    307
    Should Be Equal    ${resp.json()}[form][action]    add
    ${expected}=    Get Binary File    ${CURDIR}${/}data.json
    Should Be Equal    ${resp.json()}[files][document]    ${expected.decode('utf-8')}

Test Post Multipart Data With Files Described By Dictionaries
    ${file}=    Create Dictionary    name=document    path=${CURDIR}${/}data.json
    ...    filename=renamed.json    content_type=application/json
    ${files}=    Create List    ${file}
    ${fields}=    Create Dictionary    count=${3}
    ${multipart}=    Create Multipart Data    fields=${fields}    files=${files}

    Should Be Equal    ${multipart.fields}[1][1][0]    renamed.json
    Should Be Equal    ${multipart.fields}[1][1][2]    application/json

    ${resp}=    POST On Session    ${GLOBAL_SESSION}    /anything    data=${multipart}

    Should Be Equal    ${resp.json()}[form][count]    3
    ${expected}=    Get Binary File    ${CURDIR}${/}data.json
    Should Be Equal    ${resp.json()}[files][document]    ${expected.decode('utf-8')}

Test Create Multipart Data Fails Clearly With Invalid Arguments
    Run Keyword And Expect Error    ValueError: Multipart fields must be a dictionary or a list of (name, value) pairs*
    ...    Create Multipart Data    fields=${{["not a pair"]}}
    Run Keyword And Expect Error    ValueError: Multipart files must be (name, path*
    ...    Create Multipart Data    files=${{[("document",)]}}
    Run Keyword And Expect Error    ValueError: Multipart file needs a name and a path*
    ...    Create Multipart Data    files=${{[{"name": "document"}]}}
    ${existing}=    Create List    document    ${CURDIR}${/}data.json
    ${missing}=    Create List    missing    ${CURDIR}${/}does_not_exist.bin
    Run Keyword And Expect Error    FileNotFoundError: *does_not_exist.bin*
    ...    Create Multipart Data    files=${{[$existing, $missing]}}
