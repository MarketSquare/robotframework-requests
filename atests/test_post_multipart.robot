*** Settings ***
Library     RequestsLibrary


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
