*** Settings ***
Library             RequestsLibrary
Resource            res_setup.robot

Test Setup          Setup Test Session
Test Teardown       Teardown Test Session


*** Variables ***
${test_session}     local test session created in Test Setup


*** Test Cases ***
Create a session and make sure it exists
    [Tags]    session
    Create Session    existing_session    ${HTTP_LOCAL_SERVER}
    ${exists}=    Session Exists    existing_session
    Should Be True    ${exists}

Verify a non existing session
    [Tags]    session
    ${exists}=    Session Exists    non-existing-session
    Should Not Be True    ${exists}
