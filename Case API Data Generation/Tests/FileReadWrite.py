import csv
import datetime
import pandas as pd

def read_owner_id(loc):

    #reading values from input CSV file and storing in a dictionary
     with open(loc) as f:
        next(f)  # Skip the header
        inputCSV = csv.reader(f, skipinitialspace=True)
        owner_dict = dict(inputCSV)

    #converting the dictionary values from string to int
     for owner in owner_dict:
        owner_dict[owner] = int(owner_dict[owner])

    #returning the final dictionary to the main program
     return owner_dict

def write_instanceids_to_csv(instance_id_list,output_path,output_filename):
    ## function to generate the instance_ids and write them to the input csv file
    filename=''
    if output_filename == None:
        filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        with open(output_path+'/InstanceID_'+filename+'.csv', 'w', newline='') as csvfile: #creating the output files
           #defining the headers
            fieldnames = ['instanceID']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            #writing the header to the files
            writer.writeheader()

            for instances in instance_id_list:
                writer.writerow({'instanceID':instances})

    else:
        filename=output_filename
        sample = pd.read_csv(output_path +'/'+ filename+'.csv')
        sample['instanceID'] = instance_id_list
        sample.drop(sample.filter(regex="Unname"), axis=1, inplace=True)
        sample.to_csv(output_path +'/'+ filename+'.csv', index=False)

    print('Instance IDs successfully generated.')


def write_caseids_to_csv(instance_id_list,output_path,output_filename):
    ## function to generate the instance_ids and write them to the input csv file
    filename=''
    if output_filename == None:
        filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        with open(output_path+'/caseID_'+filename+'.csv', 'w', newline='') as csvfile: #creating the output files
           #defining the headers
            fieldnames = ['case_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            #writing the header to the files
            writer.writeheader()

            for instances in instance_id_list:
                writer.writerow({'case_id':instances})

    else:
        filename=output_filename
        sample = pd.read_csv(output_path +'/'+ filename+'.csv')
        sample['case_id'] = instance_id_list
        sample.drop(sample.filter(regex="Unname"), axis=1, inplace=True)
        sample.to_csv(output_path +'/'+ filename+'.csv', index=False)

    print('Case IDs successfully generated.')


def add_owners_to_csv(owner_dict,owner_list,output_path):
    filename='Form_Input_VSM'
    with open(output_path + '/'+filename+'.csv', 'w',
              newline='') as csvfile:  # creating the output files
        # defining the headers
        fieldnames = ['owner_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # writing the header to the files
        writer.writeheader()
        for owners in owner_list:
            count=owner_dict[owners]

            for n in range(count):
                writer.writerow({'owner_id': owners})

    return filename


