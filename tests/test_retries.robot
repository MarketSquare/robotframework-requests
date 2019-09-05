*** Settings ***
Library  String
Library  Collections
Library  ../src/RequestsLibrary/RequestsKeywords.py

Suite Teardown  Delete All Sessions

*** Test Cases ***
Retry Get Request Because Of 502 Error
    [Tags]  get  retry
    ${retry_status_list}=   Create List  502
    Create Session  httpbin  http://httpbinf.org  debug=1  retry_status_list=${retry_status_list}
    Run Keyword And Expect Error  RetryError: *   Get Request  httpbin  /status/502



