*** Settings ***
Library  Collections
Library  String
Library  RequestsLibrary
Library  OperatingSystem
Resource  ../res_setup.robot

*** Variables ***
${JSON_DATA}  '{"file":{"path":"/logo1.png"},"token":"some-valid-oauth-token"}'

*** Test Cases ***
Encoding Error
    ${headers}=  Create Dictionary  Content-Type=application/json
    Set Suite Variable  ${data}   { "elementToken":"token", "matchCriteria":[{"field":"name","dataType":"string","useOr":"false","fieldValue":"Operation check 07", "closeParen": "false", "openParen": "false", "operator": "equalTo"}], "account": { "annualRevenue": "456666", "name": "Account", "numberOfEmployees": "integer", "billingAddress": { "city": "Miami", "country": "US", "countyOrDistrict": "us or fl", "postalCode": "33131", "stateOrProvince": "florida", "street1": "Trade Center", "street2": "North Main rd" }, "number": "432", "industry": "Bank", "type": "string", "shippingAddress": { "city": "denver", "country": "us", "countyOrDistrict": "us or co", "postalCode": "80202", "stateOrProvince": "colorado", "street1": "Main street", "street2": "101 Avenu"}}}

    ${resp}=  POST On Session   ${GLOBAL_SESSION}  /anything  data=${data}  headers=${headers}
    Should Be Equal As Strings  ${resp.status_code}  200
