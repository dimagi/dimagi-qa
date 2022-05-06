import time
import csv
import xml.etree.ElementTree as ET
from Tests.RandomFormValueGenerator import *
from Tests.APITests import post_form_API
from Config.config import TestData


def submit_forms(output_path, form_counts, input_xml, owner):
    tree = ET.parse(input_xml)
    root = tree.getroot()

    XML_TEMPLATE = ET.tostring(root, encoding='unicode')
    # for vol in range(owner):
    with open(output_path + '/Volume_' + owner + '.csv', 'r') as read_obj:
            csv_dict_reader = csv.DictReader(read_obj)
            for row in csv_dict_reader:
                # generating the data
                volume = row['volume']
                vol1 = row['vol1']
                vol2 = row['vol2']
                vol3 = row['vol3']
                vol4 = row['vol4']
                base = row['base']
                case_id = row['case_id']
                instanceID = row['instanceID']

                # print(volume, vol1, vol2, vol3, vol4, base, case_id,instanceID)
                xml_string = XML_TEMPLATE.format(vol1=vol1,
                                                 vol2=vol2, vol3=vol3, vol4=vol4,
                                                 base=base, case_id=case_id, instanceID=instanceID)

                # print(form_index, xml_string)
                # calling API Post method
                result = post_form_API(xml_string, TestData.API_POST_URL, TestData.name)


                # code to write xml string to xml files
                with open(output_path + '/' + instanceID + '.xml', "wb") as f:
                    f.write(xml_string.encode('UTF-8'))
                    tree.write(output_path + '/' + instanceID + '.xml', default_namespace=None)
                print(owner + '_' + instanceID + '.xml created successfully.')

                # writing responses to csv file

                with open(output_path + '/Responses.csv', 'a+', newline='') as csvfile:
                   writer = csv.writer(csvfile)
                   list_response=[volume,vol1,vol2,vol3,vol4,base,case_id, instanceID, result]
                   writer.writerow(list_response)
                print(volume, vol1,vol2,vol3,vol4,base,case_id, instanceID, result)


def create_forms(output_path, input_xml, owner, form_counts, instance_id_list, case_id_list):
    with open(output_path + '/Volume_' + owner + '.csv', 'w', newline='') as csvfile:  # creating the output files
        # defining the headers
        fieldnames = ['volume', 'vol1', 'vol2', 'vol3', 'vol4', 'base', 'case_id', 'instanceID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writing the header to the files
        writer.writeheader()

        for form_index in range(form_counts):
            # generating the data

            vol1 = volume1_assignment(owner)
            vol2 = volume2_assignment(owner)
            vol3 = volume3_assignment(owner)
            vol4 = volume4_assignment(owner)
            base = ""
            instanceID = instance_id_list.pop(0) if instance_id_list else False
            case_id = case_id_list.pop(0) if instance_id_list else False

            writer.writerow({'volume': owner, 'vol1': vol1,
                             'vol2': vol2, 'vol3': vol3,
                             'vol4': vol4, 'base': base,
                             'case_id': case_id, 'instanceID': instanceID})
