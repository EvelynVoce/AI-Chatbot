from wikipedia import summary, exceptions
from similarity import get_similar
import nltk
from pyjokes import get_joke
from nltk.sem import Expression
import pandas

read_expr = Expression.fromstring
kb: list = []
data = pandas.read_csv('kb.csv', header=None)
[kb.append(read_expr(row)) for row in data[0]]

user_name: str = ""


def extract_name(user_input: str) -> str:
    for sent in nltk.sent_tokenize(user_input):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                return ' '.join(c[0] for c in chunk.leaves())


def get_ai_response(kern, user_input: str):
    if user_input == "":
        return

    answer: str = kern.respond(user_input)
    # Kernel recognises input and responds appropriately
    if answer[0] != '#':
        return answer

    cmd, output = answer[1:].split('$')
    if cmd == '0':  # Bye command
        return output

    elif cmd == '1':  # Wikipedia command
        try:
            output = summary(output, sentences=2, auto_suggest=False)
        except exceptions.PageError or exceptions.DisambiguationError:
            output = "Sorry, I do not know that. Be more specific!"

    elif cmd == '3':  # Memory triggers
        if "my name is" in user_input.lower():  # Extract name
            global user_name
            user_name = extract_name(user_input)
            if user_name is None:
                user_name = ""

    elif cmd == '4':  # Memory retrieval
        if "my name" in user_input.lower():
            return user_name if user_name != "" else "I do not know your name"

    elif cmd == '5':  # Random joke
        output = get_joke(language="en", category="neutral")

    elif cmd == "31":  # I know that x is y
        object1, object2 = output.split(' is ')
        expr = read_expr(object2 + '(' + object1 + ')')

        # >>> ADD SOME CODES HERE to make sure expr does not contradict
        # with the KB before appending, otherwise show an error message.

        kb.append(expr)
        return 'OK, I will remember that', object1, 'is', object2

    elif cmd == "32":  # Check that x is y
        pass

    elif cmd == '99':  # Default command
        output = get_similar(user_input)
    return output


# def main():
#     print(welcome_message := "Welcome to this chat bot. Please feel free to ask questions from me!")
#     speak(welcome_message)
#     while True:
#         user_input: str = input("> ")
#         if user_input == "":
#             continue
#
#         answer: str = kern.respond(user_input)
#
#         # Kernel recognises input and responds appropriately
#         if answer[0] != '#':
#             print(answer)
#             speak(answer)
#             continue
#
#         cmd, output = answer[1:].split('$')
#         if cmd == '0':  # Bye command
#             print(output)
#             speak(output)
#             break
#
#         elif cmd == '1':  # Wikipedia command
#             try:
#                 output = summary(output, sentences=3, auto_suggest=False)
#             except exceptions.PageError:
#                 output = "Sorry, I do not know that. Be more specific!"
#
#         elif cmd == '99':  # Default command
#             output = similarity.get_similar(user_input)
#
#         print(output)
#         speak(output)

# from nltk.corpus import wordnet
# from collections import Counter
# from nltk import word_tokenize, pos_tag

# My own code
# sentence: str = input("Enter a sentence")
# tokens: list[str] = word_tokenize(sentence)
# tagged: tuple[(str, str)] = pos_tag(tokens)
# print(tagged)
# print(word_dict := dict(Counter(sentence.split())))  # Create word dict


# class Word:
#
#     def __init__(self, w):
#         self.word: str = w
#         syn = wordnet.synsets(self.word)
#         self.type: str = syn[0].lexname().split('.')[0] if syn else None


# # Tokenize words
# word_class: list[Word] = [Word(w) for w in sentence.split()]
# for w in word_class:
#     print(w.word, w.type)


# WEATHER


# elif cmd == '2':  # Weather command: Test if this works!
#     api_key: str = "5403a1e0442ce1dd18cb1bf7c40e776f"
#     api_url: str = r"http://api.openweathermap.org/data/2.5/weather?q="
#     response = get(api_url + output + r"&units=metric&APPID=" + api_key)
#     response_json = loads(response.content)
#     if response.status_code == 200 and response_json:
#         t = response_json['main']['temp']
#         tmi = response_json['main']['temp_min']
#         tma = response_json['main']['temp_max']
#         hum = response_json['main']['humidity']
#         wsp = response_json['wind']['speed']
#         conditions = response_json['weather'][0]['description']
#         print("The temperature is", t, "°C, varying between", tmi, "and", tma,
#               "at the moment, humidity is", hum, "%, wind speed ", wsp, "m/s,", conditions)
#     else:
#         print("Sorry, I could not resolve the location you gave me.")