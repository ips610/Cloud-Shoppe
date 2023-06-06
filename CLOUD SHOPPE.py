# IPS_COURIER_SERVICE

import mysql.connector as mysql
from mysql.connector import cursor
import csv
import pickle
import random
import string
import stdiomask
#import getpass

# connecting with database and creating the login table if not there which contains username and password


def connecting_the_database():

    global database, cursor, login_details

    database = mysql.connect(
        host="localhost", user="root", password="", database="CLOUD_SHOPPE")

    if database.is_connected():
        print("Welcome to 'CLOUD SHOPPE'")
    cursor = database.cursor()

    # login table it will store records in mysql only breif record

    login_details = "create table if not exists login_details (Name char(50),Username char(20) primary key, Password char(20),AccountCreatedOn char(20));"
    cursor.execute(login_details)
    print("-----------------------------")

# creating the sign up


def creating_user_account():

    global name, username, password, user_account, address, mobileno, email, choose, captcha

    # it will store records in mysql detailed record

    user_account = "create table if not exists user_details (Name char(50), Username char(20) primary key, Password char(20), Address char(100), MobileNumber int, Email char(100));"
    cursor.execute(user_account)

    # sign up and login

    print('1. SIGN UP')
    print('2. LOGIN')
    print()
    choose = int(input("ENTER (1) FOR NEW ACCOUNT OR (2) FOR LOGIN: "))

    # sign up

    while choose == 1:

        name = input("Enter Your Name: ")
        username = input("Set Your User_Name Here: ")
        q1 = "select * from login_details where Username=%s;"
        q2 = (username,)
        cursor.execute(q1, q2)
        if cursor.fetchone() is None:

            password = stdiomask.getpass("Set Your Password Here: ", mask="*")
            confirm_password = stdiomask.getpass(
                "Confirm Your Password: ", mask="*")

            while password != confirm_password:

                print("Password Does Not Match !!!")
                print("Please Enter Your Password Again")
                password = stdiomask.getpass("Set Your Password Here: ", mask="*")
                confirm_password = stdiomask.getpass(
                    "Confirm Your Password: ", mask="*")

            address = input("Enter Address: ")
            mobileno = int(input("Enter Mobile No: "))

            # mobile no check length must be 10 digits

            if len(str(mobileno)) == 10:
                pass
            else:
                while len(str(mobileno)) != 10:
                    print("Invalid Mobile Number")
                    mobileno = int(input("Enter Mobile No: "))

            email = input("Enter Email: ")

            captcha_code()
            entered_captcha = input("Enter Above Captcha Code To Proceed: ")

            while captcha != entered_captcha:

                print()
                print("Captcha Does Not Match")
                print("Try Again !!!")
                print()

                captcha_code()
                entered_captcha = input("Enter Above Captcha Code To Proceed: ")

            q1 = "insert into login_details(Name,Username,Password,AccountCreatedOn) values(%s,%s,%s,now());"
            q2 = (name, username, password)
            cursor.execute(q1, q2)

            q3 = "insert into user_details values(%s,%s,%s,%s,%s,%s);"
            q4 = (name, username, password, address, mobileno, email)
            cursor.execute(q3, q4)

            database.commit()
            user_details_csv_file_record()
            print("Account created Successfully")
            choose = 2

        else:
            
            print("Username Already Taken !!!")
            choose=1

    # login

# creating login window


def logging_into_user_account():

    global login_username, login_password, choose, captcha
    global essential_items_cart, books_educational_cart, books_novels_cart, electronics_items_cart, clothes_items_cart, games_items_cart, medicines_items_cart, postmail_total
    global name, username, password, user_account, address, mobileno, email, choose, captcha

    while choose == 2:

        print()
        print("Login")
        print("-----")
        print()

        login_username = input("Enter Your User_Name: ")
        login_password = stdiomask.getpass("Enter Your Password: ", mask="*")

        captcha_code()
        entered_captcha = input("Enter Above Captcha Code To Proceed: ")

        while captcha != entered_captcha:

            print()
            print("Captcha Does Not Match")
            print("Try Again !!!")
            print()

            captcha_code()
            entered_captcha = input("Enter Above Captcha Code To Proceed: ")

        q1 = "select * from login_details where Username=%s and password=%s;"
        q2 = (login_username, login_password)
        cursor.execute(q1, q2)

        if cursor.fetchone() is None:

            print("Invalid UserName or Password !!")
            choose = int(input("Press (1) for sign up and (2) for login: "))
            if choose == 1:
                creating_user_account()

        else:

            essential_items_cart = 0
            books_educational_cart = 0
            books_novels_cart = 0
            electronics_items_cart = 0
            clothes_items_cart = 0
            games_items_cart = 0
            medicines_items_cart = 0
            postmail_total = 0

            q3 = "select * from user_details where Username=%s and password=%s;"
            q4 = (login_username, login_password)
            cursor.execute(q3, q4)
            record=cursor.fetchall()
            name=record[0][0]
            address=record[0][3]
            mobileno=record[0][4]
            email=record[0][5]

            print("Login Successful !!!")
            choose = 3

# storing user data in csv files


def user_details_csv_file_record():

    global user_details, writer_user_details

    # it will store records in csv file with required fields

    user_details = open("User Details.csv", "a", newline="\r\n")
    writer_user_details = csv.writer(user_details)
    writer_user_details.writerow(
        ["Name", "Username", "Address", "MobileNumber"])
    writer_user_details.writerow([name, username, address, mobileno])
    user_details.close()

