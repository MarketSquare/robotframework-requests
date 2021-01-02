*** Settings ***
Library   RequestsLibrary
Resource  res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***
Get Request With Default Redirection
    [Tags]  get
    ${resp}=  Get Request  ${GLOBAL_SESSION}  /redirect-to?url=anything
    Status Should Be  OK  ${resp}
    Length Should Be  ${resp.history}  1

Get Request With Redirection
    [Tags]  get
    ${resp}=  Get Request  ${GLOBAL_SESSION}  /redirect-to?url=anything  allow_redirects=${true}
    Status Should Be  OK  ${resp}
    Length Should Be  ${resp.history}  1

Get Request Without Redirection
    [Tags]  get
    ${resp}=  Get Request  ${GLOBAL_SESSION}  /redirect-to?url=anything  allow_redirects=${false}
    Status Should Be  302  ${resp}
    Length Should Be  ${resp.history}  0

# TODO understand whether this is the right behavior or not
Options Request Without Redirection By Default
    [Tags]  options
    ${resp}=  Options Request  ${GLOBAL_SESSION}  /redirect-to?url=anything
    Status Should Be  OK  ${resp}
    Length Should Be  ${resp.history}  0

# TODO understand whether this is the right behavior or not
Options Request With Redirection
    [Tags]  options
    ${resp}=  Options Request  ${GLOBAL_SESSION}  /redirect-to?url=anything  allow_redirects=${true}
    Status Should Be  OK  ${resp}
    Length Should Be  ${resp.history}  0

Head Request With Redirection
    [Tags]  head
    ${resp}=  Head Request  ${GLOBAL_SESSION}  /redirect-to?url=anything  allow_redirects=${true}
    Status Should Be  OK  ${resp}
    Length Should Be  ${resp.history}  1

Head Request Without Redirection By Default
    [Tags]  head
    ${resp}=  Head Request  ${GLOBAL_SESSION}  /redirect-to?url=anything
    ${status}=  Convert To String  ${resp.status_code}
    Status Should Be  302  ${resp}
    Length Should Be  ${resp.history}  0

Head Request Without Redirection
    ${resp}=  Head Request  ${GLOBAL_SESSION}  /redirect-to?url=anything  allow_redirects=${false}
    ${status}=  Convert To String  ${resp.status_code}
    Status Should Be  302  ${resp}
    Length Should Be  ${resp.history}  0

Post Request With Redirection
    [Tags]  post
    # FIXME should be 2 different tests
    # FIXME should be verifed also the payload is returned
    # FIXME returned http method should be verified
    ${resp}=  Post Request  ${GLOBAL_SESSION}  /redirect-to?url=anything  data=something
    Status Should be  OK  ${resp}
    ${redirected_url}=  Catenate  ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings  ${resp.json()['url']}  ${redirected_url}
    ${resp}=  Post Request  ${GLOBAL_SESSION}  /redirect-to?url=anything  data=something  allow_redirects=${true}
    Status Should be  OK  ${resp}
    ${redirected_url}=  Catenate  ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings  ${resp.json()['url']}  ${redirected_url}

Post Request Without Redirection
    [Tags]  post
    ${resp}=  Post Request  ${GLOBAL_SESSION}  /redirect-to?url=anything  data=something  allow_redirects=${false}
    Status Should be  302  ${resp}

Put Request With Redirection
    [Tags]  put
    # FIXME should be 2 different tests
    # FIXME should be verifed also the payload is returned
    # FIXME returned http method should be verified
    ${resp}=  Put Request  ${GLOBAL_SESSION}  /redirect-to?url=anything
    Status Should be  OK  ${resp}
    ${redirected_url}=  Catenate  ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings  ${resp.json()['url']}  ${redirected_url}
    ${resp}=  Put Request  ${GLOBAL_SESSION}  /redirect-to?url=anything  allow_redirects=${true}
    Status Should be  OK  ${resp}
    ${redirected_url}=  Catenate  ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings  ${resp.json()['url']}  ${redirected_url}

Put Request Without Redirection
    [Tags]  put
    ${resp}=  Put Request  ${GLOBAL_SESSION}  /redirect-to?url=anything  allow_redirects=${false}
    Status Should be  302  ${resp}
