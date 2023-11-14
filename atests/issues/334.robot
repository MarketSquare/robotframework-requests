*** Settings ***
Library    RequestsLibrary
Resource  ../res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***

Test evaluated response is always the one passed
    ${response_error}=  GET On Session  ${GLOBAL_SESSION}  url=/status/404    expected_status=any
    ${response_ok}=     GET On Session  ${GLOBAL_SESSION}  url=/status/200    expected_status=any
    Status Should Be    404    ${response_error}