# captcha code for login and sign up securitiy


def captcha_code():

    global captcha

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits

    mixture = lower+upper+num

    temp = random.sample(mixture, 6)

    captcha = "".join(temp)

    print()
    print(captcha)
    print()


# essential items shopping functions


def essential_items_shopping():

    global essential_items_list, essential_items_list_price, essential_items_cart, essential_items_cart_number, essential_items_cart_number_qty

    essential_items_list = ["Flour", "Pulses", "Toothpaste", "Chips", "Biscuits",
                            "Chocolate", "Sugar", "Soap", "Bread", "Maggi"]
    essential_items_list_price = [
        25, 90, 70, 20, 10, 5, 20, 30, 35, 12]

    essential_items_cart_number = int(input("Enter Item Number: "))
    essential_items_cart_number_qty = float(input("Enter Quantity: "))
    essential_items_cart += essential_items_list_price[essential_items_cart_number -
                                                       1] * essential_items_cart_number_qty

    print(
        essential_items_list[essential_items_cart_number-1], "Added Successfully !!!")

    # writing details in file
    essential_items_cart_details_text_file()

    print(essential_items_list_price[essential_items_cart_number-1]
          * essential_items_cart_number_qty)

    print()


def essential_items_shopping_items():

    global essential_items_list, essential_items_list_price, essential_items_cart, essential_items_cart_number, essential_items_cart_number_qty

    essential_items_list = ["Flour", "Pulses", "Toothpaste", "Chips",
                            "Biscuits", "Chocolate", "Sugar", "Soap", "Bread", "Maggi"]
    essential_items_list_price = [25, 90, 70, 20, 10, 5, 20, 30, 35, 12]

    for i in range(0, len(essential_items_list)):
        print(i+1, ". ", essential_items_list[i],
              "     ", essential_items_list_price[i])


def essential_items_cart_details_text_file():

    global essential_items_list, essential_items_list_price, essential_items_cart, essential_items_cart_number, essential_items_cart_number_qty
    global cart_items_details

    # writing details in file

    cart_items_details.write("Item Name: ")
    cart_items_details.write(
        essential_items_list[essential_items_cart_number-1])
    cart_items_details.write("   ")
    cart_items_details.write("Quantity: ")
    cart_items_details.write(str(essential_items_cart_number_qty))
    cart_items_details.write("   ")
    cart_items_details.write("Price: ")
    cart_items_details.write(str(
        essential_items_list_price[essential_items_cart_number-1] * essential_items_cart_number_qty))
    cart_items_details.write("\n")


# educational books shopping functions


def books_educational_items_shopping():

    global books_educational_list, books_educational_list_price, books_educational_cart, books_educational_cart_number, books_educational_cart_number_qty

    books_educational_list = ["NCERT Physics XI", "NCERT Chemistry XI", "NCERT Maths XI", "NCERT English XI", "Computer Science With Python By Sumita Arora XI",
                              "NCERT Physics XII", "NCERT Chemistry XII", "NCERT Maths XII", "NCERT English XII", "Computer Science With Python By Sumita Arora XII"]
    books_educational_list_price = [
        350, 325, 170, 160, 450, 370, 350, 180, 170, 550]

    books_educational_cart_number = int(input("Enter Item Number: "))
    books_educational_cart_number_qty = float(input("Enter Quantity: "))
    books_educational_cart += books_educational_list_price[books_educational_cart_number -
                                                           1] * books_educational_cart_number_qty

    print(
        books_educational_list[books_educational_cart_number-1], "Added Successfully !!!")

    # writing details in text file
    books_educational_items_cart_details_text_file()

    print(books_educational_list_price[books_educational_cart_number-1]
          * books_educational_cart_number_qty)


def books_educational_items_shopping_items():

    global books_educational_list, books_educational_list_price, books_educational_cart, books_educational_cart_number, books_educational_cart_number_qty

    books_educational_list = ["NCERT Physics XI", "NCERT Chemistry XI", "NCERT Maths XI", "NCERT English XI", "Computer Science With Python By Sumita Arora XI",
                              "NCERT Physics XII", "NCERT Chemistry XII", "NCERT Maths XII", "NCERT English XII", "Computer Science With Python By Sumita Arora XII"]
    books_educational_list_price = [
        350, 325, 170, 160, 450, 370, 350, 180, 170, 550]

    for i in range(0, len(books_educational_list)):
        print(i+1, ". ", books_educational_list[i],
              "     ", books_educational_list_price[i])


def books_educational_items_cart_details_text_file():

    global books_educational_list, books_educational_list_price, books_educational_cart, books_educational_cart_number, books_educational_cart_number_qty
    global cart_items_details

    # writing details in file

    cart_items_details.write("Item Name: ")
    cart_items_details.write(
        books_educational_list[books_educational_cart_number-1])
    cart_items_details.write("   ")
    cart_items_details.write("Quantity: ")
    cart_items_details.write(str(books_educational_cart_number_qty))
    cart_items_details.write("   ")
    cart_items_details.write("Price: ")
    cart_items_details.write(str(
        books_educational_list_price[books_educational_cart_number-1] * books_educational_cart_number_qty))
    cart_items_details.write("\n")


