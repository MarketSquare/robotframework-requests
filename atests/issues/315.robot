*** Settings ***
Library   RequestsLibrary
Resource  ../res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***
Test On Session Keyword With Verify As Parameter

    GET On Session  ${GLOBAL_SESSION}  /  verify=${False}


#Test Unverified SSL Cert With Session Verify True
#
#    Create Session  unverified_ssl  unverified-ssl-??? verify=${True}
#    Run Keyword And Expect Error  SSLError:*  GET On Session  unverified_ssl  /
#
#
#Test Unverified SSL Cert With Session Verify False And Request Override True
#
#    Create Session  unverified_ssl  unverified-ssl-??? verify=${False}
#    GET On Session  unverified_ssl  /  verify=${True}
#
#
#Test Unverified SSL Cert With Session Verify True And Request Override False
#
#    Create Session  unverified_ssl  unverified-ssl-??? verify=${True}
#    GET On Session  unverified_ssl  /  verify=${False}
