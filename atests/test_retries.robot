*** Settings ***
Library  String
Library  Collections
Library  RequestsLibrary
Resource  res_setup.robot

*** Test Cases ***
Retry Session With Wrong Retry Status List
    [Tags]  session  retry
    ${retry_status_list}=   Create List  502baaad
    Run Keyword And Expect Error  ValueError: *   Create Session  http_server  ${HTTP_LOCAL_SERVER}  retry_status_list=${retry_status_list}

Retry Session With Empty Retry Status List
    [Tags]  session  retry
    ${retry_status_list}=   Set Variable  ${Empty}
    Create Session  http_server  ${HTTP_LOCAL_SERVER}  retry_status_list=${retry_status_list}

Retry Get Request Because Of 502 Error With Default Config
    [Tags]  get  retry
    ${retry_status_list}=   Create List  502  503
    Create Session  http_server  ${HTTP_LOCAL_SERVER}  retry_status_list=${retry_status_list}
    Run Keyword And Expect Error  RetryError: *   GET On Session  http_server  /status/502

Retry Get Request Because Of 502 Error With Max Retries 1
    [Tags]  get  retry
    ${retry_status_list}=   Create List  502
    Create Session  http_server  ${HTTP_LOCAL_SERVER}  max_retries=1  retry_status_list=${retry_status_list}
    Run Keyword And Expect Error  RetryError: *   GET On Session  http_server  /status/502

Retry Disabled Get Request
    [Tags]  get  retry
    ${retry_status_list}=   Create List  502  503
    Create Session  http_server  ${HTTP_LOCAL_SERVER}  max_retries=0  retry_status_list=${retry_status_list}
    GET On Session  http_server  url=/status/502  expected_status=502

Retry Post Request Because Of 502 Error With Default Config
    [Tags]  post  retry
    ${retry_status_list}=   Create List  502
    ${retry_method_list}=   Create List  GET  POST
    Create Session  http_server  ${HTTP_LOCAL_SERVER}  retry_status_list=${retry_status_list}  retry_method_list=${retry_method_list}
    Run Keyword And Expect Error  RetryError: *   POST On Session  http_server  url=/status/502  expected_status=502

Retry Post Request Because Of 502 Error With Wrong Config
    [Tags]  post  retry
    ${retry_status_list}=   Create List  502
    ${retry_method_list}=   Create List  WRONG
    Create Session  http_server  ${HTTP_LOCAL_SERVER}  retry_status_list=${retry_status_list}  retry_method_list=${retry_method_list}
    POST On Session  http_server  url=/status/502  expected_status=502

# TODO fake the server in order to recover after a while
