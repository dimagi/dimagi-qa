*** Settings ***
Library  SeleniumLibrary
Library    String
Library    DateTime
Resource    ../../Base/base.robot


*** Variables ***

## Assign or Reassign Contacts Form ##
${Assign or Reassign Contact Form}    //tr[contains(@aria-label,'Assign or Re')]
${Permanently assign}    //p[contains(.,'Permanently assign')]
${Q:Permanently reassign to}    //span[contains(text(),'Permanently reassign')]/following::span[@title='Please choose an item'][1]
${A:Permanently reassign to}   //li[contains(.,'CT 1')]
${A:Permanently reassign to poc}   //li[contains(.,'CT')]
${A:Permanently unassign}    //p[contains(.,'from its current primary owner')]
${Submit Form}     //button[@type='submit' and @class='submit btn btn-primary']
${Success Message}    //p[text()='Form successfully saved!']


*** Keywords ***
    
Open Assign or Reassign Contact Form
    Sleep    2s
    Wait Until Element Is Enabled    ${Assign or Reassign Contact Form} 
    JS Click    ${Assign or Reassign Contact Form} 
    
Permanently Assign to Self (CM)
    Open Assign or Reassign Contact Form
    Wait Until Element Is Enabled    ${Permanently assign}  
    JS Click    ${Permanently assign} 
    Execute JavaScript    window.scrollBy(900, 900);
    IF  "${domain}"=="ny-staging-cdcms"
    Answer Dropdown    ${Q:Permanently reassign to}    ${A:Permanently reassign to}
    ELSE
    Answer Dropdown    ${Q:Permanently reassign to}    ${A:Permanently reassign to poc}
    END
    Submit Form and Check Success 

Unassign from Self (CM)
    Open Assign or Reassign Contact Form  
    Wait Until Element Is Enabled    ${A:Permanently unassign}  
    JS Click    ${A:Permanently unassign} 
    Submit Form and Check Success 


    
   