import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('C:/Users/aaronhampson/Downloads/ASDYHUSAJDB/murder-mystery.db')
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Get a list of table names in the database
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()
table_names = [table[0] for table in table_names] 


# Read each table into a separate DataFrame
dataframes = {}
for table_name in table_names:
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        dataframes[table_name] = df
    except Exception as e:
        print(f"Error reading table {table_name}: {str(e)}")

# Close the database connection
conn.close()
print(f"Dataframes:{table_names}")
print()
print(dataframes['crime_scene_report'].info())
print()
print()
matching_rows = dataframes['crime_scene_report'][
    (dataframes['crime_scene_report']['city'] == 'SQL City') &
    (dataframes['crime_scene_report']['date'] == 20180115) &
    (dataframes['crime_scene_report']['type'] == 'murder')
]

print(matching_rows["description"])

# So, now we have 2 witnesses! 
# Explore the other dataframes to find the murderer.

for i in dataframes: print(i) # prints list of DF names

witness_one = dataframes['person'][
    (dataframes['person']['name'].str.contains("Annabel")) &
    (dataframes['person']['address_street_name'] == 'Franklin Ave')
]

witness_two = dataframes['person'][
    (dataframes['person']['address_street_name'] == 'Northwestern Dr') &
    (dataframes['person']['address_number'].nlargest())
]

# print(witness_one) # Morty Schapiro
# print(witness_two) # Annabel Miller

witness_one_id = int(witness_one['id'])
witness_two_id = int(witness_two['id'])

witness_one_interview = dataframes['interview'][
    (dataframes['interview']['person_id'] == witness_one_id)
]
witness_two_interview = dataframes['interview'][
    (dataframes['interview']['person_id'] == witness_two_id)
]

print(witness_one_interview)
print(witness_two_interview)



gym_members = dataframes['get_fit_now_check_in'][
    (dataframes['get_fit_now_check_in']['check_in_date'] == 20180109) &
    (dataframes['get_fit_now_check_in']['membership_id'].str.contains("48Z")) 
]

suspect_one = dataframes['get_fit_now_member'][
    (dataframes['get_fit_now_member']['id'] == "48Z7A")
]
suspect_two = dataframes['get_fit_now_member'][
    (dataframes['get_fit_now_member']['id'] == "48Z55")
]

print(suspect_one)
print(suspect_two)

suspect_one_person_id = int(suspect_one["person_id"])
suspect_two_person_id = int(suspect_two["person_id"])

license_plate = dataframes['drivers_license'][
    (dataframes['drivers_license']['plate_number'].str.contains("H42W")) &
    (dataframes['drivers_license']['gender'] == "male")
]

possible_cars = [i for i in license_plate['id']]

guilty_one = dataframes['person'][
    (dataframes['person']['license_id'].isin(possible_cars)) &
    (dataframes['person']['id'] == suspect_one_person_id)
].empty

guilty_two = dataframes['person'][
    (dataframes['person']['license_id'].isin(possible_cars)) &
    (dataframes['person']['id'] == suspect_two_person_id)
].empty

if guilty_one is True:
    print(f"joe germuska is innocent and jeremy bowers is guilty")
    guilty_id = suspect_two_person_id
else:
    print(f"jeremy bowers is innocent and jeremy bowers is guilty")
    guilty_id = suspect_one_person_id

guilty_testimony = dataframes['interview'][
    (dataframes['interview']['person_id'] == guilty_id)
]

print(guilty_testimony)

hirer = dataframes['drivers_license'][
    (dataframes['drivers_license']['hair_color'] == "red") &
    (dataframes['drivers_license']['car_make'] == "Tesla") &
    (dataframes['drivers_license']['car_model'] == "Model S") &
    (dataframes['drivers_license']['height'] >= 65) &
    (dataframes['drivers_license']['height'] <= 67)
]

possible_hirers = [i for i in hirer['id']]

hirer = dataframes['person'][
    (dataframes['person']['license_id'].isin(possible_hirers))
]

possible_hirers = [i for i in hirer['id']]

print(possible_hirers)

hirer = dataframes['facebook_event_checkin'][
    (dataframes['facebook_event_checkin']['person_id'].isin(possible_hirers)) &
    (dataframes['facebook_event_checkin']['event_name'] == "SQL Symphony Concert") &
    (dataframes['facebook_event_checkin']['date'].astype(str).str.startswith("201712"))
]

print(hirer) # person id = 99716

hirer = dataframes['person'][
    (dataframes['person']['id'] == 99716)
]

print(dataframes['interview'][(dataframes['interview']['person_id'] == 99716)])
print(hirer)

# the murderer is Miranda Priestley.