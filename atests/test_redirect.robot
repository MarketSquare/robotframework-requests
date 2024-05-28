*** Settings ***
Library     RequestsLibrary


*** Test Cases ***
Get Request With Default Redirection
    [Tags]    get
    ${resp}=    GET    url=${HTTP_LOCAL_SERVER}/redirect-to?url=anything
    Status Should Be    OK    ${resp}
    Length Should Be    ${resp.history}    1

Get Request With Redirection
    [Tags]    get
    ${resp}=    GET    url=${HTTP_LOCAL_SERVER}/redirect-to?url=anything    allow_redirects=${True}
    Status Should Be    OK    ${resp}
    Length Should Be    ${resp.history}    1

Get Request Without Redirection
    [Tags]    get
    ${resp}=    GET    url=${HTTP_LOCAL_SERVER}/redirect-to?url=anything    allow_redirects=${False}
    Status Should Be    302    ${resp}
    Length Should Be    ${resp.history}    0

Head Request Without Default Redirection
    [Tags]    head
    ${resp}=    HEAD    url=${HTTP_LOCAL_SERVER}/redirect-to?url=anything
    Status Should Be    302    ${resp}
    Length Should Be    ${resp.history}    0

Head Request With Redirection
    [Tags]    head
    ${resp}=    HEAD    url=${HTTP_LOCAL_SERVER}/redirect-to?url=anything    allow_redirects=${True}
    Status Should Be    OK    ${resp}
    Length Should Be    ${resp.history}    1

Head Request Without Redirection
    [Tags]    head
    ${resp}=    HEAD    url=${HTTP_LOCAL_SERVER}/redirect-to?url=anything    allow_redirects=${False}
    Status Should Be    302    ${resp}
    Length Should Be    ${resp.history}    0

Get Request on Session With Default Redirection
    [Tags]    get
    ${resp}=    GET On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything
    Status Should Be    OK    ${resp}
    Length Should Be    ${resp.history}    1

Get Request on Session With Redirection
    [Tags]    get
    ${resp}=    GET On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${true}
    Status Should Be    OK    ${resp}
    Length Should Be    ${resp.history}    1

Get Request on Session Without Redirection
    [Tags]    get
    ${resp}=    GET On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${false}
    Status Should Be    302    ${resp}
    Length Should Be    ${resp.history}    0

Options Request on Session With Redirection By Default
    [Tags]    options
    ${resp}=    OPTIONS On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything
    Status Should Be    200    ${resp}
    Length Should Be    ${resp.history}    1

Options Request on Session With Redirection
    [Tags]    options
    ${resp}=    OPTIONS On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${true}
    Status Should Be    OK    ${resp}
    Length Should Be    ${resp.history}    1

Options Request on Session Without Redirection
    [Tags]    options
    ${resp}=    OPTIONS On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${false}
    Status Should Be    302    ${resp}
    Length Should Be    ${resp.history}    0

Head Request on Session Without Redirection By Default
    [Tags]    head
    ${resp}=    HEAD On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything
    ${status}=    Convert To String    ${resp.status_code}
    Status Should Be    302    ${resp}
    Length Should Be    ${resp.history}    0

Head Request on Session With Redirection
    [Tags]    head
    ${resp}=    HEAD On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${true}
    Status Should Be    OK    ${resp}
    Length Should Be    ${resp.history}    1

Head Request on Session Without Redirection
    ${resp}=    HEAD On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${false}
    ${status}=    Convert To String    ${resp.status_code}
    Status Should Be    302    ${resp}
    Length Should Be    ${resp.history}    0

Post Request on Session With Redirection
    [Tags]    post
    # FIXME should be 2 different tests
    # FIXME should be verifed also the payload is returned
    # FIXME returned http method should be verified
    ${resp}=    POST On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    data=something
    Status Should be    OK    ${resp}
    ${redirected_url}=    Catenate    ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings    ${resp.json()['url']}    ${redirected_url}
    ${resp}=    POST On Session
    ...    ${GLOBAL_SESSION}
    ...    url=/redirect-to?url=anything
    ...    data=something
    ...    allow_redirects=${true}
    Status Should be    OK    ${resp}
    ${redirected_url}=    Catenate    ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings    ${resp.json()['url']}    ${redirected_url}

Post Request on Session Without Redirection
    [Tags]    post
    ${resp}=    POST On Session
    ...    ${GLOBAL_SESSION}
    ...    url=/redirect-to?url=anything
    ...    data=something
    ...    allow_redirects=${false}
    Status Should be    302    ${resp}

Put Request on Session With Redirection
    [Tags]    put
    # FIXME should be 2 different tests
    # FIXME should be verifed also the payload is returned
    # FIXME returned http method should be verified
    ${resp}=    PUT On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything
    Status Should be    OK    ${resp}
    ${redirected_url}=    Catenate    ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings    ${resp.json()['url']}    ${redirected_url}
    ${resp}=    PUT On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${true}
    Status Should be    OK    ${resp}
    ${redirected_url}=    Catenate    ${HTTP_LOCAL_SERVER}/anything
    Should Be Equal As Strings    ${resp.json()['url']}    ${redirected_url}

Put Request on Session Without Redirection
    [Tags]    put
    ${resp}=    PUT On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${false}
    Status Should be    302    ${resp}

CONNECT Request on Session Without Redirection
    [Tags]    connect
    ${resp}=    CONNECT On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${false}
    Status Should be    302    ${resp}
    Length Should Be    ${resp.history}    0

CONNECT Request on Session With Redirection
    [Tags]    connect
    ${resp}=    CONNECT On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${true}
    Status Should be    OK    ${resp}
    Length Should Be    ${resp.history}    1

TRACE Request on Session Without Redirection
    [Tags]    trace
    ${resp}=    TRACE On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${false}
    Status Should be    302    ${resp}
    Length Should Be    ${resp.history}    0

TRACE Request on Session With Redirection
    [Tags]    trace
    ${resp}=    TRACE On Session    ${GLOBAL_SESSION}    url=/redirect-to?url=anything    allow_redirects=${true}
    Status Should be    OK    ${resp}
    Length Should Be    ${resp.history}    1
