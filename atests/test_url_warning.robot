*** Settings ***
Library  Collections
Library  String
Library  RequestsLibrary
Resource  res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***

On Session Named URL with = symbol should not have warnings
   GET On Session  ${GLOBAL_SESSION}  url=/anything?a=a&b=b

On Session Positional URL with = symbol
   Run Keyword And Expect Error   TypeError:*  GET On Session  ${GLOBAL_SESSION}  /anything?a=a&b=b

On Session Positional URL with '' should not have warnings
   GET On Session  ${GLOBAL_SESSION}  ${Empty}

On Session Positional URL with None should not have warnings
   GET On Session  ${GLOBAL_SESSION}  ${None}

Session Less Named URL with = symbol should not have warnings
   GET  url=${HTTP_LOCAL_SERVER}/anything?a=a&b=b

Session Less Positional URL with = symbol
   Run Keyword And Expect Error   TypeError:*  GET  ${HTTP_LOCAL_SERVER}/anything?a=a&b=b

Session Less Positional URL with '' should not have warnings
   GET  ${HTTP_LOCAL_SERVER}/${Empty}

