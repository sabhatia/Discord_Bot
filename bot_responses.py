import random

def get_response(message: str) -> str:
    l_message = message.lower()

    if (l_message == 'hello'):
        return 'Hey there'

    if (l_message == 'bye'):
        return 'Have a nice day!'

    if (l_message == 'roll'):
        return str(random.randint(1,6))

    if (l_message == 'help'):
        return "`This is a help message that you can modify!`"

    return random.choice(
        ['I didn\'t get that. Can you rephrase?',
         'I\'m not sure I understand. Come again?'
         'Can you ask that question differently?']
    )