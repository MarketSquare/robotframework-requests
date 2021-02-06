*** Settings ***
Library   RequestsLibrary
Resource  ../res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***
Test On Session Keyword With Verify As Parameter

    GET On Session  ${GLOBAL_SESSION}  /  verify=${False}
