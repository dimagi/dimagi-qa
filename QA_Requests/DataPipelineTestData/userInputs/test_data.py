"""Static inputs for the QA-8710 household test data generator.

Everything that describes the "Household Registration" app (form xmlns, case type,
choice values) lives here so the generator and form builder never hardcode it.
Choice values must match the app's form definitions exactly.
"""


class TestData:
    output_path = "./OutputFiles"

    case_type = "household"
    device_id = "qa-8710-data-generator"
    app_version_label = "QA-8710 data generator"

    register_xmlns = "http://openrosa.org/formdesigner/91F832DD-8E0A-4AE1-8BDE-E78B232DF8B3"
    followup_xmlns = "http://openrosa.org/formdesigner/EDD07781-622E-45A0-ABCB-8468B502C5E1"
    close_xmlns = "http://openrosa.org/formdesigner/EFF3F078-EF4F-4636-B988-350A875E4905"

    register_form_name = "Register Household"
    followup_form_name = "Household Follow-up Visit"
    close_form_name = "Close Household"


class Places:
    # village value -> district value, made-up centre point and a local "profile"
    # that skews water source / electricity so villages look different in exports.
    villages = {
        "riverbend": {"district": "eastern", "gps": (-13.9124, 27.6418), "electricity": 0.35,
                      "water": {"piped": 5, "borehole": 25, "protected_well": 20, "unprotected_well": 10,
                                "rainwater": 5, "surface_water": 35}},
        "kasama_hills": {"district": "northern", "gps": (-13.7581, 27.5032), "electricity": 0.25,
                         "water": {"piped": 3, "borehole": 40, "protected_well": 25, "unprotected_well": 20,
                                   "rainwater": 7, "surface_water": 5}},
        "lindale": {"district": "central", "gps": (-13.9850, 27.4710), "electricity": 0.70,
                    "water": {"piped": 45, "borehole": 30, "protected_well": 15, "unprotected_well": 5,
                              "rainwater": 3, "surface_water": 2}},
        "mapleford": {"district": "central", "gps": (-14.0412, 27.5566), "electricity": 0.60,
                      "water": {"piped": 35, "borehole": 35, "protected_well": 15, "unprotected_well": 8,
                                "rainwater": 5, "surface_water": 2}},
        "northfield": {"district": "northern", "gps": (-13.7012, 27.6125), "electricity": 0.30,
                       "water": {"piped": 5, "borehole": 35, "protected_well": 30, "unprotected_well": 15,
                                 "rainwater": 10, "surface_water": 5}},
        "sunvale": {"district": "southern", "gps": (-14.2033, 27.4458), "electricity": 0.45,
                    "water": {"piped": 15, "borehole": 40, "protected_well": 20, "unprotected_well": 10,
                              "rainwater": 10, "surface_water": 5}},
        "westbrook": {"district": "southern", "gps": (-14.1546, 27.3381), "electricity": 0.40,
                      "water": {"piped": 10, "borehole": 30, "protected_well": 25, "unprotected_well": 15,
                                "rainwater": 5, "surface_water": 15}},
        "oakridge": {"district": "eastern", "gps": (-13.8777, 27.7590), "electricity": 0.20,
                     "water": {"piped": 2, "borehole": 35, "protected_well": 25, "unprotected_well": 25,
                               "rainwater": 8, "surface_water": 5}},
    }


class Distributions:
    # household size 1..12
    household_size = {1: 4, 2: 8, 3: 12, 4: 15, 5: 16, 6: 14, 7: 11, 8: 8, 9: 5, 10: 3, 11: 2, 12: 2}
    children_under_5 = {0: 45, 1: 33, 2: 17, 3: 5}
    livelihood_count = {1: 55, 2: 35, 3: 10}
    livelihoods = {"farming": 40, "livestock": 20, "trading": 18, "wage_labour": 15, "fishing": 5, "other": 4}
    head_gender = {"female": 48, "male": 52}

    household_size_change = {-1: 10, 0: 80, 1: 10}
    attended_training = 0.35
    training_topic = {"savings_group": 30, "agriculture": 30, "water_sanitation": 15,
                      "financial_literacy": 15, "business_skills": 10}
    visit_notes_blank = 0.35

    # share of cases that get 1 or 2 follow-up visits, and that are later closed
    one_followup = 0.40
    two_followups = 0.15
    closed = 0.04
    close_reason = {"moved_away": 55, "duplicate": 15, "declined": 20, "other": 10}

    # uneven split of households across the mobile workers, in settings order
    worker_weights = [26, 22, 20, 18, 14]