# novels books shopping functions


def books_novels_items_shopping():

    global books_novels_list, books_novels_list_price, books_novels_cart, books_novels_cart_number, books_novels_cart_number_qty

    books_novels_list = ["Arabian Nights", "Rich Dad Poor Dad", "Harry Potter Series", "Sherlock Holmes", "Angles And Demons",
                         "Origin", "Frankenstein", "Invisible Man", "Pride And Prejudice", "Wings Of Fire"]
    books_novels_list_price = [1000, 300, 2700,
                               1000, 260, 250, 120, 175, 120, 420]

    books_novels_cart_number = int(input("Enter Item Number: "))
    books_novels_cart_number_qty = float(input("Enter Quantity: "))
    books_novels_cart += books_novels_list_price[books_novels_cart_number -
                                                 1] * books_novels_cart_number_qty

    print(books_novels_list[books_novels_cart_number-1],
          "Added Successfully !!!")

    # writing details in text file
    books_novels_items_cart_details_text_file()

    print(books_novels_list_price[books_novels_cart_number-1]
          * books_novels_cart_number_qty)

    print()


def books_novels_items_shopping_items():

    global books_novels_list, books_novels_list_price, books_novels_cart, books_novels_cart_number, books_novels_cart_number_qty

    books_novels_list = ["Arabian Nights", "Rich Dad Poor Dad", "Harry Potter Series", "Sherlock Holmes", "Angles And Demons",
                         "Origin", "Frankenstein", "Invisible Man", "Pride And Prejudice", "Wings Of Fire"]
    books_novels_list_price = [1000, 300, 2700,
                               1000, 260, 250, 120, 175, 120, 420]

    for i in range(0, len(books_novels_list)):
        print(i+1, ". ", books_novels_list[i],
              "     ", books_novels_list_price[i])


def books_novels_items_cart_details_text_file():

    global books_novels_list, books_novels_list_price, books_novels_cart, books_novels_cart_number, books_novels_cart_number_qty
    global cart_items_details

    # writing details in file

    cart_items_details.write("Item Name: ")
    cart_items_details.write(
        books_novels_list[books_novels_cart_number-1])
    cart_items_details.write("   ")
    cart_items_details.write("Quantity: ")
    cart_items_details.write(str(books_novels_cart_number_qty))
    cart_items_details.write("   ")
    cart_items_details.write("Price: ")
    cart_items_details.write(str(
        books_novels_list_price[books_novels_cart_number-1] * books_novels_cart_number_qty))
    cart_items_details.write("\n")


# electronics items shopping functions


def electronics_items_shopping():

    global electronics_items_list, electronics_items_list_price, electronics_items_cart, electronics_items_cart_number, electronics_items_cart_number_qty

    electronics_items_list = ["OnePlus Nord 2", "Macbook M1 Chip", "Asus ROG Strix G17", "Sandisk Pen - Drive",
                              "Samsung External SSD", "Printer", "XP Pen Tablet", "JBL Headphone", "Logitech MX Master 3 Mouse", "Logitech Craft Keyboard"]
    electronics_items_list_price = [
        35000, 200000, 125000, 500, 15000, 20000, 35000, 7000, 9000, 13000]

    electronics_items_cart_number = int(input("Enter Item Number: "))
    electronics_items_cart_number_qty = float(input("Enter Quantity: "))
    electronics_items_cart += electronics_items_list_price[electronics_items_cart_number -
                                                           1] * electronics_items_cart_number_qty

    print(
        electronics_items_list[electronics_items_cart_number-1], "Added Successfully !!!")

    # writing details in text file
    electronics_items_cart_details_text_file()

    print(electronics_items_list_price[electronics_items_cart_number-1]
          * electronics_items_cart_number_qty)

    print()


def electronics_items_shopping_items():

    global electronics_items_list, electronics_items_list_price, electronics_items_cart, electronics_items_cart_number, electronics_items_cart_number_qty

    electronics_items_list = ["OnePlus Nord 2", "Macbook M1 Chip", "Asus ROG Strix G17", "Sandisk Pen - Drive",
                              "Samsung External SSD", "Printer", "XP Pen Tablet", "JBL Headphone", "Logitech MX Master 3 Mouse", "Logitech Craft Keyboard"]
    electronics_items_list_price = [
        35000, 200000, 125000, 500, 15000, 20000, 35000, 7000, 9000, 13000]

    for i in range(0, len(electronics_items_list)):
        print(i+1, ". ", electronics_items_list[i],
              "     ", electronics_items_list_price[i])


def electronics_items_cart_details_text_file():

    global electronics_items_list, electronics_items_list_price, electronics_items_cart, electronics_items_cart_number, electronics_items_cart_number_qty
    global cart_items_details

    # writing details in file

    cart_items_details.write("Item Name: ")
    cart_items_details.write(
        electronics_items_list[electronics_items_cart_number-1])
    cart_items_details.write("   ")
    cart_items_details.write("Quantity: ")
    cart_items_details.write(str(electronics_items_cart_number_qty))
    cart_items_details.write("   ")
    cart_items_details.write("Price: ")
    cart_items_details.write(str(
        electronics_items_list_price[electronics_items_cart_number-1] * electronics_items_cart_number_qty))
    cart_items_details.write("\n")


# clothes items shopping functions


