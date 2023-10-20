#user authentification 
#income and expense tracking
#Budget planning
#financial reports
#saving and investment tracking
#data export

import psycopg2
import csv

def csvimport(cursor):
    
    #SQL query to the accounts table
    csv_query = "SELECT * FROM accounts"
    
    #executes the query
    cursor.execute(csv_query)
    
    #fetch the data from all rows
    data = cursor.fetchall()
    
    #variable for exporting as csv file
    csv_file = "export_data.csv"
    
    #open csv file for writing
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        
        #write the header row (column names)
        writer.writerow([desc[0] for desc in cursor.description])
        
        #write the data rows
        writer.writerows(data)


#user login function that ask you to login before executing rest of code
def userlogin(cursor, connection):
    print("Are you a new user or an existing user?")
    question = input("Enter new or exisiting: ")
    
    #allows you to create a new user
    if question == 'new':
        create_id = input("Enter a new user ID: ")
        newid_query = "INSERT INTO userlogin (id) VALUES(%s)"
        try:
            cursor.execute(newid_query, (create_id,))
            connection.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")
            
    #allows you to check if you are an existing user or not  
    elif question == 'existing':
        while True:
            exist_id = input("Enter your user ID: ")
            exist_query = "SELECT id FROM userlogin WHERE id = %s"
            
            cursor.execute(exist_query, (exist_id,))
            
            id_row = cursor.fetchone()
            
            #if you are an existing user it will continue if not you will be told to try again 
            if id_row:
                print(f'Welcome {exist_id}')
                break
            else:
                print(f"User '{exist_id}' does not exist. Please try again.")

#function for inserting data into the acounts database
def insert_data(cursor, connection):
    user_id = input('Enter user ID: ')
    total = int(input("Enter your total amount of money: "))
    month = input("What month is it: ")
    monthly_expenses = int(input("Enter how much you spent this month: "))
    left_over = total - monthly_expenses
    print(f"You have {left_over} left over, in the month of {month}.")

    # Insert Query
    insert_query = "INSERT INTO accounts (user_id, total, month, monthly_expenses) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(insert_query, (user_id, total, month, monthly_expenses))
        connection.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")

#allows you to view the accounts database
#maybe I will allow the option of viewing the userlogin database
def view_data(cursor):
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

#function for calculating expenses 
def calculate_expenses(cursor):
    print("Enter 1 if you would like to input data or enter 2 if you would like to select data from the database ")
    choice2 = input("Select 1/2: ")
    
    #this choice you will input code and it will give feedback on what you should allocate money too
    if choice2 == '1':
        income = int(input("Enter your income for the month: "))
        necessities = income * 0.5
        wants = income * 0.3
        savings = income * 0.2
        print(f"Based on the information you provided:")
        print(f"You can spend ${necessities:.2f} on necessities (e.g., living, food, and transport).")
        print(f"You can spend ${wants:.2f} on wants (e.g., shopping, eating out).")
        print(f"You should put ${savings:.2f} in savings.")
    
    #this section will allow you to chose data from accounts database and use that to show what you should spend money on 
    elif choice2 == '2':
        cursor.execute("SELECT * FROM accounts")
        rows = cursor.fetchall()
        for i, row in enumerate(rows, start=1):
            print(f"{i}. {row}")
        
        user_choice = int(input("Select a row number: "))
        if 1 <= user_choice <= len(rows):
            selected_row = rows[user_choice - 1]
            print(f"You selected, {selected_row}")
            
            column_data = selected_row[1]
            
            income2 = column_data
            necessities2 = income2 * 0.5
            wants2 = income2 * 0.3
            savings2 = income2 * 0.2
            print(f"Based on the information provided from the database:")
            print(f"You can spend ${necessities2:.2f} on necessities (e.g., living, food, and transport).")
            print(f"You can spend ${wants2:.2f} on wants (e.g., shopping, eating out).")
            print(f"You should put ${savings2:.2f} in savings.")
        
        
        
    else:
        print("Invalid selection.")
        
#where the code will run with the menu and we will call functions into here
def main():
    #connects to the postgresql database
    connection = psycopg2.connect(
        dbname="",
        user="",
        password="",
        host="",
        port=""
    )

    cursor = connection.cursor()
    
    userlogin(cursor, connection)

    while True:
        
        print("Monthly Budget and Expense Tracker:")
        print("1. Begin entering data")
        print("2. View data table")
        print("3. Calculate how much I can spend each month")
        print("4. Download table as a csv file")
        print("5. Type 'exit' to quit")

        choice = input("Select option 1/2/3/4: ")

        if choice == '1':
            insert_data(cursor, connection)
        elif choice == '2':
            view_data(cursor)
        elif choice == '3':
            calculate_expenses(cursor)
        elif choice == '4':
            csvimport(cursor)
            print("File was sucessfully was exported")
        elif choice == '5' or choice.lower() == 'exit':
            break
        else:
            print("Invalid choice, select again from the options.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
