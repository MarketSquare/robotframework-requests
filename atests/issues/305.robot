*** Settings ***
Library   RequestsLibrary

*** Test Cases ***
Test NTLM Session without installed library
    ${auth}=    Create List  1  2  3
    Run Keyword And Expect Error  requests_ntlm module not installed  Create Ntlm Session  ntlm  http://localhost:80  ${auth}
