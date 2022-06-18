*** Settings ***
Library  Collections
Library  String
Library  RequestsLibrary

*** Test Cases ***

Get HTTPS & Verify Cert
    [Tags]  get     get-cert
    Create Session    httpbin    https://httpbin.org   verify=True
    ${resp}=  GET On Session  httpbin  /get
    Should Be Equal As Strings  ${resp.status_code}  200

Get HTTPS & Verify Cert with a CA bundle
    [Tags]  get     get-cert
    Create Session    httpbin    https://httpbin.org   verify=${CURDIR}${/}cacert.pem
    ${resp}=  GET On Session  httpbin  /get
    Should Be Equal As Strings  ${resp.status_code}  200

Get HTTPS with Client Side Certificates
    [Tags]  get     get-cert
    @{client_certs}=    Create List     ${CURDIR}${/}clientcert.pem     ${CURDIR}${/}clientkey.pem
    Create Client Cert Session  crtsession  https://server.cryptomix.com/secure     client_certs=@{client_certs}
    ${resp}=    GET On Session     crtsession  /
    Should Be Equal As Strings  ${resp.status_code}     200
