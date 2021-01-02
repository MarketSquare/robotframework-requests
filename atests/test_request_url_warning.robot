*** Settings ***
Library  Collections
Library  String
Library  RequestsLibrary
Resource  res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***

Named URL with = symbol should not have warnings
   GET On Session  ${GLOBAL_SESSION}  url=/anything?a=a&b=b

Positional URL with = symbol
   Run Keyword And Expect Error   TypeError:*  GET On Session  ${GLOBAL_SESSION}  /anything?a=a&b=b

Positional URL with '' should not have warnings
   GET On Session  ${GLOBAL_SESSION}  ${Empty}

Positional URL with None should not have warnings
   GET On Session  ${GLOBAL_SESSION}  ${None}

