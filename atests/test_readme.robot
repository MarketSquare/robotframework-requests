*** Settings ***
Library  Collections
Library  RequestsLibrary

*** Test Cases ***

Quick GET Request Test
    [Tags]  skip
    ${response}=    GET    https://www.google.com/search    params=query=ciao    expected_status=200

Quick GET A JSON Body
    [Tags]  skip
    ${response}=    GET    https://jsonplaceholder.typicode.com/posts/1
    Should Be Equal As Strings   1  ${response.json()}[id]


Get Request Test
    [Tags]  skip
    Create Session    jsonplaceholder    https://jsonplaceholder.typicode.com
    Create Session    google             http://www.google.com

    ${resp_google}=   GET On Session     google             /           expected_status=200
    ${resp_json}=     GET On Session     jsonplaceholder    /posts/1

    Should Be Equal As Strings           ${resp_google.reason}    OK
    Dictionary Should Contain Value      ${resp_json.json()}    sunt aut facere repellat provident occaecati excepturi optio reprehenderit

Post Request Test
    [Tags]  skip
    Create Session    jsonplaceholder    https://jsonplaceholder.typicode.com

    &{data}=          Create dictionary  title=Robotframework requests  body=This is a test!  userId=1
    ${resp}=          POST On Session    jsonplaceholder     /posts    json=${data}    expected_status=anything

    Status Should Be                     201    ${resp}
    Dictionary Should Contain Key        ${resp.json()}     id
