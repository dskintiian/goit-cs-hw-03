from colorama import Fore, Back, Style
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker
from random import randint


#
# db = client.book
#
# result = db.cats.find_one({"_id": ObjectId("60d24b783733b1ae668d4a77")})
# print(result)




def main():
    try:
        while True:
            try:
                command, *arguments = parse_command(input('>>'))
            except ValueError:
                continue

            if command in ['exit', 'close']:
                print('Good bye!')
                break

            try:
                cmd_handlers(command, *arguments)
            except KeyError as e:
                print(f'Command {e} not found')
                help_handler()
            except TypeError as e:
                print(f'Command {e} not found')
                help_handler()

    except KeyboardInterrupt:
        print('Good bye!')


def parse_command(input_string: str):
    return input_string.split()

def cmd_handlers(command, *arguments):
    handlers_map = {
        'help': help_handler,
        'seed': seed_data,
        'show': show_cat,
        'change-age': change_cat_age,
        'add-feature': add_cat_feature,
        'delete': delete_cat,
        'delete-all': delete_all_cats
    }

    return handlers_map[command](*arguments)

def help_handler():
    print(f'''Possible commands:
{Fore.LIGHTWHITE_EX}{Back.BLUE}help{Style.RESET_ALL} - prints list of available commands
{Fore.LIGHTWHITE_EX}{Back.BLUE}seed{Style.RESET_ALL} - generates some cats and writes data into database
{Fore.LIGHTWHITE_EX}{Back.BLUE}show [name]{Style.RESET_ALL} - find a cat by name and print it's details
{Fore.LIGHTWHITE_EX}{Back.BLUE}change-age [name] [age]{Style.RESET_ALL} - changes cat's age 
{Fore.LIGHTWHITE_EX}{Back.BLUE}add-feature [name] [new feature]{Style.RESET_ALL} - adds a feature to cat
{Fore.LIGHTWHITE_EX}{Back.BLUE}delete [name]{Style.RESET_ALL} - removes cat from database
{Fore.LIGHTWHITE_EX}{Back.BLUE}delete-all{Style.RESET_ALL} - removes all cats from database
{Fore.LIGHTWHITE_EX}{Back.BLUE}close{Style.RESET_ALL} or {Fore.YELLOW}{Back.BLUE}exit{Style.RESET_ALL} - terminates a program
    ''')

def seed_data():
    faker = Faker()
    db = get_mogo_db()
    data = [{'name': faker.first_name_nonbinary().split(' ')[0], 'age': randint(1,15), 'features': [faker.sentence(nb_words=3) for _ in range(randint(1,5))]} for _ in range(50)]
    print(data)
    db['cats'].insert_many(data)

def show_cat(name: str):
    db = get_mogo_db()
    try:
        cat = db.cats.find_one({'name': name})
        if cat is not None:
            print(cat)
        else:
            print('No such cat')

    except TypeError as e:
        print(e)

def change_cat_age(name: str, age: str):
    db = get_mogo_db()
    try:
        cat = db.cats.find_one({'name': name})
        if cat is not None:
            db.cats.update_one({"name": name}, {"$set": {"age": int(age)}})
            print('Done')
        else:
            print('No such cat')
    except TypeError as e:
        print(e)

def add_cat_feature(name: str, *args):
    db = get_mogo_db()
    try:
        cat = db.cats.find_one({'name': name})
        if cat is not None:
            db.cats.update_one({"name": name}, {"$push": {"features": ' '.join(args)}})
            print('Done')
        else:
            print('No such cat')
    except TypeError as e:
        print(e)

def delete_cat(name: str):
    db = get_mogo_db()
    try:
        cat = db.cats.find_one({'name': name})
        if cat is not None:
            db.cats.delete_one({"name": name})
            print('Done')
        else:
            print('No such cat')
    except TypeError as e:
        print(e)


def delete_all_cats(*_):
    db = get_mogo_db()
    if input('Are you sure? (Y/N) ').lower() == 'y':
        db.cats.delete_many({})
        print('Done')

def get_mogo_db():
    client = MongoClient(
        'mongodb+srv://mongodbuser:mongodbpswd@aws-free-goit.veujg.mongodb.net/',
        server_api=ServerApi('1')
    )

    return client['goit']


if __name__ == '__main__':
    main()