def clothes_items_shopping():

    global clothes_items_list, clothes_items_list_price, clothes_items_cart, clothes_items_cart_number, clothes_items_cart_number_qty

    clothes_items_list = ["T - Shirt", "Shirt", "Pants", "Shorts",
                          "Nightsuit", "Saree", "Kurta Pyzama", "Trousers", "Jeans", "Shoes"]
    clothes_items_list_price = [500, 750, 900,
                                600, 1200, 1000, 1200, 900, 1000, 2200]

    clothes_items_cart_number = int(input("Enter Item Number: "))
    clothes_items_cart_number_qty = float(input("Enter Quantity: "))
    clothes_items_cart += clothes_items_list_price[clothes_items_cart_number -
                                                   1] * clothes_items_cart_number_qty

    print(clothes_items_list[clothes_items_cart_number-1],
          "Added Successfully !!!")

    # writing details in text files
    clothes_items_cart_details_text_file()

    print(clothes_items_list_price[clothes_items_cart_number-1]
          * clothes_items_cart_number_qty)

    print()


def clothes_items_shopping_items():

    global clothes_items_list, clothes_items_list_price, clothes_items_cart, clothes_items_cart_number, clothes_items_cart_number_qty

    clothes_items_list = ["T - Shirt", "Shirt", "Pants", "Shorts",
                          "Nightsuit", "Saree", "Kurta Pyzama", "Trousers", "Jeans", "Shoes"]
    clothes_items_list_price = [500, 750, 900,
                                600, 1200, 1000, 1200, 900, 1000, 2200]

    for i in range(0, len(clothes_items_list)):
        print(i+1, ". ", clothes_items_list[i],
              "     ", clothes_items_list_price[i])


def clothes_items_cart_details_text_file():

    global clothes_items_list, clothes_items_list_price, clothes_items_cart, clothes_items_cart_number, clothes_items_cart_number_qty
    global cart_items_details

    # writing details in file

    cart_items_details.write("Item Name: ")
    cart_items_details.write(clothes_items_list[clothes_items_cart_number-1])
    cart_items_details.write("   ")
    cart_items_details.write("Quantity: ")
    cart_items_details.write(str(clothes_items_cart_number_qty))
    cart_items_details.write("   ")
    cart_items_details.write("Price: ")
    cart_items_details.write(str(
        clothes_items_list_price[clothes_items_cart_number-1] * clothes_items_cart_number_qty))
    cart_items_details.write("\n")


# games items shopping functions


def games_items_shopping():

    global games_items_list, games_items_list_price, games_items_cart, games_items_cart_number, games_items_cart_number_qty

    games_items_list = ["Play Station 5", "X - Box", "Spiderman", "Drone",
                        "GTA San Andres", "Nintendo", "Cars", "Train", "VR Controller", "Play Station Portable"]
    games_items_list_price = [74000, 56000, 1200,
                              7500, 1500, 7000, 1300, 1700, 1800, 12000]

    games_items_cart_number = int(input("Enter Item Number: "))
    games_items_cart_number_qty = float(input("Enter Quantity: "))
    games_items_cart += games_items_list_price[games_items_cart_number -
                                               1] * games_items_cart_number_qty

    print(games_items_list[games_items_cart_number-1],
          "Added Successfully !!!")

    # writing details in text file
    games_items_cart_details_text_file()

    print(games_items_list_price[games_items_cart_number-1]
          * games_items_cart_number_qty)


def games_items_shopping_items():

    global games_items_list, games_items_list_price, games_items_cart, games_items_cart_number, games_items_cart_number_qty

    games_items_list = ["Play Station 5", "X - Box", "Spiderman", "Drone",
                        "GTA San Andres", "Nintendo", "Cars", "Train", "VR Controller", "Play Station Portable"]
    games_items_list_price = [74000, 56000, 1200,
                              7500, 1500, 7000, 1300, 1700, 1800, 12000]

    for i in range(0, len(games_items_list)):
        print(i+1, ". ", games_items_list[i],
              "     ", games_items_list_price[i])


def games_items_cart_details_text_file():

    global games_items_list, games_items_list_price, games_items_cart, games_items_cart_number, games_items_cart_number_qty
    global cart_items_details

    # writing details in file

    cart_items_details.write("Item Name: ")
    cart_items_details.write(games_items_list[games_items_cart_number-1])
    cart_items_details.write("   ")
    cart_items_details.write("Quantity: ")
    cart_items_details.write(str(games_items_cart_number_qty))
    cart_items_details.write("   ")
    cart_items_details.write("Price: ")
    cart_items_details.write(str(
        games_items_list_price[games_items_cart_number-1] * games_items_cart_number_qty))
    cart_items_details.write("\n")


# medicines items shopping functions


def medicines_items_shopping():

    global medicines_items_list, medicines_items_list_price, medicines_items_cart, medicines_items_cart_number, medicines_items_cart_number_qty

    medicines_items_list = ["Paracetamol", "Crocin", "B12 Capsule", "D3 Pouch",
                            "A to Z Multivitamin Capsule", "Clindon Gel", "AcneBar", "Candid - B", "Ear Buds", "Cough Syrup"]
    medicines_items_list_price = [40, 25, 200, 30, 70, 75, 70, 40, 25, 80]

    medicines_items_cart_number = int(input("Enter Item Number: "))
    medicines_items_cart_number_qty = float(input("Enter Quantity: "))
    medicines_items_cart += medicines_items_list_price[medicines_items_cart_number -
                                                       1] * medicines_items_cart_number_qty

    print(
        medicines_items_list[medicines_items_cart_number-1], "Added Successfully !!!")

    # writing details in text file
    medicines_items_cart_details_text_file()

    print(medicines_items_list_price[medicines_items_cart_number-1]
          * medicines_items_cart_number_qty)

    print()


