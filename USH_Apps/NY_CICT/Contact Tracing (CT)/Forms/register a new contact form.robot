*** Settings ***
Library  SeleniumLibrary
Library    String
Library    DateTime
Resource    ../Menu/menu.robot
Resource    ../../Base/base.robot


*** Keywords ***

Generate Random Contact Name
    ${hex} =    Generate Random String	6	[NUMBERS]abcdef
    ${date}     Get Current Date    result_format=%m/%d/%Y
    ${contact_name_random} =     Catenate	SEPARATOR=-	Contact	${hex}  ${date}
    Set Suite Variable  ${contact_name_random}
    [Return]    ${contact_name_random}

   
Register contact with phone number
   Open Register New Contacts Menu
   Select Created Case    ${select_first case_in_caselist}
   Run Keyword And Ignore Error     Wait Until Element Is Visible    ${register_new_contacts_form}
   Run Keyword And Ignore Error    JS Click    ${register_new_contacts_form}
   Generate Random Contact Name
   ${name_random}    Get Variable Value    ${contact_name_random}
   Input Text       ${contact_first_name}    ${name_random}
   Input Text       ${contact_last_name}    ${name_random}
   Run Keyword And Ignore Error     Phone No not Matching
   ${Mobile number}    Generate Mobile Number
   Input Text       ${contact_phone_num}    ${Mobile number}
   JS Click    ${preferred_language}
   JS Click   ${last_contact_date}
   ${Yesterday's date}    Yesterday's Date
   Input Text    ${last_contact_date}   ${Yesterday's date}
   JS Click    ${last_contact_date}
   Submit Form and Check Success  
   [Return]  ${name_random}  ${Mobile number}


Register contact without phone number
   [Arguments]  ${case_name}    ${case_created}
   Open Register New Contacts Menu
#   ${case_name}    Get Case Name
#   ${case_created}   Set Case Name
   Case Search    ${case_name}    
   Search in the case list    ${case_name}
   Select Created Case    ${case_created}
   Run Keyword And Ignore Error     Wait Until Element Is Visible    ${register_new_contacts_form}
   Run Keyword And Ignore Error    JS Click    ${register_new_contacts_form}
   Generate Random Contact Name
   ${name_random}    Get Variable Value    ${contact_name_random}
   Input Text       ${contact_first_name}    ${name_random} 
   Input Text       ${contact_last_name}    ${name_random}   
   JS Click    ${preferred_language}
   JS Click   ${last_contact_date}
   ${Yesterday's date}    Yesterday's Date
   Input Text    ${last_contact_date}   ${Yesterday's date}
   JS Click    ${last_contact_date}
   Submit Form and Check Success   

Phone No Not Matching
    Wait Until Element Is Visible    ${phone_no_not_matching}
    JS Click    ${phone_no_not_matching}

Get Contact Name
    ${name_random}    Get Variable Value    ${contact_name_random}
#    ${name_random}     Set Variable     Contact-3bba
    Log         ${name_random}
    [Return]    ${name_random}

Set Contact Name
    ${name_random}  Get Contact Name
    ${contact_created}  Set Variable    //tr[.//td[text()='${name_random}']]
    Log    ${contact_created}
    Set Suite Variable   ${contact_created}
    [Return]    ${contact_created} 
