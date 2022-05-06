import csv
from pandas import *
import math

from Tests.RandomStringGenerator import *
from Tests.CommonFunctions import age_calculator

def create_household_data(output_path,owner,household_counts,case_name_list):

    with open(output_path+'/'+owner+'.csv', 'w', newline='') as csvfile: #creating the output files
       #defining the headers
        fieldnames = ['external_id','owner_id', 'vaccination_centre_id', 'household_name', 'case_name', 'household_date_of_registration', 'household_area_urban_rural']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #writing the header to the files
        writer.writeheader()

        #loop to write data for each owner
        for cases in range(household_counts):
            # getting the household_name from the already generated list and removing the same from the list
            # so that their is no repeatations and the names are unique

            random_case = case_name_list.pop(0) if case_name_list else False
            #generating the registration dates
            household_reg_date = household_date_of_registration_generator()
            #generation the household area
            household_area = household_area_generator()

            #writing all the values generated to the file
            writer.writerow({'external_id':random_case,'owner_id': owner, 'vaccination_centre_id': owner,
                             'household_name': random_case, 'case_name':random_case,
                             'household_date_of_registration': household_reg_date,
                             'household_area_urban_rural': household_area})

    print('File: '+owner+'.csv successfully generated.')


def create_person_data(output_path,owner,household_counts,case_name_list,parent_id_list):

    with open(output_path+'/'+owner+'.csv', 'w', newline='') as csvfile: #creating the output files
       #defining the headers
        fieldnames = ['external_id','case_name', 'date_of_registration', 'dob', 'dummy_cp', 'gender', 'occupation',
                      'owner_id','vaccination_centre_id','whether_commorbidities','is_pregnant',
                      'all_conditional_vaccines','vaccines_completed','all_dose_id_administered',
                      'parent_type','parent_external_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #writing the header to the files
        writer.writeheader()

        #loop to write data for each owner
        for cases in range(household_counts):
            # getting the househol_name from the already generated list and removing the same from the list
            # so that their is no repeatations and the names are unique

            random_case_name = case_name_list.pop(0) if case_name_list else False
            #generating the registration dates
            date_of_registration = household_date_of_registration_generator()
            dob = dob_generator()
            age=age_calculator(dob)
            dummy_cp="All Vaccines"
            gender=gender_generator()
            occupation=occupation_generator(age)
            owner_id=owner
            vaccination_centre_id=owner
            whether_commorbidities=yes_no_generator()
            is_pregnant=pregnancy_status_generator(gender,age)
            all_conditional_vaccines=conditional_vaccine_generator(gender,age,is_pregnant)
            vaccines_completed=vaccine_generator(all_conditional_vaccines,dob)
            all_dose_id_administered=dose_generator(vaccines_completed)
            parent_type="household"
            parent_external_id=parent_id_list.pop(0) if case_name_list else False

            #generation the household area
            household_area = household_area_generator()

            #writing all the values generated to the file
            writer.writerow({'external_id':random_case_name,'case_name':random_case_name, 'date_of_registration':date_of_registration,
                             'dob':dob, 'dummy_cp':dummy_cp, 'gender':gender, 'occupation':occupation,
                             'owner_id':owner_id,'vaccination_centre_id':vaccination_centre_id,
                             'whether_commorbidities':whether_commorbidities,
                             'is_pregnant':is_pregnant,'all_conditional_vaccines':all_conditional_vaccines,
                             'vaccines_completed':vaccines_completed,'all_dose_id_administered':all_dose_id_administered,
                             'parent_type':parent_type,'parent_external_id':parent_external_id
                             })

    print('File: '+owner+'.csv successfully generated.')

def create_parent_external_id_list(household_output_path1, owner, person_case_counts):
    file = read_csv(household_output_path1+'/'+owner+'.csv')

    # creating empty lists
    case_names = file['household_name'].tolist()
    
    household_count=len(case_names)
    total_count=person_case_counts/household_count
    new_case_name_list=case_names * math.ceil(total_count)

    return  new_case_name_list