def medicines_items_shopping_items():

    global medicines_items_list, medicines_items_list_price, medicines_items_cart, medicines_items_cart_number, medicines_items_cart_number_qty

    medicines_items_list = ["Paracetamol", "Crocin", "B12 Capsule", "D3 Pouch",
                            "A to Z Multivitamin Capsule", "Clindon Gel", "AcneBar", "Candid - B", "Ear Buds", "Cough Syrup"]
    medicines_items_list_price = [40, 25, 200, 30, 70, 75, 70, 40, 25, 80]

    for i in range(0, len(medicines_items_list)):
        print(i+1, ". ", medicines_items_list[i],
              "     ", medicines_items_list_price[i])


def medicines_items_cart_details_text_file():

    global medicines_items_list, medicines_items_list_price, medicines_items_cart, medicines_items_cart_number, medicines_items_cart_number_qty
    global cart_items_details

    # writing details in file

    cart_items_details.write("Item Name: ")
    cart_items_details.write(
        medicines_items_list[medicines_items_cart_number-1])
    cart_items_details.write("   ")
    cart_items_details.write("Quantity: ")
    cart_items_details.write(str(medicines_items_cart_number_qty))
    cart_items_details.write("   ")
    cart_items_details.write("Price: ")
    cart_items_details.write(str(
        medicines_items_list_price[medicines_items_cart_number-1] * medicines_items_cart_number_qty))
    cart_items_details.write("\n")

# shopping list


