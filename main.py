from TwitterAPI import TwitterAPI
import psycopg2
import datetime
import csv
import random

con = psycopg2.connect(
    host='localhost',
    database='Twitterzuil',
    user='postgres',
    password='38gAc57ip!'
)

cur = con.cursor()

# SQL, creating a table within pgAdmin with the name proja_db
'''cur.execute("CREATE TABLE proja_db (" 
            "id SERIAL,"
            "name VARCHAR, "
            "message VARCHAR, "
            "date DATE, "
            "moderation VARCHAR, "
            "comment VARCHAR, "
            "moderator_id INTEGER"
             ");")'''


api = TwitterAPI('fDyrxs5vC3i1SKp1Vzk8Esbxn',
                 'BkenseWC7SBxJJ4oqsCwy7Pc2xUlNOETwbflxG5ZHg3QXYDuBJ',
                 '990236539367149569-XFCvDLiZZuZUo0Lspuc3aBUbCO12ya8',
                 'dBAkIIZGUQUi1UuHuj6GesAGozc5JdUX5sHeHDqlWLPhN')

current_date = datetime.datetime.now().strftime("%Y-%m-%d : %H:%M:%S")  # Acquiring current date information


def name_check():  # function to check whether if a name has been given, if not then assign string : Anonymous
    name = input('What is your name? (Leave empty to stay anonymous): ')
    if not name:
        anon = name.replace(name, 'Anonymous')
        return anon
    else:
        return name


name_value = name_check()


def message_check():  # function to check message length.
    while True:  # running a while loop to ensure the input keeps repeating itself until it gets a satisfactory answer.
        message = input('Please type your message here (max 140 char): ')
        if len(message) > 140:
            print('Error, exceeded max allowed characters.')
            continue
        else:
            return message


message_value = message_check()


def moderator():    # function to accept or reject messages. If message is accepted, show the message on twitter.
    moderation = input('[Accept/Reject?] Uppercase sensitive!: ')
    if moderation == 'Reject':
        return 'Rejected'

    elif moderation == 'Accept':
        twitter_message = message_value + ' -' + name_value
        r = api.request('statuses/update', {'status': twitter_message})
        if r.status_code == 200:
            print('SUCCESS')
        return 'Accepted'


moderation_value = moderator()


def moderator_input_check():  # function to input commentary on messages, left open provided the message was accepted.
    moderator_input = input("Insert comment (Leave open if message got accepted): ")
    if not moderator_input:
        empty_input = moderator_input.replace(moderator_input, 'No comment')
        return empty_input
    else:
        return moderator_input


moderator_input_value = moderator_input_check()


def moderator_id_check():  # function to check whether the moderator uses the correct ID.
    while True:
        try:
            moderator_id = int(input("Insert MOD_ID: "))
        except ValueError:
            print("Error, please choose a MOD_ID that's a positive integer bigger than 0.")
            continue
        else:
            return moderator_id


moderator_id_value = moderator_id_check()

# sql code that inserts data within the proja_db column.
sql = "INSERT INTO proja_db (name, message, date, moderation, comment, moderator_id) VALUES (%s, %s, %s, %s, %s, %s)"
val = (name_value, message_value, current_date, moderation_value, moderator_input_value, moderator_id_value)

cur.execute(sql, val)

cur.execute("SELECT * FROM proja_db;")

con.commit()

cur.fetchall()

con.commit()


def writing_to_csv():
    with open('message_bestand.csv', 'a') as csv_file:  # csv.write lines to get all the input saved as a csv
        # file.
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            [name_value, message_value, current_date, moderation_value, moderator_input_value, moderator_id_value])
    return


writing_to_csv()

cur.close()

con.close()
