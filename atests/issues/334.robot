*** Settings ***
Documentation    Testing with a external API: https://fakerestapi.azurewebsites.net/index.html
...              Testing (pt-br) accents in body string JSON

Library          RequestsLibrary

Suite Setup      Run Keywords
...              Create Session fakeAPI
...              AND  Check if fakeAPI is online


*** Variables ***
${URL_API}       https://fakerestapi.azurewebsites.net/api/v1
&{BOOK_201}      ID=201
...              Title=Meu novo Book com acentuação
...              Description=Meu novo livro conta coisas fantásticas
...              PageCount=523
...              Excerpt=Meu Novo livro é, sem dúvida, extraordinário
...              PublishDate=2018-04-26T17:58:14.765Z
&{BOOK_150}      ID=150
...              Title=Book 150 alterado com acentuação
...              Description=Descrição do book 150 alterada
...              PageCount=600
...              Excerpt=Resumo do book 150 alterado
...              PublishDate=2017-04-26T15:58:14.765Z
${ACCENT_ERROR}  The JSON value could not be converted to System.String.


*** Test Cases ***
POST a new Book with (pt-br) accents
    POST a new Book (with "data")

PUT a new Book with (pt-br) accents
    PUT a Book (with "data")


*** Keywords ***
Create Session fakeAPI
    ${headers}       Create Dictionary    content-type=application/json
    Create Session   fakeAPI    ${URL_API}    headers=${headers}  disable_warnings=${True}

Check if fakeAPI is online
    [Documentation]  Checking API: https://fakerestapi.azurewebsites.net/index.html 
    ${response}  Get On Session    fakeAPI    /Users/1   expected_status=any
    ${status}    Run Keyword and Return Status
    ...          Status Should Be   200
    Run Keyword Unless  ${status}   Fatal Error
    ...  msg=External API is not responding as expected. Please try again later or check the server for changes.

POST a new Book (with "data")
    ${response}    Post On Session   fakeAPI    Books
    ...            data={"id":${BOOK_201.ID},"title":"${BOOK_201.Title}","description":"${BOOK_201.Description}","pageCount":${BOOK_201.PageCount},"excerpt":"${BOOK_201.Excerpt}","publishDate":"${BOOK_201.PublishDate}"}
    ...            expected_status=any
    Check Accents Error  ${response}
    Status Should Be     200

PUT a Book (with "data")
    ${response}    Put On Session   fakeAPI    Books/150
    ...            data={"id":${BOOK_150.ID},"title":"${BOOK_150.Title}","description":"${BOOK_150.Description}","pageCount":${BOOK_150.PageCount},"excerpt":"${BOOK_150.Excerpt}","publishDate":"${BOOK_150.PublishDate}"}
    ...            expected_status=any
    Check Accents Error  ${response}
    Status Should Be     200

Check Accents Error
    [Arguments]   ${response}
    Should Not Contain    ${response.text}    ${ACCENT_ERROR}
    ...  msg=The answer shows that there is still malformed JSON error. Possible accent/encode error.    