*** Settings ***
Library  SeleniumLibrary
Library    String
Library    DateTime
Resource    ../../Base/base.robot


*** Variables ***

## Assign or Reassign Cases Form ##
${Assign or Reassign Case Form}    //tr[@aria-label='Assign or Reassign the Case']
${Permanently assign}    //p[contains(.,'Permanently assign the case to a different staff member')]
${Q:Permanently reassign to}    //span[text()='Permanently reassign case to this staff member']/following::span[@title='Please choose an item'][1]
${A:Permanently reassign to}   //li[contains(.,'CI 1')]
${A:Permanently reassign to poc}   //li[contains(.,'CI')]
${A:Permanently unassign}    //p[contains(.,'Unassign the case from its current primary owner')]
${Submit Form}     //button[@type='submit' and @class='submit btn btn-primary']
${Success Message}    //p[text()='Form successfully saved!']


*** Keywords ***
    
Open Assign or Reassign Case Form
    Sleep    2s
    Wait Until Element Is Enabled    ${Assign or Reassign Case Form} 
    JS Click    ${Assign or Reassign Case Form}
    
Permanently Assign to Self
    Open Assign or Reassign Case Form 
    Wait Until Element Is Enabled    ${Permanently assign}  
    JS Click    ${Permanently assign} 
    Execute JavaScript    window.scrollBy(900, 900);
    IF  "${domain}"=="ny-staging-cdcms"
    Answer Dropdown    ${Q:Permanently reassign to}    ${A:Permanently reassign to}
    ELSE
    Answer Dropdown    ${Q:Permanently reassign to}    ${A:Permanently reassign to poc}
    END
    Submit Form and Check Success 

Unassign from Self
    Open Assign or Reassign Case Form  
    Wait Until Element Is Enabled    ${A:Permanently unassign}  
    JS Click    ${A:Permanently unassign} 
    Submit Form and Check Success 


    
   