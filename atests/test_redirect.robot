*** Settings ***
Library  ../src/RequestsLibrary/RequestsKeywords.py
Resource  res_setup.robot

Suite Setup     Setup Flask Http Server
Suite Teardown  Teardown Flask Http Server And Sessions

*** Test Cases ***
Get Request With Redirection
    [Tags]  get
    Create Session  httpbin  http://httpbin.org    debug=3
    ${resp}=  Get Request  httpbin  /redirect/1
    Should Be Equal As Strings  ${resp.status_code}  200

    ${resp}=  Get Request  httpbin  /redirect/1  allow_redirects=${true}
    Should Be Equal As Strings  ${resp.status_code}  200

Get Request Without Redirection
    [Tags]  get
    Create Session  httpbin  http://httpbin.org
    ${resp}=  Get Request  httpbin  /redirect/1  allow_redirects=${false}
    ${status}=  Convert To String  ${resp.status_code}
    Should Start With  ${status}  30

Options Request With Redirection
    [Tags]  options
    Create Session  httpbin  http://httpbin.org
    ${resp}=  Options Request  httpbin  /redirect/1
    Should Be Equal As Strings  ${resp.status_code}  200
    ${resp}=  Options Request  httpbin  /redirect/1  allow_redirects=${true}
    Should Be Equal As Strings  ${resp.status_code}  200

Head Request With Redirection
    [Tags]  head
    Create Session  httpbin  http://httpbin.org
    ${resp}=  Head Request  httpbin  /redirect/1  allow_redirects=${true}
    Should Be Equal As Strings  ${resp.status_code}  200

Head Request Without Redirection
    [Tags]  head
    Create Session  httpbin  http://httpbin.org
    ${resp}=  Head Request  httpbin  /redirect/1
    ${status}=  Convert To String  ${resp.status_code}
    Should Start With  ${status}  30
    ${resp}=  Head Request  httpbin  /redirect/1  allow_redirects=${false}
    ${status}=  Convert To String  ${resp.status_code}
    Should Start With  ${status}  30

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