def shopping_list():

    global essential_items_list, essential_items_list_price, essential_items_cart, essential_items_cart_number, essential_items_cart_number_qty
    global books_educational_list, books_educational_list_price, books_educational_cart, books_educational_cart_number, books_educational_cart_number_qty
    global books_novels_list, books_novels_list_price, books_novels_cart, books_novels_cart_number, books_novels_cart_number_qty
    global electronics_items_list, electronics_items_list_price, electronics_items_cart, electronics_items_cart_number, electronics_items_cart_number_qty
    global clothes_items_list, clothes_items_list_price, clothes_items_cart, clothes_items_cart_number, clothes_items_cart_number_qty
    global games_items_list, games_items_list_price, games_items_cart, games_items_cart_number, games_items_cart_number_qty
    global medicines_items_list, medicines_items_list_price, medicines_items_cart, medicines_items_cart_number, medicines_items_cart_number_qty
    global cart_items_details
    global choose

    while choose == 3 or choose == 10:

        shopping = 'y'

        if choose == 3:

            cart_items_details = open("Cart Items Details.txt", "w")
            cart_items_details.write("Receipt")
            cart_items_details.write("\n")
            cart_items_details.write("-------")
            cart_items_details.write("\n")
            cart_items_details.write("\n")

        elif choose == 10:

            cart_items_details = open("Cart Items Details.txt", "a")

        while shopping == 'y' or shopping == 'Y':

            print()
            print("CATEGORIES OFFERED BY US")
            print("------------------------")

            print()

            print("1. Essential Items")
            print("2. Books")
            print("3. Electronics")
            print("4. Clothes")
            print("5. Games")
            print("6. Medicine")
            print("7. Post Mail")

            print()
            choice = int(input("Enter Your Choice: "))
            print()

            if choice == 1:

                print("Essential Items")
                print("---------------")

                print()
                print("Item Name", "Price")
                print("---------", "-----")
                print()

                essential_items_shopping_items()

                print()

                # adding items into cart

                category_confirmation = input(
                    "Do you want to add items from this category ... Press 'Y' else Press 'N': ")

                if category_confirmation == "y" or category_confirmation == "Y":

                    essential_items = "y"
                    while essential_items == "y" or essential_items == 'Y':
                        print()

                        essential_items_shopping()

                        essential_items = input(
                            "Do you want to enter more items from Essential Items category ... Press 'Y' else Press 'N': ")
                        print()

                    print()
                    print("Your Total For This Category Is: ",
                          essential_items_cart)
                    print()
                    shopping = input(
                        "Do you want to move to other category: 'Press (Y) for going to other category Press (N) for viewing your cart: ")
                    choose = 4
                    print()

                else:
                    shopping = 'y'
                    print()

            elif choice == 2:

                print("Books")
                print("-------------------")
                print()
                print("1. Educational Books")
                print("2. Novels")
                print()

                books_choice = int(input("Enter Your Choice: "))
                print()
                print()

                if books_choice == 1:

                    print("Item Name", "Price")
                    print("---------", "-----")
                    print()

                    books_educational_items_shopping_items()

                    print()

                    category_confirmation = input(
                        "Do you want to add items from this category ... Press 'Y' else Press 'N': ")

                    if category_confirmation == "y" or category_confirmation == "Y":

                        books_educational = "y"
                        while books_educational == "y" or books_educational == 'Y':
                            print()

                            books_educational_items_shopping()
                            books_educational = input(
                                "Do you want to enter more items from Educational Books category ... Press 'Y' else Press 'N': ")

                    print()
                    print("Your Total For This Category Is: ",
                          books_educational_cart)
                    print()

                    shopping = input(
                        "Do you want to move to other category: 'Press (Y) for going to other category Press (N) for viewing your cart: ")
                    choose = 4

                elif books_choice == 2:

                    print("NOVELS")
                    print("-------")

                    print()

                    print("Item Name", "Price")
                    print("---------", "-----")
                    print()

                    books_novels_items_shopping_items()

                    category_confirmation = input(
                        "Do you want to add items from this category ... Press 'Y' else Press 'N': ")

                    books_novels_cart = 0

                    if category_confirmation == "y" or category_confirmation == "Y":

                        books_novels = "y"
                        while books_novels == "y" or books_novels == 'Y':

                            print()

                            books_novels_items_shopping()
                            books_novels = input(
                                "Do you want to enter more items from Novels Books category ... Press 'Y' else Press 'N': ")
                            print()

                    print()
                    print("Your Total For This Category Is: ", books_novels_cart)
                    print()
                    shopping = input(
                        "Do you want to move to other category: 'Press (Y) for going to other category Press (N) for viewing your cart: ")
                    choose = 4

                else:

                    print("Category Requested")

            elif choice == 3:

                print("ELECTRONICS")
                print("-----------")

                print()

                print("Item Name", "Price")
                print("---------", "-----")
                print()

                electronics_items_shopping_items()

                print()

                category_confirmation = input(
                    "Do you want to add items from this category ... Press 'Y' else Press 'N': ")

                if category_confirmation == "y" or category_confirmation == "Y":

                    electronics_items = "y"
                    while electronics_items == "y" or electronics_items == 'Y':

                        print()

                        electronics_items_shopping()

                        electronics_items = input(
                            "Do you want to enter more items from electronics Items category ... Press 'Y' else Press 'N': ")
                        print()

                    print()
                    print("Your Total For This Category Is: ",
                          electronics_items_cart)
                    print()
                    shopping = input(
                        "Do you want to move to other category: 'Press (Y) for going to other category Press (N) for viewing your cart: ")
                    choose = 4
                    print()

                else:
                    shopping = 'y'
                    print()

            elif choice == 4:

                print("CLOTHES")
                print("--------")

                print()

                print("Item Name", "Price")
                print("---------", "-----")
                print()

                clothes_items_shopping_items()

                print()

                category_confirmation = input(
                    "Do you want to add items from this category ... Press 'Y' else Press 'N': ")

                if category_confirmation == "y" or category_confirmation == "Y":

                    clothes_items = "y"
                    while clothes_items == "y" or clothes_items == 'Y':
                        print()

                        clothes_items_shopping()
                        clothes_items = input(
                            "Do you want to enter more items from Clothes Items category ... Press 'Y' else Press 'N': ")
                        print()

                    print()
                    print("Your Total For This Category Is: ", clothes_items_cart)
                    print()
                    shopping = input(
                        "Do you want to move to other category: 'Press (Y) for going to other category Press (N) for viewing your cart: ")
                    choose = 4
                    print()

                else:
                    shopping = 'y'
                    print()

            elif choice == 5:

                print("GAMES")
                print("-----")

                print()

                print("Item Name", "Price")
                print("---------", "-----")
                print()

                games_items_shopping_items()

                print()

                category_confirmation = input(
                    "Do you want to add items from this category ... Press 'Y' else Press 'N': ")

                if category_confirmation == "y" or category_confirmation == "Y":

                    games_items = "y"
                    while games_items == "y" or games_items == 'Y':
                        print()

                        games_items_shopping()
                        games_items = input(
                            "Do you want to enter more items from Games Items category ... Press 'Y' else Press 'N': ")
                        print()

                    print()
                    print("Your Total For This Category Is: ", games_items_cart)
                    print()
                    shopping = input(
                        "Do you want to move to other category: 'Press (Y) for going to other category Press (N) for viewing your cart: ")
                    choose = 4
                    print()

                else:
                    shopping = 'y'
                    print()

            elif choice == 6:

                print("MEDICINES")
                print("---------")

                print()

                print("Item Name", "Price")
                print("---------", "-----")
                print()

                medicines_items_shopping_items()

                print()

                category_confirmation = input(
                    "Do you want to add items from this category ... Press 'Y' else Press 'N': ")

                if category_confirmation == "y" or category_confirmation == "Y":

                    medicines_items = "y"
                    while medicines_items == "y" or medicines_items == 'Y':
                        print()
                        medicines_items_shopping()
                        medicines_items = input(
                            "Do you want to enter more items from Medicines Items category ... Press 'Y' else Press 'N': ")
                        print()

                    print()
                    print("Your Total For This Category Is: ",
                          medicines_items_cart)
                    print()
                    shopping = input(
                        "Do you want to move to other category: 'Press (Y) for going to other category Press (N) for viewing your cart: ")
                    choose = 4
                    print()

                else:
                    shopping = 'y'
                    print()

            elif choice == 7:

                print("Welcome to our Courier Service")
                print("------------------------------")
                print()
                print(
                    "We offer very affordable rates for your shipment with very fast delivery")
                print("₹ 100 Per Kg")

                print("We are highly Thank You For Choosing Our Service ☺☻☺☻☺☻")

                postmail_records()

                print()
                print()
                print("Your Post Mail Details: ")
                print("------------------------")
                print()

                # displaying the details of postmail

                recipt_record_slip = open("Recipt Record.txt", "r")
                slip = recipt_record_slip.read()
                print(slip)

                shopping = input(
                    "Do you want to move to other category: 'Press (Y) for going to other category Press (N) for viewing your cart: ")
                choose = 4
                print()

            else:
                print("Category Requested")

                shopping = input(
                    "Do you want to move to other category: 'Press (Y) for going to other category Press (N) for viewing your cart: ")

        if shopping == 'n' or shopping == 'N':

            updating_your_cart()

        else:

            print("Wrong Input !!!")

    # shipping record for parcel items
    # funtion not to be called in main


