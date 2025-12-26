*** Settings ***
Library     RequestsLibrary
Library     customAuthenticator.py
Resource    res_setup.robot
Variables   secretvar.py

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
    ${auth}=    Create List    user    passwd
    Create Digest Session
    ...    authsession
    ...    ${HTTP_LOCAL_SERVER}
    ...    auth=${auth}
    ...    debug=3
    ${resp}=    GET On Session    authsession    /digest-auth/auth/user/passwd
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Be Equal As Strings    ${resp.json()['authenticated']}    True

Get With Auth with Robot Secrets
    [Tags]     robot-74    get    get-cert
    Skip If    $SECRET_PASSWORD == "not-supported"
    ...    msg=robot version does not support secrets
    ${auth}=    Create List    user     ${SECRET_PASSWORD}
    Create Session    authsession    ${HTTP_LOCAL_SERVER}    auth=${auth}
    ${resp}=    GET On Session    authsession    /basic-auth/user/secret_passwd
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Be Equal As Strings    ${resp.json()['authenticated']}    True

Get With Digest Auth with Robot Secrets
    [Tags]    robot-74    get    get-cert
    Skip If    $SECRET_PASSWORD == "not-supported"
    ...    msg=robot version does not support secrets
    ${auth}=    Create List    user    ${SECRET_PASSWORD}
    Create Digest Session
    ...    authsession
    ...    ${HTTP_LOCAL_SERVER}
    ...    auth=${auth}
    ...    debug=3
    ${resp}=    GET On Session    authsession    /digest-auth/auth/user/secret_passwd
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Be Equal As Strings    ${resp.json()['authenticated']}    True

Session-less GET With Auth with Robot Secrets
    [Tags]    robot-74    get    get-cert    session-less
    Skip If    $SECRET_PASSWORD == "not-supported"
    ...    msg=robot version does not support secrets
    ${auth}=    Create List    user    ${SECRET_PASSWORD}
    ${resp}=    GET    ${HTTP_LOCAL_SERVER}/basic-auth/user/secret_passwd    auth=${auth}
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Be Equal As Strings    ${resp.json()['authenticated']}    True
