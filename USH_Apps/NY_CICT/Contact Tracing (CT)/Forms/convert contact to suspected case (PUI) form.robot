*** Settings ***
Library  SeleniumLibrary
Resource    ../../Base/base.robot
Resource    change to pui status form.robot


*** Keywords *** 

Convert contact to PUI form
    Open All Contacts Unassigned & Open menu
    ${contact_name}    Get Case Name
    ${contact_created}   Set Case Name
    Search in the case list    ${contact_name}
    Select Created Case    ${contact_created}    
    Wait Until Element Is Enabled    ${covert_to_pui_form}
    JS Click    ${covert_to_pui_form} 
    PUI form submission
  