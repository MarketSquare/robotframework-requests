*** Settings ***
Library     RequestsLibrary
Library     customAuthenticator.py
Resource    res_setup.robot


*** Test Cases ***
Get With Auth
    [Tags]    get    get-cert
    ${auth}=    Create List    user    passwd
    Create Session    authsession    ${HTTP_LOCAL_SERVER}    auth=${auth}
    ${resp}=    GET On Session    authsession    /basic-auth/user/passwd
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Be Equal As Strings    ${resp.json()['authenticated']}    True

Get With Custom Auth
    [Tags]    get
    ${auth}=    Get Custom Auth    user    passwd
    Create Custom Session    authsession    ${HTTP_LOCAL_SERVER}    auth=${auth}
    ${resp}=    GET On Session    authsession    /basic-auth/user/passwd
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Be Equal As Strings    ${resp.json()['authenticated']}    True

Get With Digest Auth
    [Tags]    get    get-cert
    ${auth}=    Create List    user    pass
    Create Digest Session
    ...    authsession
    ...    ${HTTP_LOCAL_SERVER}
    ...    auth=${auth}
    ...    debug=3
    ${resp}=    GET On Session    authsession    /digest-auth/auth/user/pass
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Be Equal As Strings    ${resp.json()['authenticated']}    True
