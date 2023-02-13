import database.db_functions as database
import tests
import webview

def view_page():
    with open('web/index.html', 'r') as file:
        html = file.read().replace('\n', '')
    window = webview.create_window('Testing PyWebView', html=html, width=800, height=600)
    webview.start()

    return

def main():
    while(1):
        try:
            choose = int(input('''------- CHOOSE ------\n0. SHOW PAGE\n1. START DATABASES\n2. TEST INSERT RECORDS\n3. SHOW RECORDS'''))
        except:
            print("Please type a correct option.")
        else:
            if choose == 0:
                view_page()
            elif choose == 1:
                database.start_database()
            elif choose == 2:
                tests.test_insert()
            elif choose == 3:
                tests.show_all()
            else:
                return

if __name__ == "__main__":
    main()
