import csv
import os.path
import time

from Config.config import TestData
from Tests.APITests import write_person_data
from Tests.DataFileCreation import create_household_data, create_person_data, create_parent_external_id_list
from Tests.FileReadWrite import *
from Tests.FormCreation import create_forms, submit_forms
from Tests.RandomFormValueGenerator import *
from Tests.RandomStringGenerator import household_name_genrator


class DataCreation:
    case_name_list = list()  # declaring an empty list for the randomly generated case names
    person_case_name_list = list()
    original_case_names_household = list()

    def gsheet_integration(input_file, input_xml, output_path):
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        with open(output_path + '/Responses.csv', 'w', newline='') as csvfile:  # creating the output files
            # defining the headers
            fieldnames = ['volume', 'vol1','vol2','vol3','vol4','base','case_id', 'instanceID', 'result']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # writing the header to the files
            writer.writeheader()

        with open(output_path + '/CaseAPI.csv', 'w', newline='') as csvfile:  # creating the output files
            # defining the headers
            fieldnames = ['volume', 'count','case_id', 'instanceID']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # writing the header to the files
            writer.writeheader()

        # reading the data from the input file as a dictionary
        owner_form_dict = read_owner_id(input_file)

        # counting total rows of volumes in the input sheet
        total_owners = len(owner_form_dict)
        print("Total Owners in the list: ", total_owners)

        # storing the dictionary keys in a list and creating a list of all volume
        owner_list = owner_form_dict.keys()

        # calculating the total sum of the api cases
        total_case_counts = sum(owner_form_dict.values())
        print(total_case_counts)

        instance_id_list = list(instance_id_generator(total_case_counts))
        write_instanceids_to_csv(instance_id_list, output_path, 'CaseAPI')

        case_id_list = list(instance_id_generator(total_case_counts))
        write_caseids_to_csv(case_id_list, output_path, 'CaseAPI')
        # print(instance_id_list)
        # loop to generate the test outputs
        for owner in owner_list:
            vol_counts = owner_form_dict[owner]
            # if not os.path.isdir(output_path + '/' + owner):
            #     os.mkdir(output_path + '/' + owner)
            # calling the function to create the output files
            create_forms(output_path, input_xml, owner, vol_counts, instance_id_list, case_id_list)
        print("All forms data successfully generated.")

        for owner in owner_list:
            vol_counts = owner_form_dict[owner]
            # if not os.path.isdir(output_path + '/' + owner):
            #     os.mkdir(output_path + '/' + owner)
            # calling the function to create the output files
            submit_forms(output_path, vol_counts, input_xml, owner)
        print("All forms successfully submitted")

    if __name__ == '__main__':
        start_time = time.time()
        # calling the function to generate Household files
        if TestData.scenario_type == "CaseAPI":
            gsheet_integration(TestData.input_file_path, TestData.input_xml_path, TestData.output_path)
        else:
            print("Scenario Type is not provided in the config file")

        end_time = time.time()
        print("Total time taken to execute the code: ", end_time - start_time)
        # create_household1()
