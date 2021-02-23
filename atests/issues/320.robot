*** Settings ***
Library   Collections
Library   RequestsLibrary
Resource  ../res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***
Test GET with list of values as params
    ${values_list}=     Create List    1    2    3    4    5
    ${parameters}=      Create Dictionary  key  ${values_list}
    ${resp}=            GET On Session  ${GLOBAL_SESSION}  url=/anything  params=${parameters}
    Should Contain      ${resp.json()}[url]  ?key=1&key=2&key=3&key=4&key=5
    Should Be Equal     ${resp.json()}[args]  ${parameters}
