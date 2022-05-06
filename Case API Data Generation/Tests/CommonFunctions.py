import datetime
from datetime import date

def age_calculator(dob): ## to calculate person age depending on dob
    today = date.today()
    born = datetime.datetime.strptime(dob, "%Y-%m-%d")

    age=today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    return age
