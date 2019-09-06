*** Settings ***
Library  String
Library  Collections
Library  ../src/RequestsLibrary/RequestsKeywords.py

Suite Teardown  Delete All Sessions

*** Test Cases ***
Retry Session With Wrong Retry Status List
    [Tags]  session  retry
    ${retry_status_list}=   Create List  502baaad
    Run Keyword And Expect Error  ValueError: *   Create Session  httpbin  http://httpbin.org  retry_status_list=${retry_status_list}

Retry Session With Empty Retry Status List
    [Tags]  session  retry
    ${retry_status_list}=   Set Variable  ${Empty}
    Create Session  httpbin  http://httpbin.org  retry_status_list=${retry_status_list}

Retry Get Request Because Of 502 Error With Default Config
    [Tags]  get  retry
    ${retry_status_list}=   Create List  502  503
    Create Session  httpbin  http://httpbin.org  retry_status_list=${retry_status_list}
    Run Keyword And Expect Error  RetryError: *   Get Request  httpbin  /status/502

Retry Get Request Because Of 502 Error With Max Retries 1
    [Tags]  get  retry
    ${retry_status_list}=   Create List  502
    Create Session  httpbin  http://httpbin.org  max_retries=1  retry_status_list=${retry_status_list}
    Run Keyword And Expect Error  RetryError: *   Get Request  httpbin  /status/502

Retry Disabled Get Request
    [Tags]  get  retry
    ${retry_status_list}=   Create List  502  503
    Create Session  httpbin  http://httpbin.org  max_retries=0  retry_status_list=${retry_status_list}
    Get Request  httpbin  /status/502