def postmail_records():

    global sendername, senderaddress, sendermobileno, recievername, recieveraddress, recivermobileno, weightofpackage, main_record, recipt_record_list, postmail_total
    global name, username, password, user_account, address, mobileno, email, choose, captcha

    # csv file will have details of all customers and will not display them
    # text file will only save current customer record and will display them

    main_record = open("Main Record.csv", "a", newline='\r\n')
    writer_postmail_record = csv.writer(main_record)
    recipt_record = open("Recipt Record.txt", "w+")

    sender = input(
        "Is your sender name and address same as your account details or not ... If same press 'y' and if no press 'n' ")
    print()

    if sender == 'y' or sender == 'Y':

        # sender details

        sendername = name
        senderaddress = address
        sendermobileno = mobileno

        # reciver details

        print("Reciver Details")
        print("---------------")

        recievername = input("Enter Reciever Name: ")
        recieveraddress = input("Enter Reciver Address: ")
        recivermobileno = int(input("Enter Reciver Mobile Number: "))

        weightofpackage = float(input("Enter weight of package: "))

        writer_postmail_record.writerow(["Sender Name", "Sender Address", "Sender Mobile Number",
                                        "Reciever Name", "Reciver Address", "Reciver Mobile Number", "Weight Of Package"])
        writer_postmail_record.writerow([sendername, senderaddress, sendermobileno,
                                        recievername, recieveraddress, recivermobileno, weightofpackage])
        recipt_record_list = (["Sender Name", "Sender Address", "Sender Mobile Number",
                               "Reciever Name", "Reciver Address", "Reciver Mobile Number", "Weight Of Package"])
        recipt_record_list_value = [sendername, senderaddress, sendermobileno,
                                    recievername, recieveraddress, recivermobileno, weightofpackage]

        postmail_total = weightofpackage*100

        value = 0
        for record in recipt_record_list:
            recipt_record.write(record)
            recipt_record.write(": ")
            recipt_record.write(str(recipt_record_list_value[value]))
            recipt_record.write("\n")
            value += 1

        cart_items_details.write("\n")
        cart_items_details.write("\n")
        cart_items_details.write("Postmail Record")
        cart_items_details.write("\n")
        cart_items_details.write("---------------")
        cart_items_details.write("\n")
        cart_items_details.write("\n")
        cart_items_details.write("Sender Name: ")
        cart_items_details.write(sendername)
        cart_items_details.write("\n")
        cart_items_details.write("Sender Address: ")
        cart_items_details.write(senderaddress)
        cart_items_details.write("\n")
        cart_items_details.write("Sender Mobile Number: ")
        cart_items_details.write(str(sendermobileno))
        cart_items_details.write("\n")
        cart_items_details.write("Reciever Name: ")
        cart_items_details.write(recievername)
        cart_items_details.write("\n")
        cart_items_details.write("Reciever Address: ")
        cart_items_details.write(recieveraddress)
        cart_items_details.write("\n")
        cart_items_details.write("Reciever Mobile Number: ")
        cart_items_details.write(str(recivermobileno))
        cart_items_details.write("\n")
        cart_items_details.write("Weight Of Package: ")
        cart_items_details.write(str(weightofpackage))
        cart_items_details.write("\n")

        main_record.close()
        recipt_record.close()

    elif sender == 'n' or sender == 'N':

        # sender details

        print("Sender Details")
        print("--------------")
        sendername = input("Enter Sender Name: ")
        senderaddress = input("Enter Sender Address: ")
        sendermobileno = int(input("Enter Sender Mobile Number: "))

        print()
        # reciver details

        print("Reciver Details")
        print("---------------")
        recievername = input("Enter Reciever Name: ")
        recieveraddress = input("Enter Reciver Address: ")
        recivermobileno = int(input("Enter Reciver Mobile Number: "))

        print()

        weightofpackage = float(input("Enter weight of package: "))

        writer_postmail_record.writerow(["Sender Name", "Sender Address", "Sender Mobile Number",
                                        "Reciever Name", "Reciver Address", "Reciver Mobile Number", "Weight Of Package"])
        writer_postmail_record.writerow([sendername, senderaddress, sendermobileno,
                                        recievername, recieveraddress, recivermobileno, weightofpackage])

        recipt_record_list = (["Sender Name", "Sender Address", "Sender Mobile Number",
                               "Reciever Name", "Reciver Address", "Reciver Mobile Number", "Weight Of Package"])
        recipt_record_list_value = [sendername, senderaddress, sendermobileno,
                                    recievername, recieveraddress, recivermobileno, weightofpackage]

        postmail_total = weightofpackage*100

        value = 0

        for record in recipt_record_list:
            recipt_record.write(record)
            recipt_record.write(": ")
            recipt_record.write(str(recipt_record_list_value[value]))
            recipt_record.write("\n")
            value += 1

        cart_items_details.write("\n")
        cart_items_details.write("\n")
        cart_items_details.write("Postmail Record")
        cart_items_details.write("\n")
        cart_items_details.write("---------------")
        cart_items_details.write("\n")
        cart_items_details.write("\n")
        cart_items_details.write("Sender Name: ")
        cart_items_details.write(sendername)
        cart_items_details.write("\n")
        cart_items_details.write("Sender Address: ")
        cart_items_details.write(senderaddress)
        cart_items_details.write("\n")
        cart_items_details.write("Sender Mobile Number: ")
        cart_items_details.write(str(sendermobileno))
        cart_items_details.write("\n")
        cart_items_details.write("Reciever Name: ")
        cart_items_details.write(recievername)
        cart_items_details.write("\n")
        cart_items_details.write("Reciever Address: ")
        cart_items_details.write(recieveraddress)
        cart_items_details.write("\n")
        cart_items_details.write("Reciever Mobile Number: ")
        cart_items_details.write(str(recivermobileno))
        cart_items_details.write("\n")
        cart_items_details.write("Weight Of Package: ")
        cart_items_details.write(str(weightofpackage))
        cart_items_details.write("\n")

        main_record.close()
        recipt_record.close()

