*** Settings ***
Library  RequestsLibrary
Resource  res_setup.robot

*** Test Cases ***
Create a session and make sure it exists
    [Tags]    session
    Create Session     existing_session  ${HTTP_LOCAL_SERVER}
    ${exists}=         Session Exists    existing_session
    Should Be True     ${exists}

Verify a non existing session
    [Tags]    session
    ${exists}=          Session Exists    non-existing-session
    Should Not Be True  ${exists}
