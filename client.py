import configparser
import csv
import random
import sys

config = configparser.ConfigParser()
config.read('config.ini')

# https://stackoverflow.com/a/12424439
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
        print('\n')
    except:
        print("failed to send mail")
        print('\n')

people = []
with open('people.csv', mode='r') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        person = {}
        person['id'] = row['id']
        person['name'] = row['name']
        person['email'] = row['email']
        person['spouse_id'] = row['spouse_id']
        
        people.append(person)
        
print('Name Drawing Utility')        
print('====================')
print('\n')
        
ineligible_receiver_ids = []

giver_id_to_receiver_id = {}

try: 
    for person in people:
        giver = person
        giver_id = person['id']
        giver_name = person['name']
        giver_spouse_id = person['spouse_id']
        
        print('  * choosing receiver for: ' + giver_name)
        
        eligible_receivers = []
        for potential_receiver in people:
            # you cannot give a gift to yourself or your spouse
            if potential_receiver['id'] == giver_id or potential_receiver['id'] == giver_spouse_id:
                continue
            # you cannot give a gift to someone whose already a reciever
            if potential_receiver['id'] in ineligible_receiver_ids:
                continue
            eligible_receivers.append(potential_receiver)
        
        receiver = random.choice(eligible_receivers)
        receiver_id = receiver['id']
        receiver_name = receiver['name']
        
        giver_id_to_receiver_id[giver_id] = receiver_id
        
        ineligible_receiver_ids.append(receiver_id)
except:
    print('\n')
    print('Oops, try again...')
    sys.exit(1)    

print('\n')
for giver_id in giver_id_to_receiver_id:    
    giver_name = [person['name'] for person in people if person['id'] == giver_id][0]
    giver_email = [person['email'] for person in people if person['id'] == giver_id][0]
    receiver_name = [person['name'] for person in people if person['id'] == giver_id_to_receiver_id[giver_id]][0]
    
    print('  * sending email to ' + giver_name + '...')    
    print('\n')
    
    email_subject = 'Name Drawing Utility: Your Receiver'
    email_body = giver_name + ', you are giving a gift this year to ' + receiver_name + '.'
    send_email(config['EMAIL']['USER'], config['EMAIL']['PWD'], giver_email, email_subject, email_body)
