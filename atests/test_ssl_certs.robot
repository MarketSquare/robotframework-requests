*** Settings ***
Library     RequestsLibrary


*** Test Cases ***
Get HTTPS & Verify Cert
    [Tags]    get    get-cert
    Create Session    sslsession    https://github.com    verify=True
    ${resp}=    GET On Session    sslsession    /
    Should Be Equal As Strings    ${resp.status_code}    200

Get HTTPS & Verify Cert with a CA bundle
    [Tags]    get    get-cert
    Create Session    sslsession    https://github.com    verify=${CURDIR}${/}cacert.pem
    ${resp}=    GET On Session    sslsession    /
    Should Be Equal As Strings    ${resp.status_code}    200

Get HTTPS with Client Side Certificates
    [Tags]    get    get-cert
    @{client_certs}=    Create List    ${CURDIR}${/}clientcert.pem    ${CURDIR}${/}clientkey.pem
    Create Client Cert Session    sslsession    https://server.cryptomix.com/secure    client_certs=@{client_certs}
    ${resp}=    GET On Session    sslsession    /
    Should Be Equal As Strings    ${resp.status_code}    200
