*** Settings ***
Documentation     Workflow to test Patient and Contact Good Path
Suite Setup    Driver Launch
Library  SeleniumLibrary    timeout=200s
Library  DependencyLibrary
Resource    ../Case Investigation (CI)/Menu/menu.robot
Resource    ../Case Investigation (CI)/Forms/register a new case form.robot
Resource    ../Case Investigation (CI)/Forms/case investigation form.robot
Resource    ../Case Investigation (CI)/Forms/assign or reassign form.robot

Suite Teardown  Close Browser

*** Test Cases ***

Patient_Good_1
    [Documentation]    Register New Case
    HQ Login
    Log in as ci_user
    Register New Case
    Open All Cases: Incomplete Demographic Information Menu
    ${case_name}    Get Case Name
    ${case_created}   Set Case Name
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Open All Open Cases
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Set Global Variable    ${case_name}
    Set Global Variable    ${case_created}


Patient_Good_2
    [Documentation]    All Cases: Incomplete Demographic Information
    Depends on test     Patient_Good_1
    Open All Cases: Incomplete Demographic Information Menu
    Sleep    20s
    ${case_name}    Get Case Name
    ${case_created}   Set Case Name
    Case Search    ${case_name}
    Search in the case list      ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Select Created Case    ${case_created}
    Fill up and Submit Case Investigation Form
    ## Landed on Incomplete Demographic page
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Not Be Visible    ${case_created}
    Open All Open Cases
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Open All Cases: Unassigned & Open
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}


Patient_Good_3
    [Documentation]    All Cases: Assigned & Open
    Depends on test     Patient_Good_2
    Open All Cases: Unassigned & Open
    ${case_name}    Get Case Name
    ${case_created}   Set Case Name
    Search in the case list      ${case_name}
    Element Should Be Visible    ${case_created}
    Select Created Case    ${case_created}
    Permanently Assign to Self
    ## Lands on Unassigned and open
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Not Be Visible    ${case_created}
    Open All Cases: Assigned & Open
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Open All Open Cases
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}


Patient_Good_4
    [Documentation]    All Cases: Unassigned & Open
    Depends on test     Patient_Good_3
    Open All Cases: Assigned & Open
    ${case_name}    Get Case Name
    ${case_created}   Set Case Name
    Search in the case list      ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Select Created Case    ${case_created}
    Unassign from Self
    ## Lands on Assigned and open
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Not Be Visible    ${case_created}
    Open All Cases: Unassigned & Open
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  5 sec       Element Should Be Visible    ${case_created}
    Open All Open Cases
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}

Patient_Good_5
    [Documentation]    My Cases
    Depends on test     Patient_Good_4
    Open All Cases: Unassigned & Open
    ${case_name}    Get Case Name
    ${case_created}   Set Case Name
    Search in the case list      ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Select Created Case    ${case_created}
    Permanently Assign to Self
    ## Lands on Unassigned and open
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Not Be Visible    ${case_created}
    Open My Cases
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Open All Open Cases
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}


Patient_Good_6
    [Documentation]    All Cases: Unable to Reach
    Depends on test     Patient_Good_5
    Open My Cases
    ${case_name}    Get Case Name
    ${case_created}   Set Case Name
    Search in the case list      ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Select Created Case    ${case_created}
    Open Form    ${Case Investigation Form}
    Unable to reach
    All Cases: Unable to Reach
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Open All Open Cases
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}

Patient_Good_7
    [Documentation]    All Closed Cases
    Depends on test     Patient_Good_6
    Open All Cases
    ${case_name}    Get Case Name
    ${case_created}   Set Case Name
    Search in the case list      ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Select Created Case    ${case_created}
    Open Form    ${Case Investigation Form}
    Activity for case complete
    Open All Closed Cases
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Be Visible    ${case_created}
    Open All Open Cases
    Search in the case list     ${case_name}
    Wait Until Keyword Succeeds  2 min  20 sec      Element Should Not Be Visible    ${case_created}
