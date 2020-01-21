*** Settings ***
Library  Process


*** Variables ***
${GLOBAL_LOCAL_SESSION}     global_local_session
${HTTP_LOCAL_SERVER}        http://localhost:5000


*** Keywords ***
Setup Flask Http Server
    Start Process  ${CURDIR}/http_server/run.sh  cwd=${CURDIR}/http_server/  alias=flask
    Sleep  1  # I know... needed to let the http server start before starting the connection
    Create Session  global_local_session  ${HTTP_LOCAL_SERVER}

Teardown Flask Http Server And Sessions
    Delete All Sessions
    Terminate All Processes    kill=True
