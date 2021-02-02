import matplotlib.pyplot as plt
from string import punctuation, whitespace

trans_dict = {}
for s in punctuation:
    trans_dict[ord(s)] = None

for s in whitespace:
    trans_dict[ord(s)] = None


def analyse_text(filename):
    fin = open(filename, 'r', encoding="utf-8")
    people = dict()
    i = 0
    for line in fin:
        if i < 3:
            i += 1
            continue
        person = get_person(people, line)
        if person == "1234567890qwertyasdfghzxcvbn":
            continue
        people[person] = people.get(person, 0) + 1
    fin.close()
    return people


def get_person(d, s):
    if "salió del grupo" in s or " añadió a " in s or " cambió la descripción del grupo" in s or "Añadiste a " in s:
        return '1234567890qwertyasdfghzxcvbn'

    date = s[:15].translate(trans_dict)
    if not date.isdigit():
        return '1234567890qwertyasdfghzxcvbn'

    first_letter = '///'
    for letter in range(len(s)):
        if s[letter].isalpha() and first_letter == "///":
            first_letter = letter
        elif not s[letter].isalpha() and s[letter] != " " and first_letter != '///':
            last_letter = letter
            break
    try:
        return s[first_letter:last_letter]
    except:
        print(s)


def make_graphic(d):
    print(d)
    people = [person for person in d]
    n_messages = [n for n in d.values()]
    plt.pie(n_messages, labels=people, autopct='%1.1f%%')
    plt.show()


make_graphic(analyse_text('Chat de WhatsApp con Nos Falta 1_4.txt'))
