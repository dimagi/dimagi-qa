from random import choice, shuffle
import datetime
import random
import string
import re
import uuid
import pandas as pd

def instance_id_generator(total_case_counts):
    id_set=set() #declaring an empty set to store the unique household names

    for i in range(total_case_counts): #loop to generate the household names
        # generating 5 charaters long alphanumeric household  names
        ids=str(uuid.uuid4())

        #adding prefix to the random string: HH_ for household and CL_ for person
        id_set.add(ids)
    return id_set

def volume_generator(volume):
    print(volume)
    volume_value = ''
    if volume == 1:
        volume_value = "a"
    elif volume == 2:
        volume_value = "b"
    elif volume == 3:
        volume_value = "c"
    elif volume == 4:
        volume_value = "d"
    print(volume_value)
    return volume_value

def volume1_assignment(volume):
    print(volume)
    vol1 = ''
    if volume == 'a':
        vol1='a'
    else:
        vol1=''
    print(vol1)
    return vol1

def volume2_assignment(volume):
    print(volume)
    vol2 = ''
    if volume == 'b':
        vol2='b'
    else:
        vol2=''
    print(vol2)
    return vol2

def volume3_assignment(volume):
    print(volume)
    vol3 = ''
    if volume == 'c':
        vol3='c'
    else:
        vol3=''
    print(vol3)
    return vol3

def volume4_assignment(volume):
    print(volume)
    vol4 = ''
    if volume == 'd':
        vol4='d'
    else:
        vol4=''
    print(vol4)
    return vol4