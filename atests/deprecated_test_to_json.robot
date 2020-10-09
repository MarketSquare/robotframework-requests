*** Settings ***
Library  Collections
Library  RequestsLibrary
Resource  res_setup.robot

Suite Setup     Run Keywords  Setup Flask Http Server
...             Setup Response For Json Tests
Suite Teardown  Teardown Flask Http Server And Sessions

*** Variables ***
${resp}         created in the setup
&{dict_params}  key_one=true    key_two=this is a test string

*** Test Cases ***

Do Not Pretty Print a JSON object
    [Tags]    json
    ${jsondata}=    To Json    ${resp.content}
    Dictionaries Should Be Equal   ${jsondata['args']}    ${dict_params}

Pretty Print a JSON object
    [Tags]    json
    Comment    Define json variable.
    ${output}=    To Json    ${resp.content}    pretty_print=True
    Should Contain    ${output}    "key_one": "true"
    Should Contain    ${output}    "key_two": "this is a test string"
    Should Not Contain    ${output}    {u'key_two': u'this is a test string', u'key_one': u'true'}

Set Pretty Print to non-Boolean value
    [Tags]    json
    Comment    Define json variable.
    ${output}=    To Json    ${resp.content}    pretty_print="Hello"
    Log    ${output}
    Should Contain    ${output}    "key_one": "true"
    Should Contain    ${output}    "key_two": "this is a test string"
    Should Not Contain    ${output}    {u'key_two': u'this is a test string', u'key_one': u'true'}

*** Keywords ***

Setup Response For Json Tests
    ${resp}=   GET On Session    ${GLOBAL_SESSION}    /anything    params=${dict_params}
    Set Suite Variable  ${resp}
