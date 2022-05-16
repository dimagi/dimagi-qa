*** Settings ***
Library  SeleniumLibrary
Library    String
Library    DateTime
Resource    ../../Base/base.robot 


*** Variables ***

## Case Investigation Form ##

${Case Investigation Form}    //tr[@aria-label='Case Investigation']

${Q:Case Interview Disposition A:Reached person, agreed to call}    //p[text()='Reached person, agreed to call']
${Q:Case Interview Disposition A:Attempted for two days and unable to reach}    //p[text()='Attempted for two days and unable to reach']

${Q:Home/Cell Phone}    //span[text()='Home/Cell Phone']/following::div[1]/div[@class='widget']/descendant::input
${Q:Date Tested}    //p[text()='What date did you get tested?']/following::div[1]/div[@class='widget']/descendant::input
${Q:Preferred Language A:English}    //p[text()='English']

${Q:Search For Address}    //span[text()='Search for Address']/following::div[1]/div[@class='widget']/descendant::input
${Address}     South Side River Bourgeois Road, Subdivision A, Nova Scotia B0E 2X0, Canada
${Fisrt address}    //li[contains(.,'South Side')]

${Q:County of residence}    (//*[contains(text(),'County')])[1]/following::span[@title='Please choose an item'][1]

${A:County of residence}    //label[.//*[contains(text(),'County')]]/following-sibling::div//select
#//*[contains(text(),'County')][1]/following::ul[@role='listbox']/li[1]
${Country success}    (//*[contains(text(),'County')])[1]/following::i[@class="fa fa-check text-success"][1]

${Q:State}    //span[text()='State']/following::span[@title='Please choose an item'][1]
${A:State}    //label[.//*[.='State']]/following-sibling::div//select
#//*[contains(text(),'State')][1]/following::ul[@role='listbox']/li[1]
${State success}    //span[text()='State']/following::i[@class="fa fa-check text-success"][1]

${Q:Zipcode_error}     //label[.//span[text()='Zip Code']]/following-sibling::div//textarea[contains(@data-bind,'value: $data.rawAnswer')]
${Q:Zipcode_normal}     //label[.//span[text()='Zip Code']]/following-sibling::div//textarea
${Zipcode success}    //label[.//span[text()='Zip Code']]/following-sibling::div//i[@class="fa fa-check text-success"]
${Zipcode failure}    //label[.//span[text()='Zip Code']]/following-sibling::div//i[@class="fa fa-warning text-danger clickable"]

${Q:Transer Patient A: No}    //p[contains(.,'No, do not transfer')]

${Q:Activity complete A: Yes}    //span[contains(.,'Is all activity for this case complete')]/following::p[text()='Yes']
${Q:Final Disposition A:Reached, completed investigation}    //p[text()='Reached, completed investigation']

${Q:Gender A:Female}    //p[text()='Female']
${Q:Race A:Asian}    //p[text()='Asian']
${Q:Ethnicity A:Hispanic/Latino}    //p[text()='Hispanic/Latino']
${Submit Form}     //button[@type='submit' and @class='submit btn btn-primary']
${Success Message}    //p[text()='Form successfully saved!']


*** Keywords *** 
    
Open Case Investigation Form
    Sleep    2s
    Wait Until Element Is Enabled    ${Case Investigation Form} 
    JS Click    ${Case Investigation Form} 
    
Fill up and Submit Case Investigation Form
   Open Case Investigation Form
   Wait Until Element Is Enabled    ${Q:Case Interview Disposition A:Reached person, agreed to call}    
   JS Click    ${Q: Case Interview Disposition A:Reached person, agreed to call}
   Add User Details
   ${Yesterday's date}    Yesterday's Date
   Input Text    ${Q:Date Tested}    ${Yesterday's date}
   Add Address
   Submit Form and Check Success
   
Add Address
   # Select Address
   Run Keyword And Ignore Error    Input Text    ${Q:Search For Address}   ${Address}
   Press Keys   ${Q:Search For Address}     ENTER   TAB
#   Click Element    ${Fisrt address}
   Sleep    15s
   # Contry
   Select Dropdown   ${Q:County of residence}    ${A:County of residence}

   # Zipcode
#   Execute JavaScript    window.document.evaluate(${Q:Zipcode_normal}, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollIntoView(true);
   Scroll Element Into View    ${Q:Zipcode_error}
#   Wait Until Element Is Visible    ${Zipcode failure}    80s
   Wait Until Element Is Enabled   ${Q:Zipcode_error}     60s
   Clear Element Text    ${Q:Zipcode_error}
   Press Keys    ${Q:Zipcode_normal}   12345    TAB
   Sleep    10s
   Wait Until Element Is Visible    ${Zipcode success}  60s

   # State
   Select Dropdown   ${Q:County of residence}    ${A:County of residence}
   Select Dropdown    ${Q:State}    ${A:State}
   Transfer Patient - No
   
Transfer Patient - No
   Wait Until Element Is Enabled    ${Q:Transer Patient A: No} 
   Scroll Element Into View    ${Q:Transer Patient A: No}     
   JS Click    ${Q:Transer Patient A: No}
   
Add User Details
   JS Click    ${Q:Preferred Language A:English}
   ${Mobile number}    Generate Mobile Number
   Input Text       ${Q:Home/Cell Phone}     ${Mobile number}
   JS Click    ${Q:Gender A:Female}
   JS Click    ${Q:Race A:Asian}
   JS Click    ${Q:Ethnicity A:Hispanic/Latino} 
    

Unable to reach
   Wait Until Element Is Enabled    ${Q:Case Interview Disposition A:Attempted for two days and unable to reach}    
   JS Click    ${Q:Case Interview Disposition A:Attempted for two days and unable to reach}
   Run Keyword And Ignore Error    Transfer Patient - No
   Submit Form and Check Success 
   
    

Activity for case complete
    Wait Until Element Is Enabled    ${Q:Activity complete A: Yes}     
    JS Click    ${Q:Activity complete A: Yes} 
    Wait Until Element Is Visible    ${Q:Final Disposition A:Reached, completed investigation}
    JS Click    ${Q:Final Disposition A:Reached, completed investigation}
    Run Keyword And Ignore Error    Transfer Patient - No
    Submit Form and Check Success 
