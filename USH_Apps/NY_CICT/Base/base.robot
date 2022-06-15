*** Settings ***
Library  SeleniumLibrary
Library    String
Library    DateTime
Resource    ../Locators/locators.robot
Resource     ../Case Investigation (CI)/Forms/register a new case form.robot
Resource    ../Contact Tracing (CT)/Forms/register a new contact form.robot
Library     driverpath.py
Library    base_python_functions.py
Library    Collections


*** Variables ***

# Case Search
${first-name_case_search}    xpath:(//td/div[contains(., "First Name")]/following::input)[1]
${last-name_case_search}    xpath:(//td/div[contains(., "Last Name")]/following::input)[1]
${search all cases in the list}    //button[contains(., 'Search All')]

*** Keywords ***
    
HQ Login
    ${chromedriver_path}=   driverpath.Get Driver Path
    ${chrome_options}=  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys, selenium.webdriver
    Call Method    ${chrome_options}    add_argument    --disable-extensions
    Call Method    ${chrome_options}    add_argument    --headless
    Call Method    ${chrome_options}    add_argument    --start-maximized
    Call Method    ${chrome_options}    add_argument    --disable-dev-shm-usage
    Call Method    ${chrome_options}    add_argument    --no-sandbox
    Open Browser    ${LOGIN URL}    ${BROWSER}      executable_path=${chromedriver_path}       options=${chrome_options}

    Set Window Size    1920    1080
    Set Selenium Implicit Wait  ${implcit_wait_time}
    Maximize Browser Window
    Input Text    ${username}    ${email}
    Input Text    ${password}   ${pass}
    ${IsElementVisible}=  Run Keyword And Return Status    Element Should Be Visible   ${confirm_cookie}
    Run Keyword And Ignore Error    wait until page contains element    ${confirm_cookie}   30
    ${IsElementVisible}=  Run Keyword And Return Status    Element Should Be Visible   ${confirm_cookie}
    Run Keyword If     ${IsElementVisible}    Click Element  ${confirm_cookie}
    Click Button  ${submit_button}
    ${token}    Generate 2FA Token    ${secret}
    Input Text    ${otp_token}   ${token}
    Click Button  ${submit_button}
    Title Should Be    ${commcare hq title} 
    #Run Keyword And Ignore Error     Click Element    ${confirm_cookie}
    Open Web App


Open Web App
    ${IsElementVisible}=  Run Keyword And Return Status    Element Should Be Visible   ${confirm_cookie}
    Run Keyword If     ${IsElementVisible}    Click Element  ${confirm_cookie}
    Click Element    ${webapps_menu}
   
Open App Home Screen
    Sleep    3s
    Wait Until Element Is Visible    ${app_home}  
    Wait Until Element Is Enabled    ${app_home}     
    Click Element    ${app_home}
      
Open WebApp Home
    Sleep    3s
    ${IsElementVisible}=  Run Keyword And Return Status    Element Should Be Visible   ${confirm_cookie}
    Run Keyword If     ${IsElementVisible}    Click Element  ${confirm_cookie}
    Wait Until Element Is Enabled    ${webapps_home}
    Click Element    ${webapps_home}
    
Sync App
    Open WebApp Home
    Click Element    ${sync}
    Sleep    5s
    Wait Until Element Is Visible    ${sync success}    

Go Back Home and Sync App
    Click Element    ${home_btn}
    Click Element    ${sync}
    Sleep    5s
    Wait Until Element Is Visible    ${sync success}
    Sleep    5s
    Run Keyword And Ignore Error    Click Element    ${select_app}


Log in as ci_user
   Sync App
   Click Element    ${login_as}
   Click Element    ${ci_user}
   Sleep    2s
   Click Element    ${confirm_user_login}
   Sleep    2s
   Sync App
   Click Element    ${select_app} 
   
Log in as ct_user
   Sync App
   Click Element    ${login_as}
   Click Element    ${ct_user}
   Sleep    2s
   Click Element    ${confirm_user_login}
   Sync App
   Click Element    ${select_app} 

Log in as ctsup_user
   Sync App
   Click Element    ${login_as}
   Input Text    ${search_username}     CT Supervisor
   Click Element    ${search_user_button}
   Sleep    2s
   Click Element    ${ctsup_user}
   Sleep    2s
   Click Element    ${confirm_user_login}
   Sleep    2s
   Sync App
   Click Element    ${select_app}

Log in as cisup_user
   Sync App
   Click Element    ${login_as}
   Input Text    ${search_username}     CI Supervisor
   Click Element    ${search_user_button}
   Sleep    2s
   Click Element    ${cisup_user}
   Sleep    2s
   Click Element    ${confirm_user_login}
   Sleep    2s
   Sync App
   Click Element    ${select_app}

JS Click
    [Arguments]    ${element}
    Wait Until Element Is Enabled    ${element}    
#    Execute JavaScript  document.evaluate("${element}", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null).snapshotItem(0).click();
    Execute JavaScript    document.evaluate("${element}",document.body,null,9,null).singleNodeValue.click();

Generate Mobile Number
   ${mobile number}    Generate random string    10    0123456789 
   [Return]    ${mobile number}   
   
Yesterday's Date
   ${date}     Get Current Date    result_format=%m/%d/%Y    increment=-1 day
   [Return]   ${date}
   
Past Date Generator
   [Arguments]      ${n}
   ${date}     Get Current Date    result_format=%m/%d/%Y    increment=-${n} day
   [Return]   ${date}

<<<<<<< Updated upstream
Today's Date
   ${date}     Get Current Date    result_format=%m/%d/%Y
   [Return]   ${date}


Future Date Generator
   [Arguments]      ${n}
   ${date}     Get Current Date    result_format=%m/%d/%Y    increment=${n} day
   [Return]   ${date}


Select Dropdown
   [Arguments]    ${question}    ${answer}
   Wait Until Element Is Enabled   ${question}
   Wait Until Element Is Visible    ${question}
#   Click Element   ${question}
#   Wait Until Element Is Visible    ${answer}
#   Click Element  ${answer}
   Select From List By Index    ${answer}   ${1}
   
Answer Dropdown
   [Arguments]    ${question}    ${answer}
   Wait Until Element Is Enabled   ${question}
   Wait Until Element Is Visible    ${question}
   Click Element   ${question}
   Wait Until Element Is Visible    ${answer}
   Click Element  ${answer}

Answer Input Text
   [Arguments]    ${question}    ${answer}    ${success}
   Wait Until Element Is Enabled    ${question} 
   Scroll Element Into View    ${question} 
   Clear Element Text   ${question} 
   Input Text    ${question}     ${answer}
   Wait Until Element Is Visible    ${success}    60s
   
Search in the case list   
    [Arguments]    ${case_or_contact_created}
    Sleep    60s
    Input Text    ${search_case}    ${case_or_contact_created}
    Click Element    ${search_button}
    

Select Created Case
    [Arguments]    ${case_or_contact_created}
    Wait Until Element Is Enabled    ${case_or_contact_created}
    Wait Until Keyword Succeeds  3x  30 sec  JS Click    ${case_or_contact_created}
    Sleep    2s
    Wait Until Element Is Enabled    ${continue}
    Sleep    2s 
    Scroll Element Into View    ${continue}
    Wait Until Keyword Succeeds  3x  500ms  Click Element    ${continue}

Select Cluster
    [Arguments]    ${case_or_contact_created}
    Wait Until Element Is Enabled    //tr[.//td[text()='${case_or_contact_created}']]
    Sleep    2s
    JS Click    //tr[.//td[text()='${case_or_contact_created}']]



Select Created Case with no lab result
    [Arguments]    ${case_or_contact_created}
    Wait Until Element Is Enabled    (//tr[.//td[text()='${case_or_contact_created}']]/self::tr//td[6][(normalize-space())])
    Sleep    2s
    JS Click    (//tr[.//td[text()='${case_or_contact_created}']]/self::tr//td[6][(normalize-space())])
    Wait Until Element Is Enabled    ${continue}
    Sleep    2s
#    Scroll Element Into View    ${continue}
    Click Element    ${continue}

Select Created Case with lab result
    [Arguments]    ${case_or_contact_created}
    Wait Until Element Is Enabled    (//tr[.//td[text()='${case_or_contact_created}']]/self::tr//td[6][not(normalize-space())])
    Sleep    2s
    JS Click    (//tr[.//td[text()='${case_or_contact_created}']]/self::tr//td[6][not(normalize-space())])
    Wait Until Element Is Enabled    ${continue}
    Sleep    2s
#    Scroll Element Into View    ${continue}
    Click Element    ${continue}

Select Case with Open Status
    [Arguments]    ${case_or_contact_created}
    Wait Until Element Is Enabled    (//tr[.//td[text()='${case_or_contact_created}']]/self::tr//td[9][normalize-space()='Open']
    Sleep    2s
    JS Click    (//tr[.//td[text()='${case_or_contact_created}']]/self::tr//td[9][normalize-space()='Open']
    Wait Until Element Is Enabled    ${continue}
    Sleep    2s
#    Scroll Element Into View    ${continue}
    Click Element    ${continue}

Case Search Search All
    Wait Until Element Is Enabled    ${search all cases in the list}
    JS Click    ${search all cases in the list}
    Wait Until Element Is Enabled    ${case search submit}
    JS Click    ${case search submit}
    
Case Search
    [Arguments]     ${case_or_contact_created}   
    Wait Until Element Is Enabled    ${search all cases in the list}
    JS Click    ${search all cases in the list}
    Sleep    5s
    Wait Until Element Is Enabled    ${first-name_case_search}
    Wait Until Keyword Succeeds  3x  500ms  Input Text    ${first-name_case_search}    ${case_or_contact_created}
    Wait Until Keyword Succeeds  3x  500ms  Input Text    ${last-name_case_search}    ${case_or_contact_created}
    Wait Until Element Is Enabled    ${case search submit}
    Wait Until Keyword Succeeds  3x  500ms  JS Click    ${case search submit}




Submit Form and Check Success
    Element Should Be Enabled    ${submit_form}
    JS Click   ${submit_form}
    Wait Until Element Is Visible    ${success_message}    60s
    Element Should Be Visible    ${success_message}

Click Element
    [Arguments]     ${element}
    Wait Until Element Is Visible    ${element}     40s
    SeleniumLibrary.Click Element    ${element}

Click Button
    [Arguments]     ${element}
    Wait Until Element Is Visible    ${element}     40s
    SeleniumLibrary.Click Button    ${element}

Input Text
    [Arguments]    ${element}     ${text}
    Wait Until Element Is Visible    ${element}     60s
    SeleniumLibrary.Input Text    ${element}     ${text}
