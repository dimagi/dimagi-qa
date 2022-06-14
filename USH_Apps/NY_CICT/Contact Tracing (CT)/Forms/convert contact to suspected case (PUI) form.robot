*** Settings ***
Library  SeleniumLibrary
Resource    ../../Base/base.robot
Resource    change to pui status form.robot


*** Keywords ***

Convert contact to PUI form
    Open All Contacts Unassigned & Open menu
    ${contact_name}    Get Contact Name
    ${contact_created}   Set Contact Name
    Search in the case list    ${contact_name}
    Select Created Case    ${contact_created}    
    Wait Until Element Is Enabled    ${covert_to_pui_form}
    JS Click    ${covert_to_pui_form} 
    PUI form submission

Convert contact to PUI form - No
    Open All Contacts Unassigned & Open menu
    ${contact_name}    Get Contact Name
    ${contact_created}   Set Contact Name
    Search in the case list    ${contact_name}
    Select Created Case    ${contact_created}
    Wait Until Element Is Enabled    ${covert_to_pui_form}
    JS Click    ${covert_to_pui_form}
    PUI form submission - No

Select Created Case and Submit PUI form
    Select Created Case    ${contact_created}
    Wait Until Element Is Enabled    ${covert_to_pui_form}
    JS Click    ${covert_to_pui_form}
    PUI form submission