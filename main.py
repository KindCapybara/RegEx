import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

phone_person = r"(\+7|8)\s*\(*(\d..)\)*\s*[-]*(\d..)?[-]*(\d.)?[-]*(\d+)?"
new_phone_person = r"+7(\2)\3-\4-\5"

additional_number = r"\(*доб.\s(\d+)\)*"
new_additional_number = r"доб.\1"

new_contact_list = []
for person in contacts_list:
    new_person = []
    for some_data in person:
        result = re.sub(phone_person, new_phone_person, some_data)
        change_additional_number = re.sub(additional_number, new_additional_number, result)
        new_person.append(change_additional_number)
    new_contact_list.append(new_person)

for person in new_contact_list:
    fls_name = []
    for some_data in range(3):
        fls_name += person[some_data].split(' ')
    person[:3] = fls_name[:3]

# Объединение повторов
merging_repetitions = set()

for person in range(1, len(new_contact_list)):
    for next_person in range(person + 1, len(new_contact_list)):
        if new_contact_list[person][:2] == new_contact_list[next_person][:2]:
            for data_index in range(2, len(new_contact_list[person])):
                if len(new_contact_list[person][data_index]) < len(new_contact_list[next_person][data_index]):
                    new_contact_list[person][data_index] = new_contact_list[next_person][data_index]
                    merging_repetitions.add(next_person)

for index in merging_repetitions:
    new_contact_list.pop(index)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contact_list)
