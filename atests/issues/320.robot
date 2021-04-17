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

Test GET with spaces in dictionary as params
    ${parameters}=      Create Dictionary  key  v a l u e
    ${resp}=            GET On Session  ${GLOBAL_SESSION}  url=/anything  params=${parameters}
    Should Be Equal     ${resp.json()}[args]  ${parameters}

Test GET with spaces in string as params
    ${parameters}=      Create Dictionary
    ${resp}=            GET On Session  ${GLOBAL_SESSION}  url=/anything  params=key=v a l u e
    Should Contain      ${resp.json()}[url]  v%20a%20l%20u%20e
