*** Settings ***
Library  Process
Library  RequestsLibrary


*** Variables ***
${GLOBAL_SESSION}       global_session
${HTTP_LOCAL_SERVER}    http://localhost:5010


*** Keywords ***

Setup acceptance test suite
    Setup Flask Http Server
    Create Session  ${GLOBAL_SESSION}  ${HTTP_LOCAL_SERVER}

Teardown acceptance test suite
    Delete All Sessions
    Switch Process    flask
    Terminate Process

Setup Flask Http Server
    ${platform}=    Evaluate    sys.platform    sys
    ${flask_cmd} =  Set Variable If
    ...  '${platform}'=='win32'  ${CURDIR}/http_server/run.cmd
    ...  ${CURDIR}/http_server/run.sh
    # No way to have the return code or other data on the process since it's in background
    Start Process  ${flask_cmd}  cwd=${CURDIR}/http_server/  alias=flask
    Create Session  ${GLOBAL_SESSION}  ${HTTP_LOCAL_SERVER}
    Wait Until Http Server Is Up And Running

Wait Until Http Server Is Up And Running
    Create Session  wait-until-up  ${HTTP_LOCAL_SERVER}  max_retries=10
    Get On Session  wait-until-up  /


