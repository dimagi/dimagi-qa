*** Settings ***
Documentation     Testing the workflow to deduplicate a suspected case (PUI) record against a confirmed
...               case record with one attached lab results and one attached contact.
Library  SeleniumLibrary
Suite Setup    HQ Login
Resource    ../Contact Tracing (CT)/Forms/change to pui status form.robot
Resource    ../Contact Tracing (CT)/Forms/contact montitoring form.robot
Resource    ../Contact Tracing (CT)/Forms/convert contact to suspected case (PUI) form.robot  
Resource    ../Contact Tracing (CT)/Forms/register a new contact form.robot
Resource    ../Case Investigation (CI)/Menu/menu.robot
Resource    ../Case Investigation (CI)/Forms/register a new case form.robot
Resource    ../Case Investigation (CI)/Forms/view record lab results.robot
Resource    ../Case Investigation (CI)/Forms/register new contacts form.robot
Resource    ../Case Investigation (CI)/Forms/change pui status form.robot
Resource    ../Case Investigation (CI)/Forms/search for duplicate patient.robot
Resource    ../Case Investigation (CI)/Forms/case investigation form.robot
Suite Teardown  Close Browser

*** Test Cases ***


Convert_PUI_to_Patient_1
    [Documentation]    Convert Contact to PUI using Convert Contact to Suspected Case (PUI) form
    Log in as ct_user
    ${created_name}  ${phone}   Register contact with phone number
    ${contact_name}    Get Contact Name
    ${contact_created}    Set Contact Name
    Log To Console    ${created_name}  ${phone}
    Convert contact to PUI form - No
    Open All Contacts Unassigned & Open menu
    Search in the case list    ${contact_name}
    Element Should Be Visible    ${contact_created}
    Select Created Case and Submit PUI form
    Open All Contacts Unassigned & Open menu
    Search in the case list    ${contact_name}
    Element Should Not Be Visible    ${contact_created}
    Set Global Variable    ${created_name}
    Set Global Variable    ${phone}

Convert_PUI_to_Patient_2
    [Documentation]    Convert Contact to PUI using Convert Contact to Suspected Case (PUI) form
    Open App Home Screen
    Log in as ci_user

    ${mphid}     ${case_name}   Register New Case   ${created_name}
    Add Phone Number in Case Investigation form     ${phone}
    ${case_created}   Set Variable    //tr[.//td[text()='${case_name}']]
    Set Global Variable    ${case_created}
    Open All Cases
    Search in the case list     ${case_name}
    Element Should Be Visible    ${case_created}
    Search in the case list    ${case_name}
    Select Created Case    ${case_created}
    Add New Lab Result
    Search in the case list     ${case_name}
    Element Should Be Visible    ${case_created}
    Search in the case list    ${case_name}
    Select Created Case with lab result    ${created_name}
    Register New Contacts to Case   2  ${created_name}  ${phone}


Convert_PUI_to_Patient_3
    [Documentation]    Convert PUI to Patient
    Open App Home Screen
    Log in as ci_user
    Open All Suspected Cases (PUIs) menu
    ${contact_name}    Get Contact Name
    ${contact_created}    Set Contact Name
    Case Search     ${contact_name}
    Select Created Case     ${case_created}
    Convert Suspected Case to Confirmed Case

Convert_PUI_to_Patient_4
    [Documentation]    Convert PUI to Patient
    Open App Home Screen
    Log in as ci_user
    Open All Cases
    ${contact_name}    Get Contact Name
    Case Search     ${contact_name}
    Select Created Case with lab result    ${contact_name}
    Search Duplicate Patient    ${contact_name}
    Open All Cases
    Sleep    3s
    Search in the case list     ${contact_name} ${contact_name}
    Verify Lab result for open case     ${contact_name}
    Verify Registered Contacts for open case     ${contact_name}