# otp generator


def otp_generator():

    global otp

    otp = random.randrange(000000, 999999, 6)
    print("Your OTP is: ", otp)

# updating the cart and payment method


def updating_your_cart():

    global card_number, card_nameholder, card_expiry, card_cvv, payment_method
    global essential_items_cart, books_educational_cart, books_novels_cart, electronics_items_cart, clothes_items_cart, games_items_cart, medicines_items_cart, postmail_total
    global choose

    print()
    print("Viewing Your Cart")
    print("-----------------")

    print()

    update_cart = 1
    while update_cart == 1:

        print("Press 1 to view the cart")
        print("Press 2 to move to payment")
        print("Press 3 to continue shopping")
        cart = int(input("Enter Your Choice: "))

        if cart == 1:
            cart_items_details.close()
            print()
            print()
            cart_items_details_receipt = open("Cart Items Details.txt", "r")
            print(cart_items_details_receipt.read())
            print()

            total = essential_items_cart+books_educational_cart+books_novels_cart+electronics_items_cart + \
                clothes_items_cart+games_items_cart+medicines_items_cart+postmail_total

            print("Your Total Is: ", total)
            print()

            update_cart = 1

        elif cart == 2:

            print("Payment")
            print("-------")

            total = essential_items_cart+books_educational_cart+books_novels_cart+electronics_items_cart + \
                clothes_items_cart+games_items_cart+medicines_items_cart+postmail_total
            print("Your Total Is: ", total)
            print("Enter method for payment ")
            payment_method = int(input(
                "Enter (1) for 'Credit Card' Enter (2) for 'Debit Card' Enter (3) for 'Cash On Delivery' :"))

            if payment_method == 1 or payment_method == 2:

                print("Enter Your Card Details")
                print("-----------------------")

                card_number = int(input("Enter Your Card Number: "))
                while len(str(card_number)) != 12:
                    print()
                    print("Invalid Card Number !")
                    print("Try Again")

                    card_number = int(input("Enter Your Card Number: "))

                card_nameholder = input("Enter Card Holder Name: ")
                card_expiry = input("Enter Expiry Date of Card: ")

                card_cvv = int(stdiomask.getpass("Enter CVV: ", mask="*"))
                while len(str(card_cvv)) != 3:
                    print()
                    print("Invalid CVV !")
                    print("Try Again")

                    card_cvv = int(input("Enter Your CVV: "))

                card_storing_confirmation = int(
                    input("Do You Want To Save Your Card Details ... Press (1) else Press (2) "))

                if card_storing_confirmation == 1:
                    storing_card_details()

                otp_final = 1
                while otp_final == 1:

                    otp_generator()
                    otp_input = int(input("Enter otp: "))

                    if otp == otp_input:

                        print("Order Successful")

                        otp_final = 2
                        payment_method = 0
                        cart = 0
                        print()

                        delivery = random.randint(3, 10)
                        print("You will recive your package by", delivery, "days")

                        cart_items_details.close()
                        update_cart = 2
                        

                    else:
                        print("Payment Failed !!!")
                        otp_final = 1

            elif payment_method == 3:

                print("Order Successful ")
                print()
                print("Kindly Arrange", total, "money before delivery")
                delivery = random.randint(3, 10)
                print("You will recive your package by", delivery, "days")

                cart_items_details.close()
                cart_items_details_receipt.close()

                update_cart = 2

        elif cart == 3:
            choose = 10
            shopping_list()


def storing_card_details():

    card_details = open("Card Details.dat", "ab")

    # username to be added in card_fields

    card_fields = [card_number, card_nameholder, card_expiry, card_cvv, '\n']
    pickle.dump(card_fields, card_details)
    card_details.close()


# _main_

connecting_the_database()
creating_user_account()
logging_into_user_account()
shopping_list()
