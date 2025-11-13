*** Settings ***
Documentation     API tests for authentication endpoints
Library           RequestsLibrary
Library           DateTime
Library           String

*** Variables ***
${BASE_URL}       http://localhost:8000
${SIGNUP_URL}     ${BASE_URL}/auth/signup
${SIGNIN_URL}     ${BASE_URL}/auth/signin

*** Test Cases ***
Test Sign Up Success
    [Documentation]    Test successful user signup
    ${timestamp}=    Get Current Date    result_format=epoch
    ${user_id}=    Set Variable    test_user_${timestamp}
    ${password}=    Set Variable    test_password
    ${data}=    Create Dictionary    user_id=${user_id}    password=${password}
    ${response}=    POST    ${SIGNUP_URL}    json=${data}
    Should Be Equal As Strings    ${response.status_code}    201
    ${json}=    Set Variable    ${response.json()}
    Should Be Equal As Strings    ${json}[user_id]    ${user_id}
    Dictionary Should Contain Key    ${json}    message

Test Sign Up Duplicate User
    [Documentation]    Test signup with duplicate user_id
    ${timestamp}=    Get Current Date    result_format=epoch
    ${user_id}=    Set Variable    duplicate_user_${timestamp}
    ${password}=    Set Variable    test_password
    ${data}=    Create Dictionary    user_id=${user_id}    password=${password}
    POST    ${SIGNUP_URL}    json=${data}
    ${response}=    POST    ${SIGNUP_URL}    json=${data}
    Should Be Equal As Strings    ${response.status_code}    400
    ${json}=    Set Variable    ${response.json()}
    Should Contain    ${json}[detail]    already exists

Test Sign In Success
    [Documentation]    Test successful user signin
    ${timestamp}=    Get Current Date    result_format=epoch
    ${user_id}=    Set Variable    signin_user_${timestamp}
    ${password}=    Set Variable    test_password
    ${signup_data}=    Create Dictionary    user_id=${user_id}    password=${password}
    POST    ${SIGNUP_URL}    json=${signup_data}
    ${signin_data}=    Create Dictionary    user_id=${user_id}    password=${password}
    ${response}=    POST    ${SIGNIN_URL}    json=${signin_data}
    Should Be Equal As Strings    ${response.status_code}    200
    ${json}=    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${json}    token
    Should Be Equal As Strings    ${json}[user_id]    ${user_id}
    Dictionary Should Contain Key    ${json}    start_time
    Dictionary Should Contain Key    ${json}    max_time

Test Sign In Wrong Password
    [Documentation]    Test signin with wrong password
    ${timestamp}=    Get Current Date    result_format=epoch
    ${user_id}=    Set Variable    wrong_pass_user_${timestamp}
    ${password}=    Set Variable    test_password
    ${signup_data}=    Create Dictionary    user_id=${user_id}    password=${password}
    POST    ${SIGNUP_URL}    json=${signup_data}
    ${signin_data}=    Create Dictionary    user_id=${user_id}    password=wrong_password
    ${response}=    POST    ${SIGNIN_URL}    json=${signin_data}
    Should Be Equal As Strings    ${response.status_code}    401
    ${json}=    Set Variable    ${response.json()}
    Should Contain    ${json}[detail]    Invalid

Test Sign In Nonexistent User
    [Documentation]    Test signin with non-existent user
    ${timestamp}=    Get Current Date    result_format=epoch
    ${user_id}=    Set Variable    nonexistent_user_${timestamp}
    ${signin_data}=    Create Dictionary    user_id=${user_id}    password=test_password
    ${response}=    POST    ${SIGNIN_URL}    json=${signin_data}
    Should Be Equal As Strings    ${response.status_code}    401
    ${json}=    Set Variable    ${response.json()}
    Should Contain    ${json}[detail]    Invalid

Test Sign In Existing Session
    [Documentation]    Test that signin returns existing session if valid
    ${timestamp}=    Get Current Date    result_format=epoch
    ${user_id}=    Set Variable    existing_session_user_${timestamp}
    ${password}=    Set Variable    test_password
    ${signup_data}=    Create Dictionary    user_id=${user_id}    password=${password}
    POST    ${SIGNUP_URL}    json=${signup_data}
    ${signin_data}=    Create Dictionary    user_id=${user_id}    password=${password}
    ${response1}=    POST    ${SIGNIN_URL}    json=${signin_data}
    ${token1}=    Set Variable    ${response1.json()}[token]
    ${response2}=    POST    ${SIGNIN_URL}    json=${signin_data}
    ${token2}=    Set Variable    ${response2.json()}[token]
    Should Be Equal    ${token1}    ${token2}

