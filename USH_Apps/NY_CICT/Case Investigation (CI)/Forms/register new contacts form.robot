*** Settings ***
Library  SeleniumLibrary
Library    String
Library    DateTime
Resource    ../../Base/base.robot
Resource    ../Menu/menu.robot
Resource    ../../Contact Tracing (CT)/Forms/contact montitoring form.robot


*** Keywords ***

Open Register New Contact(s) Form
    Sleep    5s
    Wait Until Element Is Visible   ${register_new_contacts_form}
    JS Click    ${register_new_contacts_form}

Register New Contacts to Case
    [Arguments]     ${n}    ${name}     ${phone}
    Open Register New Contact(s) Form
    Wait Until Element Is Visible    ${type_of_contact_household}
    JS Click    ${type_of_contact_household}
    Input Text    ${how_many_new_contacts}  ${n}
    Press Keys   ${how_many_new_contacts}   TAB
    FOR    ${i}    IN RANGE   0  ${n}
       ${j}=    Evaluate    ${i} + 1
       ${contact_first_name_loop}=   Catenate    SEPARATOR=     ${contact_first_name}   [    ${j}    ]
       ${contact_last_name_loop}=   Catenate    SEPARATOR=     ${contact_last_name}   [    ${j}    ]
       ${contact_phone_num_loop}=   Catenate    SEPARATOR=     ${contact_phone_num}   [    ${j}    ]
       ${preferred_language_loop}=   Catenate    SEPARATOR=     ${preferred_language}   [    ${j}    ]
       ${last_contact_date_loop}=   Catenate    SEPARATOR=     ${last_contact_date}   [    ${j}    ]

       Scroll Element Into View    ${contact_first_name_loop}
       Input Text       ${contact_first_name_loop}     ${name}_${j}
       Input Text       ${contact_last_name_loop}    ${name}_${j}
       Input Text       ${contact_phone_num_loop}    ${phone}
       JS Click    ${preferred_language_loop}
       JS Click   ${last_contact_date_loop}
       ${Yesterday's date}    Yesterday's Date
       Input Text    ${last_contact_date_loop}    ${Yesterday's date}
       JS Click    ${last_contact_date_loop}
    END
    Submit Form and Check Success

Register contact with given values without index
    [Arguments]  ${name}     ${phone}
    Open Register New Contact without index
    JS Click    ${type_of_contact_household}
    Scroll Element Into View    ${contact_first_name}
    Input Text       ${contact_first_name}     ${name}
    Input Text       ${contact_last_name}    ${name}
    Input Text       ${contact_phone_num}    ${phone}
    JS Click    ${preferred_language}
    JS Click   ${last_contact_date}
    Input Text    ${last_contact_date}    ${Yesterday's date}
    JS Click    ${last_contact_date}
    Submit Form and Check Success


Register New Contacts for Case having address and phone number
    [Arguments]     ${n}    ${generated_names}     ${phone}    ${existing_count}=${EMPTY}   ${address_reset}=no     ${symptomatic}=${EMPTY}    ${mpi_id}=${EMPTY}    ${contact_type}=${EMPTY}   ${without_index}=${EMPTY}

     @{registered_contact_details}=      Create List
     @{name_list}=      Create List
     @{recent_note_list}=      Create List
     @{mph_id_list}=      Create List
     @{contact_monitoring_details}=      Create List
     ${Yesterday's date}    Yesterday's Date
     ${Today's date}     Today's Date
     Set Global Variable    ${Yesterday's date}
     Set Global Variable    ${Today's date}

    Run Keyword And Ignore Error    Open Register New Contact(s) Form
    Run Keyword If    "${without_index}"=="yes"     Open Register New Contact without index

    Input Text    ${how_many_new_contacts}  ${n}
    Press Keys   ${how_many_new_contacts}    TAB
    Contact type selection as per user input       ${contact_type}

    FOR    ${i}    IN RANGE   0  ${n}
       ${j}=    Evaluate    ${i} + 1
       Check Contact header, count and label    ${without_index}    ${existing_count}   ${n}    ${j}
       ${name} =	Get From List	${generated_names}     ${i}
       ${note}=   Catenate    SEPARATOR=-     ${name}   note
       Enter Contact Details    ${j}    ${name}     ${phone}    ${note}     ${address_reset}    ${symptomatic}    ${mpi_id}    ${without_index}

       Collections.Append To List    ${name_list}   ${name}
       Collections.Append To List    ${recent_note_list}   ${note}
       Collections.Append To List    ${mph_id_list}   ${mpi_id}
       Collections.Append To List    ${contact_monitoring_details}   ${name}    ${email}    English     ${Yesterday's date}    ${phone}
       Collections.Append To List    ${registered_contact_details}  ${name_list}   ${recent_note_list}  ${mph_id_list}  ${contact_monitoring_details}
    END
    Submit Form and Check Success
    [Return]    @{registered_contact_details}

Check Contact ID is Alphanum
    [Arguments]     ${id}
    ${contact_id}        Get Text   ${id}
    ${true_or_false}     Check Contact ID   ${contact_id}
    Should Be True   ${true_or_false} == True
    [Return]    ${contact_id}

Get Text From Element
     [Arguments]     ${element}
     Wait Until Element Is Visible    ${element}
     Wait Until Element Is Enabled    ${element}
     ${fetched_string}      Get Text   ${element}
     ${value}   Get String    ${fetched_string}
     [Return]   ${value}


Check Count of Element
    [Arguments]     ${n}    ${element}
    ${count} =  Get Element Count   ${element}
    Should Be True  ${count} == ${n}


Check Already Registered Contacts
    [Arguments]     ${loop_count}   ${master_list}
    Open Register New Contact(s) Form
    Sleep    5s
    FOR    ${i}    IN RANGE   0  ${loop_count}
        ${loop_count}=    Evaluate    ${i} + 1
        Log      ${master_list}
        ${name_list} =   Get From List  ${master_list}  0
        #Reverse List    ${name_list}
        ${recent_note_list} =   Get From List  ${master_list}  1
        #Reverse List    ${recent_note_list}
        ${mph_id_list} =   Get From List  ${master_list}  2
        #Reverse List    ${mph_id_list}
        ${name_element_in_list} =	Get From List	${name_list}     ${i}
        ${note_element_in_list} =	Get From List	${recent_note_list}     ${i}
        ${mph_element_in_list} =	Get From List	${mph_id_list}     ${i}

        ${already_registered_contact_name_loop}=   Catenate    SEPARATOR=     ${already_registered_contact_name}   [    ${loop_count}    ]
        ${already_registered_most_recent_note_loop}=   Catenate    SEPARATOR=     ${already_registered_most_recent_note}   [    ${loop_count}    ]
        ${already_registered_mph_id_loop}=   Catenate    SEPARATOR=     ${contact_id}   [    ${loop_count}    ]

        # Checking if Contact Name is same as registered
        ${contact_name}   Get Text From Element     ${already_registered_contact_name_loop}
        Should Contain    ${contact_name}   ${name_element_in_list}
        # Checking if Note is same as registered
        ${note}  Get Text   ${already_registered_most_recent_note_loop}
        Should Contain  ${note}     ${note_element_in_list}
        # Checking mph id
        ${mph_id}  Get Text   ${already_registered_mph_id_loop}
        Should Contain  ${mph_id}     ${mph_element_in_list}
    END

Check Registered Contact Details on Contact Monitoring
    [Arguments]       ${master_list}=${EMPTY}    ${check}=${EMPTY}
    Open Contact Monitoring Form
    Sleep    5s
    Log      ${master_list}

    IF  "${check}"=="without_index_traveler"
        ${contact_details_contact_type_value}     Get Text From Element   ${contact_details_contact_type}
        ${contact_details_exposure_date_value}    Get Text From Element   ${contact_details_exposure_date}
        ${Yesterday's date}     Yesterday's Date
        Should Contain    ${contact_details_exposure_date_value}    ${Yesterday's date}
        Should Contain    ${contact_details_contact_type_value}     NYS resident
    ELSE
        ${contact_monitoring_details} =   Get From List  ${master_list}  3
        ${contact_info_contact_name_value} =	Get From List	${contact_monitoring_details}     0
        ${contact_info_email_value} =	Get From List	${contact_monitoring_details}     1
        ${contact_info_language_value}=	Get From List	${contact_monitoring_details}     2
        ${contact_info_last_exposure_value}=	Get From List	${contact_monitoring_details}     3
        ${contact_info_phone_num_value}=	Get From List	${contact_monitoring_details}     4

        # Checking if Contact Name is same as registered
        ${contact_info_contact_name}   Get Text From Element     ${contact_info_contact_name}
        Should Contain   ${contact_info_contact_name}   ${contact_info_contact_name_value}
        # Checking if Contact Language is same as registered
        ${contact_info_language}   Get Text From Element     ${contact_info_language}
        Should Contain    ${contact_info_language}  ${contact_info_language_value}
        # Checking if Contact's Last Exposure is same as registered
        ${contact_info_last_exposure}   Get Text From Element     ${contact_info_last_exposure}
        Should Contain   ${contact_info_last_exposure}  ${contact_info_last_exposure_value}
        # Checking if Contact's Phone Number is same as registered
        ${contact_info_phone_num}   Get Text From Element     ${contact_info_phone_num}
        Should Contain    ${contact_info_phone_num}     ${contact_info_phone_num_value}
    END



Enter Contact Details
    [Arguments]     ${loop_count}   ${name}     ${phone}    ${note}    ${address_reset}=no  ${symptomatic}=${EMPTY}    ${mpi_id}=${EMPTY}   ${without_index}=${EMPTY}


       ${contact_first_name_loop}=   Catenate    SEPARATOR=     ${contact_first_name}   [    ${loop_count}    ]
       ${contact_last_name_loop}=   Catenate    SEPARATOR=     ${contact_last_name}   [    ${loop_count}    ]
       ${number_same_loop}=   Catenate    SEPARATOR=     ${number_same}   [    ${loop_count}    ]
       ${contact_phone_num_loop}=   Catenate    SEPARATOR=     ${contact_phone_num}   [    ${loop_count}    ]
       ${email_id_loop}=   Catenate    SEPARATOR=     ${email_id}   [    ${loop_count}    ]
       ${contact_id_loop}=   Catenate    SEPARATOR=     ${contact_id}   [    ${loop_count}    ]
       ${contact_id_without_index_loop}=   Catenate    SEPARATOR=     ${contact_id_without_index}   [    ${loop_count}    ]
       ${preferred_language_loop}=   Catenate    SEPARATOR=     ${preferred_language}   [    ${loop_count}    ]
       ${last_contact_date_loop}=   Catenate    SEPARATOR=     ${last_contact_date}   [    ${loop_count}    ]
       ${add_note_loop}=   Catenate    SEPARATOR=     ${add_note}   [    ${loop_count}    ]
       ${address_same_yes_loop}=   Catenate    SEPARATOR=     ${address_same_yes}   [    ${loop_count}    ]
       ${address_same_no_loop}=   Catenate    SEPARATOR=     ${address_same_no}   [    ${loop_count}    ]
       ${address_value_loop}=   Catenate    SEPARATOR=     ${address_value}   [    ${loop_count}    ]
       ${mph_id_loop}=   Catenate    SEPARATOR=     ${contact_id}   [    ${loop_count}    ]


       Scroll Element Into View    ${contact_first_name_loop}
       Input Text       ${contact_first_name_loop}     ${name}
       Input Text       ${contact_last_name_loop}    ${name}
       Run Keyword And Ignore Error    JS Click    ${number_same_loop}
       Run Keyword And Ignore Error    Input Text       ${contact_phone_num_loop}    ${phone}
       Input Text       ${email_id_loop}    ${email}
       Log     ${mpi_id}

       IF   "${mpi_id}" == "${EMPTY}" and "${without_index}" == "${EMPTY}"
             ${contact_or_mph_id}    Check Contact ID is Alphanum    ${contact_id_loop}
       ELSE IF  "${mpi_id}" != "${EMPTY}" and "${without_index}" == "${EMPTY}"
            ${mph_id_element_value}        Get Text From Element   ${mph_id_loop}
            ${mph_id_updated_value}=   Catenate    SEPARATOR=     ${mph_id_element_value}-00    ${loop_count}
            Should Contain   ${mph_id_updated_value}     ${mpi_id}
       ELSE
            ${contact_or_mph_id}     Check Contact ID is Alphanum    ${contact_id_without_index_loop}
       END
       JS Click    ${preferred_language_loop}
       Input Text    ${add_note_loop}   ${note}
       IF    "${address_reset}" == "no" and "${without_index}" == "${EMPTY}"
             JS Click     ${address_same_yes_loop}
             ${address}   Get Text    ${address_value_loop}
             Should Contain   ${address}  South Side River Bourgeois Road
       ELSE IF      "${address_reset}" == "yes" and "${without_index}" == "${EMPTY}"
            JS Click     ${address_same_no_loop}
            Change Address
       ELSE IF  "${address_reset}" == "blank" and "${without_index}" == "${EMPTY}"
            JS Click     ${address_same_no_loop}
       ELSE
            Log     Without Index so adding no address
       END
       Run Keyword And Ignore Error  Input Text    ${last_contact_date_loop}    ${Yesterday's date}
       Run Keyword If    "${symptomatic}" == "yes"  JS Click    ${symptomatic_yes}

Generate Contact New Names
    [Arguments]     ${n}
    @{new_name_list}=      Create List

    FOR    ${i}    IN RANGE   0  ${n}
        ${j}=    Evaluate    ${i} + 1
        ${contact_name}  Generate Random Contact Name
        Collections.Append To List    ${new_name_list}   ${contact_name}
    END
    [Return]     ${new_name_list}

Contact type selection as per user input
    [Arguments]     ${contact_type}
    IF    "${contact_type}" == "international_travel"
        JS Click    ${type_of_contact_international_traveller}
        Scroll Element Into View    ${arrival_date_in_us}
        Input Text    ${arrival_date_in_us}    ${Today's date}
        JS Click    ${calendar_close}
    ELSE IF     "${contact_type}" == "visitor_traveling"
        JS Click    ${type_of_contact_visitor_traveling}
        Input Text    ${Date_last_impacted_states}    ${Yesterday's date}
        #JS Click    ${calendar_close}
        Select Dropdown    ${state_traveled_from}    ${state_traveled_from_select}
        JS Click    ${transportation_airline}
        Input Text    ${airline}    ABC
        Input Text  ${date_of_flight}   ${Yesterday's date}
        JS Click    ${calendar_close}
    ELSE IF     "${contact_type}" == "ooj_case"
        JS Click    ${type_of_contact_ooj_case}
        Element Should Not Be Visible   ${Date_last_impacted_states}
        Element Should Not Be Visible   ${state_traveled_from}
        Element Should Not Be Visible   ${transportation_airline}
        Element Should Not Be Visible   ${airline}
        Element Should Not Be Visible   ${date_of_flight}
    ELSE
        JS Click    ${type_of_contact_household}
    END

Check Contact header, count and label
     [Arguments]    ${without_index}    ${existing_count}   ${n}    ${j}
     IF    "${existing_count}" == "${EMPTY}" and "${without_index}"=="yes"
            Wait Until Keyword Succeeds  3x  500ms   Element Should Be Visible    //h2[text()='Contact ${j}']
     ELSE IF    "${existing_count}" != "${EMPTY}" and "${without_index}"=="yes"
                ${incremented_j}=    Evaluate    ${existing_count} + 1
                Run Keyword And Continue On Failure     Element Should Be Visible  //h2[text='Contact${incremented_j}']
     ELSE IF    "${existing_count}" == "${EMPTY}" and "${without_index}"!="yes"
                Element Should Be Visible    ${close_contacts_header}
                Element Should Not Be Visible    ${already_registered_label}
                Element Should Be Visible    //h2[text()='Close Contact ${j}']
                Check Count of Element   ${n}    ${contact_id}
     ELSE
            Element Should Be Visible    ${close_contacts_header}
            ${incremented_j}=    Evaluate    ${existing_count} + 1
            Run Keyword And Continue On Failure     Element Should Be Visible    //h2[text()='Close Contact ${incremented_j}']
            Run Keyword And Continue On Failure     Check Count of Element   ${incremented_j}    ${contact_id}
     END

Search and Select the contact created
    [Arguments]     ${contact_names}    ${index}=0
    ${contact_name} =	Get From List	${contact_names}     ${index}
    ${contact_created}     Set Variable    //tr[.//td[text()='${contact_name}']]
    Sleep    80s
    Case Search     ${contact_name}
    Search in the case list     ${contact_name}
    Select Created Case    ${contact_created}
    [Return]    ${contact_created}

Search the contact created
    [Arguments]     ${contact_names}
    ${contact_name} =	Get From List	${contact_names}     0
    ${contact_created}     Set Variable    //tr[.//td[text()='${contact_name}']]
    Sleep    80s
    Case Search     ${contact_name}
    Search in the case list     ${contact_name}
    [Return]    ${contact_created}