class Names:
    female = [
        "Abena", "Achieng", "Adaeze", "Aisha", "Akosua", "Alinta", "Amara", "Amina", "Ana", "Anjali",
        "Asha", "Beatriz", "Busisiwe", "Chanda", "Chiamaka", "Chipo", "Dalia", "Deepa", "Efua",
        "Esi", "Esther", "Fatima", "Florence", "Grace", "Hadiza", "Halima", "Imani", "Ines", "Jamila",
        "Kavita", "Khadija", "Lerato", "Lina", "Lucia", "Lydia", "Mariam", "Martha", "Mercy",
        "Monica", "Mwila", "Nadia", "Naledi", "Nandi", "Neema", "Nia", "Nomvula", "Nuru", "Patience",
        "Priya", "Rehema", "Rosa", "Ruth", "Sabina", "Salma", "Sara", "Selam", "Thandiwe", "Tiwonge",
        "Wanjiru", "Yaa", "Zainab", "Zawadi", "Zodwa",
    ]
    male = [
        "Abdul", "Adebayo", "Ahmed", "Amani", "Arjun", "Baraka", "Bongani", "Bwalya", "Carlos", "Chidi", "Chinedu",
        "Daniel", "David", "Emeka", "Emmanuel", "Fikru", "Francis", "Gabriel", "Hamisi", "Ibrahim", "Isaac",
        "James", "Joseph", "Juma", "Kamal", "Kofi", "Kwame", "Luis", "Mandla", "Mateo",
        "Moses", "Mulenga", "Musa", "Mwangi", "Nikhil", "Njoroge", "Obinna", "Omar", "Patrick", "Paulo",
        "Peter", "Rahul", "Rashid", "Samuel", "Sibusiso", "Simon", "Tafadzwa", "Tendai", "Thabo", "Tomas",
        "Tunde", "Vikram", "Yaw", "Yusuf", "Zuberi",
    ]
    surnames = [
        "Abara", "Addo", "Adeyemi", "Akinola", "Alvarez", "Amadi", "Asante", "Banda", "Bello",
        "Boateng", "Chanda", "Chikwanha", "Chirwa", "Daka", "Dlamini", "Douglas", "Eze", "Fernandes", "Gondwe",
        "Hassan", "Iyer", "Juma", "Kabwe", "Kamau", "Kapoor", "Kariuki", "Khumalo", "Lungu",
        "Mahlangu", "Makena", "Malik", "Mendes", "Mensah", "Moyo", "Mutale", "Mwale", "Mwansa",
        "Ncube", "Ndlovu", "Njoroge", "Nkosi", "Nwosu", "Obi", "Ochieng", "Odhiambo", "Okafor", "Okonkwo",
        "Omondi", "Owusu", "Patel", "Phiri", "Pillay", "Rao", "Reyes", "Sakala", "Sesay", "Shah",
        "Sibanda", "Silva", "Tembo", "Torres", "Wanjala", "Wekesa", "Zulu",
    ]


    middle_initial_share = 0.45
    middle_initials = "ABCDEFGHIJKLMNOPRSTWZ"


class Notes:
    followup = [
        "Household reported a good maize harvest this season.",
        "Head of household was away at the market; spoke with an adult family member.",
        "Family has started a small kitchen garden behind the house.",
        "Interested in joining the next savings group meeting.",
        "Roof repairs completed since the last visit.",
        "New water container provided by the community committee.",
        "Eldest child has started secondary school.",
        "Household sold two goats to pay school fees.",
        "Family asked about the next agriculture training dates.",
        "Borehole nearby was repaired last month; water access improved.",
        "Household is planning to expand their trading stall.",
        "A relative has moved in to help with farm work.",
        "Visit was short; family was preparing for a wedding.",
        "Household now keeps chickens as an extra source of income.",
        "Discussed safe water storage; family already using covered containers.",
        "Head of household found seasonal work at the nearby farm.",
    ]
    close_other = [
        "Family relocated to a relative's home in another district.",
        "Household merged with a neighbouring household.",
        "House was rebuilt in a different village.",
        "Family asked to be removed from the visit list.",
    ]
