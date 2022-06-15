*** Settings ***
Documentation     Workflow to test Contact Good Path
#Suite Setup    HQ Login
Library  SeleniumLibrary
Resource    ../Contact Tracing (CT)/Menu/menu.robot
Resource    ../Contact Tracing (CT)/Forms/register a new contact form.robot  
Resource    ../Contact Tracing (CT)/Forms/contact montitoring form.robot
Resource    ../Contact Tracing (CT)/Forms/assign or reaasign contact.robot
Resource    ../Tests/01 Patient Good Path.robot
Suite Teardown  Close Browser


*** Test Cases ***

Contact_Good_1
    [Documentation]    All Contacts: Incomplete Contact Information
    Log in as ct_user
    Log    ${case_name}+"and"+${case_created}
    Register contact without phone number    ${case_name}    ${case_created}
    ${contact_name}    Get Contact Name
    ${contact_created}   Set Contact Name
    Open All Contacts Unassigned & Open menu
    Search in the case list     ${contact_name}  
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Not Be Visible    ${contact_created}

    Open All Contacts: Incomplete Contact Information
    Search in the case list     ${contact_name}  
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}

Contact_Good_2
    [Documentation]    All Contacts: Unable to Reach

    Open All Contacts: Incomplete Contact Information
    ${contact_name}    Get Contact Name
    ${contact_created}   Set Contact Name
    Case Search    ${contact_name}
    Search in the case list      ${contact_name}
    Element Should Be Visible    ${contact_created}
    Select Created Case    ${contact_created}
    Open Contact Monitoring Form
    Unable to reach (CM)

    Open All Contacts: Incomplete Contact Information
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Not Be Visible    ${contact_created}

    Open All Contacts Unassigned & Open menu
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}

    Open All Contacts: Unable to Reach
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}


Contact_Good_3
    [Documentation]    All Contacts: Unassigned & Open

    Open All Contacts: Unable to Reach
    ${contact_name}    Get Contact Name
    ${contact_created}   Set Contact Name
    Search in the case list      ${contact_name}
    Select Created Case    ${contact_created}
    Open Contact Monitoring Form
    Reached and Agreed to Call (CM)

    Open All Contacts: Unable to Reach
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Not Be Visible    ${contact_created}

    Open All Contacts Unassigned & Open menu
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}

    Open All Open Contacts menu
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}

Contact_Good_4
    [Documentation]    All Contacts: Assigned & Open

    Open All Contacts Unassigned & Open menu
    ${contact_name}    Get Contact Name
    ${contact_created}   Set Contact Name
    Search in the case list      ${contact_name}
    Select Created Case    ${contact_created}
    Permanently Assign to Self (CM)

    ## Lands on Unassigned and open
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Not Be Visible    ${contact_created}

    Open My Contacts: Require Follow-Up
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}

    Open All Contacts: Assigned & Open
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}

    Open All Open Contacts menu
    Search in the case list     ${contact_name}
    Element Should Be Visible    ${contact_created}

Contact_Good_5
    [Documentation]    All Contacts: Require Follow-up

    Open All Contacts: Assigned & Open
    ${contact_name}    Get Contact Name
    ${contact_created}   Set Contact Name
    Search in the case list      ${contact_name}
    Select Created Case    ${contact_created}
    Open Contact Monitoring Form
    Requires Follow-up (CM)

    Open All Contacts: Require Follow-Up
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}

    Open All Contacts
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}


Contact_Good_6
    [Documentation]    All Contacts: SMS

    Open All Contacts: Require Follow-Up
    ${contact_name}    Get Contact Name
    ${contact_created}   Set Contact Name
    Search in the case list      ${contact_name}
    Select Created Case    ${contact_created}
    Open Contact Monitoring Form
    Receive SMS (CM)

    Open All Contacts: Require Follow-Up
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Not Be Visible    ${contact_created}

    Open All Contacts
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}



Contact_Good_7
    [Documentation]    All Contacts

    Open All Contacts
    ${contact_name}    Get Contact Name
    ${contact_created}   Set Contact Name
    Search in the case list      ${contact_name}
    Select Created Case    ${contact_created}
    Open Contact Monitoring Form
    Partial Interview Complete (CM)

    ## PAUSE UNTIL THE NEXT DAY!! [Check if required and if so how?]
    Open All Contacts: Require Follow-Up
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}

    Open My Contacts: Require Follow-Up
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}

Contact_Good_8
    [Documentation]    My Contacts: Require Follow-Up

    Open My Contacts: Require Follow-Up
    ${contact_name}    Get Contact Name
    ${contact_created}   Set Contact Name
    Search in the case list      ${contact_name}
    Select Created Case    ${contact_created}
    Unassign from Self (CM)

    Open My Contacts: Require Follow-Up
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Not Be Visible    ${contact_created}

    Open All Contacts: Require Follow-Up
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}

Contact_Good_9
    [Documentation]   All Closed Contacts

    Open All Contacts
    ${contact_name}    Get Contact Name
    ${contact_created}   Set Contact Name
    Search in the case list      ${contact_name}
    Select Created Case    ${contact_created}
    Open Contact Monitoring Form
    Interview Complete (CM)

    Open All Open Contacts menu
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Not Be Visible    ${contact_created}

    Open All Closed Contacts menu
    Search in the case list     ${contact_name}
    Wait Until Keyword Succeeds  2 min  5 sec   Element Should Be Visible    ${contact_created}