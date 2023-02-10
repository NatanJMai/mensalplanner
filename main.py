import eel
import database.db_functions as database
import tests

from random import randint

@eel.expose
def pg_home():
    return 2

def main():
    while(1):
        try:
            choose = int(input('''------- CHOOSE ------\n1. START DATABASES\n2. TEST INSERT RECORDS\n3. SHOW RECORDS'''))
        except:
            print("Please type a correct option.")
        else:
            if choose == 1:
                database.start_database()
            elif choose == 2:
                tests.test_insert()
            elif choose == 3:
                tests.show_all()
            else:
                return

if __name__ == "__main__":
    main()
