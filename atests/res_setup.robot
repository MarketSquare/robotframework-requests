*** Settings ***
Library  Process


*** Variables ***
${GLOBAL_LOCAL_SESSION}     global_local_session
${HTTP_LOCAL_SERVER}        http://localhost:5000


*** Keywords ***
Setup Flask Http Server
    ${platform}=    Evaluate    sys.platform    sys
    ${flask_cmd} =  Set Variable If
    ...  '${platform}'=='win32'  ${CURDIR}/http_server/run.cmd
    ...  ${CURDIR}/http_server/run.sh
    Start Process  ${flask_cmd}  cwd=${CURDIR}/http_server/  alias=flask
    Sleep  1  # I know... needed to let the http server start before starting the connection
    Create Session  ${GLOBAL_LOCAL_SESSION}  ${HTTP_LOCAL_SERVER}

Teardown Flask Http Server And Sessions
    Delete All Sessions
    Switch Process    flask
    Terminate Process
