import json
import csv
import time
import requests
from QA_Requests.Vaccine.Config.config import TestData
from requests.auth import HTTPBasicAuth


def post_form_API(data, url): ## API post method for form submission

        r = requests.post(
            url=url,
            headers=TestData.myHeader,
            data=data,
            auth=HTTPBasicAuth(TestData.name+TestData.credentials, TestData.password))

        if r.status_code == 201:
            print("successful")
        elif r.status_code == 429:
            print(requests.exceptions.RequestException)
            print("Retrying")
            r.close()
            time.sleep(2)
            r = requests.post(
                url=url,
                headers=TestData.myHeader,
                data=data,
                auth=HTTPBasicAuth(TestData.name + TestData.credentials, TestData.password))
            #time.sleep(int(r.headers["Retry_after"]))
            if r.status_code == 201:
                print("successful")
            elif r.status_code == 429:
                print(requests.exceptions.RequestException)
                exit(1)
        result=r.status_code
        print(result)
        return result

def write_person_data(AE_GET_URL,owners_list, output_path): ## API GET method to collect data for Adverse Events forms

    for owner in owners_list:
        r=requests.get(AE_GET_URL+owner+"&limit=5000",headers={"Authorization": "ApiKey "+TestData.UserName+":"+TestData.API_KEY})
        print(r.status_code)
        data = json.loads(r.text)

        for json_data in data["objects"]:
            try: ##collecting the form data and saving in a csv file
                case_id = json_data["case_id"]
                all_conditional_vaccines = json_data["properties"]["all_conditional_vaccines"]
                dob = json_data["properties"]["dob"]
                vaccines_completed = json_data["properties"]["vaccines_completed"]
                date_of_registration = json_data["properties"]["date_of_registration"]

                with open(output_path + '/JSON_Response.csv', 'a+', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    list_response=[owner, case_id, all_conditional_vaccines, dob, vaccines_completed, date_of_registration]
                    writer.writerow(list_response)
            except:
                print("value not present for owner: ", owner)