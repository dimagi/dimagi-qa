from random import choice, shuffle
import datetime
import random
import string
import re

#function to randomly generate household names
def household_name_genrator(prefix_text,total_case_counts):
    case_set=set() #declaring an empty set to store the unique household names

    for i in range(total_case_counts): #loop to generate the household names
        # generating 5 charaters long alphanumeric household  names
        str=''.join(random.choices(string.ascii_letters+string.digits,k=5))

        #adding prefix to the random string: HH_ for household and CL_ for person
        case_set.add(prefix_text+str)
    return case_set

# function to generate registration dates between 01-09-2020 and 01-09-2021
def household_date_of_registration_generator():
    start_date = datetime.date(2020, 9, 1)
    end_date = datetime.date(2021, 9, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date

#function to generate area type from between Urban and Rural
def household_area_generator():
    area_range=['urban','rural']
    random_area=random.choice(area_range)
    return random_area


def dob_generator():
    dob_range=['2021-08-01','2021-04-01','2021-01-01','2020-01-01',
               '2018-01-01','2016-01-01','2010-01-01','2008-01-01',
               '2006-01-01','2000-01-01','1999-01-01','1950-01-01']
    random_dob = random.choice(dob_range)
    return random_dob

def gender_generator():
    gender_range = ['male','female','others']
    gender = random.choice(gender_range)
    return gender

def occupation_generator(age):
    occupation_range=['healthcare_worker', 'law_enforcement_firefighter', 'banker',
                        'manager_admin', 'driver_housekeeping_staff', 'teacher', 'hotelier_airline_personnel',
                        'retail_essentials', 'retail_non_essential',
                        'social_worker_volunteer', 'retired',  'other']
    below_18_range=['student', 'unemployed']
    if age<18:
        occupation=random.choice(below_18_range)
    else:
        occupation = random.choice(occupation_range)

    return occupation

def yes_no_generator():
    choice_range=['yes','no']
    choice=random.choice(choice_range)
    return choice

def pregnancy_status_generator(gender,age):
    choice_range=['yes','no']
    if gender=='male':
        status='no'
    elif gender=='others':
        status='no'
    else:
        if age<15 and gender=='female':
            status='no'
        else:
            status=random.choices(choice_range,weights=[75,25],k=1)
            status=status[0]

    return status

def conditional_vaccine_generator(gender,age,is_pregnant):
    choice_range=['covid_19_astrazeneca','covid_19_covaxin']
    pregnant_choices=['td','td_booster']
    all_conditional_vaccines=''
    if is_pregnant == 'yes':
        vaccine_list = random.choices(pregnant_choices, weights=[50, 50], k=1)
        all_conditional_vaccines = vaccine_list[0]
    elif age>18:
        all_conditional_vaccines='hep_b_adult covid_19_jj'
    elif gender=='female' and (age>=9 and age<=15):
        all_conditional_vaccines='hpv covid_19_sinopharm'
    else:
        all_conditional_vaccines=random.choice(choice_range)

    return all_conditional_vaccines

def vaccine_generator(all_conditional_vaccines,dob):
    choice_ranges= ['BCG','Hepatitis B - Infant','OPV DPT Hepatitis B - Infant','IPV (inactivated Polio Vaccine)',
                    'Haemophilus influenzae type b (Hib)','Pneumococcal (Conjugate)','OPV','Rotavirus',
                    'DPT','Measles','Rubella','DPT Booster','Japanese Encephalitis']

    if dob == '2021-08-01':
        vaccine = random.choice(['BCG', 'IPV (inactivated Polio Vaccine)','Covid-19(Astra Zeneca)','Covid-19(Covaxin)',''])
        if all_conditional_vaccines=='covid_19_covaxin':
            if vaccine=='Covid-19(Astra Zeneca)':
                vaccine = 'Covid-19(Covaxin)'
        elif  all_conditional_vaccines == 'covid_19_astrazeneca':
            if vaccine == 'Covid-19(Covaxin)':
                vaccine = 'Covid-19(Astra Zeneca)'
    elif dob == '2021-04-01':
        vaccine = random.choice(['Hepatitis B - Infant', 'Haemophilus influenzae type b (Hib)','Covid-19(Astra Zeneca)','Covid-19(Covaxin)',''])
        if all_conditional_vaccines == 'covid_19_covaxin':
            if vaccine == 'Covid-19(Astra Zeneca)':
                vaccine = 'Covid-19(Covaxin)'
        elif all_conditional_vaccines == 'covid_19_astrazeneca':
            if vaccine == 'Covid-19(Covaxin)':
                vaccine = 'Covid-19(Astra Zeneca)'
    elif dob == '2021-01-01':
        vaccine = random.choice(['OPV DPT Hepatitis B - Infant', 'Pneumococcal (Conjugate)','Covid-19(Astra Zeneca)','Covid-19(Covaxin)',''])
        if all_conditional_vaccines == 'covid_19_covaxin':
            if vaccine == 'Covid-19(Astra Zeneca)':
                vaccine = 'Covid-19(Covaxin)'
        elif all_conditional_vaccines == 'covid_19_astrazeneca':
            if vaccine == 'Covid-19(Covaxin)':
                vaccine = 'Covid-19(Astra Zeneca)'
    elif dob == '2020-01-01':
        vaccine = random.choice(['OPV', 'Measles','Covid-19(Astra Zeneca)','Covid-19(Covaxin)',''])
        if all_conditional_vaccines == 'covid_19_covaxin':
            if vaccine == 'Covid-19(Astra Zeneca)':
                vaccine = 'Covid-19(Covaxin)'
        elif all_conditional_vaccines == 'covid_19_astrazeneca':
            if vaccine == 'Covid-19(Covaxin)':
                vaccine = 'Covid-19(Astra Zeneca)'
    elif dob == '2018-01-01':
        vaccine = random.choice(['Rotavirus', 'Rubella','Covid-19(Astra Zeneca)','Covid-19(Covaxin)',''])
        if all_conditional_vaccines == 'covid_19_covaxin':
            if vaccine == 'Covid-19(Astra Zeneca)':
                vaccine = 'Covid-19(Covaxin)'
        elif all_conditional_vaccines == 'covid_19_astrazeneca':
            if vaccine == 'Covid-19(Covaxin)':
                vaccine = 'Covid-19(Astra Zeneca)'
    elif dob == '2016-01-01':
        vaccine = random.choice(['DPT', 'DPT Booster','Covid-19(Astra Zeneca)','Covid-19(Covaxin)',''])
        if all_conditional_vaccines == 'covid_19_covaxin':
            if vaccine == 'Covid-19(Astra Zeneca)':
                vaccine = 'Covid-19(Covaxin)'
        elif all_conditional_vaccines == 'covid_19_astrazeneca':
            if vaccine == 'Covid-19(Covaxin)':
                vaccine = 'Covid-19(Astra Zeneca)'
    elif dob == '2008-01-01':
        vaccine = random.choice(['Japanese Encephalitis','Covid-19(Astra Zeneca)','Covid-19(Covaxin)',''])
        if all_conditional_vaccines == 'covid_19_covaxin':
            if vaccine == 'Covid-19(Astra Zeneca)':
                vaccine = 'Covid-19(Covaxin)'
        elif all_conditional_vaccines == 'covid_19_astrazeneca':
            if vaccine == 'Covid-19(Covaxin)':
                vaccine = 'Covid-19(Astra Zeneca)'
    elif all_conditional_vaccines=='hep_b_adult covid_19_jj':
        vaccine=random.choice(['Hepatitis B - Adult Covid-19(J&J)',''])
    elif all_conditional_vaccines=='td':
        vaccine=random.choice(['Tetanus Diptheria',''])
    elif all_conditional_vaccines=='hpv covid_19_sinopharm':
        vaccine=random.choice(['HPV Covid-19(Sinopharm)',''])
    elif all_conditional_vaccines=='td_booster':
        vaccine=random.choice(['Tetanus Diptheria Booster',''])
    elif all_conditional_vaccines=='covid_19_astrazeneca':
        vaccine=random.choice(['Covid-19(Astra Zeneca)',''])
    elif all_conditional_vaccines=='covid_19_covaxin':
        vaccine=random.choice(['Covid-19(Covaxin)',''])
    else:
        vaccine=""

    return vaccine

def dose_generator(vaccines_completed):
    dose=''
    if vaccines_completed=='OPV DPT Hepatitis B - Infant':
        dose='opv_1 opv_2 opv_3 opv_4 dpt_1 dpt_2 dpt_3 hep_b_infant_1 hep_b_infant_2 hep_b_infant_3 measles_1'
    return dose