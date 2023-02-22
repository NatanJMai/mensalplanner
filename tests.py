import datetime
import database.db_functions as database

def test_insert(day):
    # id, name and password
    query_user = """
    INSERT INTO user VALUES
    (1,  'James', 'Smith'),
    (2, 'Stefanie',  'Martin'), 
    (3, 'Steve', 'Wang'),
    (4, 'Friederike',  'Müller-Rossi'),
    (5, 'Isobel', 'Ivanova'),
    (6, 'Niamh', 'Murphy');
    """

    # id, name, description and color
    query_label = """
    INSERT INTO label VALUES
    (1,  'Label 1', 'Label to finances', 'Green'),
    (2,  'Label 2', 'Label to personal', 'Black'),
    (3,  'Label 3', 'Label to professional', 'Red');
    """

    # id, name, description, datetime, day, month, year, value, credit/debit, user and label
    now     = datetime.datetime.now().strftime('%Y-%m-%d')
    #day     = datetime.datetime.now().day
    month   = datetime.datetime.now().month
    year    = datetime.datetime.now().year
    query_task = f'''
    INSERT INTO task VALUES 
    (null, 'TASK 4', 'TASK TO FINANCE', '{day}', '{month}', '{year}', 15000, FALSE, 2, 1),
    (null, 'TASK 5', 'TASK TO FINANCE', '{day}', '{month}', '{year}', 2022, TRUE, 2, 2),
    (null, 'TASK 6', 'TASK TO FINANCE', '{day}', '{month}', '{year}', 3333, FALSE, 2, 3);
    '''

    connection = database.connect_on_database()
    #database.execute_query(connection, query_user)
    #database.execute_query(connection, query_label)
    database.execute_query(connection, query_task)

def show_all():
    query_user  = """ SELECT * FROM user; """
    query_label = """ SELECT * FROM label; """
    query_task  = """ 
    SELECT t.task_id, t.task_name, u.user_name 
        FROM task t 
        JOIN user u WHERE t.user = u.user_id; 
    """

    connection = database.connect_on_database()
    users  = database.read_query(connection, query_user)
    labels = database.read_query(connection, query_label)
    tasks  = database.read_query(connection, query_task)

    print("-------- USERS --------")
    for u in users:
        print(f"Name: {u[1]}, Password: {u[2]}")

    print("\n-------- LABEL --------")
    for u in labels:
        print(f"Name: {u[1]}, Description: {u[2]}")

    print("\n-------- TASK --------")
    for u in tasks:
        print(f"Name: {u[1]}, User: {u[2]}")