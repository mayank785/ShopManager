# importing modules
from datetime import date, datetime
import csv
from math import prod

# constants
product_list = {}
customer_dues = {}
datetoday = date.today().strftime("%b-%d-%Y")

def l_refresh():
    """ This fuction uses dictionary to update csv file """
    global product_list
    global customer_dues
    with open('products.csv', 'r') as prod:
        read = csv.reader(prod)
        product_list = {rows[0]:rows[1] for rows in read}
        prod.close()
    with open('due.csv', 'r') as due:
        read = csv.reader(due)
        customer_dues = {rows[0]:rows[1] for rows in read}
        due.close()

def lcsv_refresh():
    """ This function uses csv file to update dictionary """
    with open('products.csv', 'w') as products:
        for key in product_list.keys():
            products.write("%s,%s\n"%(key, product_list[key]))
        products.close()
    with open('due.csv', 'w') as due:
        for key in customer_dues.keys():
            due.write("%s,%s\n"%(key, customer_dues[key]))
        due.close()

def startup():
    """ This is the main program """
    l_refresh()
    print("========== MAIN PROGRAM ==========")
    print(f"Date Today : {datetoday}")
    supply()
    start = input("Start work (y or n) : ")
    if start == "n":
        exit()
    elif start == "y":
        bill_maker()
    else:
        print("Invalid input........")

def supply():
    """ This function asks for the number of supplies to manage the records of the products available """
    supply = int(input("Enter the number of supplies today : "))
    for p in range(1, supply + 1):
        supply_rec()

def supply_rec():
    """ This function records the products which were supplied to the shop on that day """
    prod = input("Product name : ")
    unit = int(input("Enter the units : "))
    with open('products.csv', 'a') as products:
        if prod not in product_list:
            products.write(f"{prod}, {unit}")
            product_list[prod] = unit
        else:
            units = unit + int(product_list[prod])
            product_list[prod] = units
            products.write(f"{prod}, {units}")
        products.close()
    lcsv_refresh()

def bill_maker():
    """ This function makes the bill """
    print("========== BILL MAKER ==========")
    cn = input("Enter the customer name : ")
    if cn in customer_dues:
        print(f"This customer already have to pay for last puchase....\nAmount to be paid : {customer_dues[f'{cn}']}")
    total = 0
    print("WHEN ALL ITEMS ARE BILLED JUST SKIP BY TYPING 'e' AND PRESSING ENTER.......")
    with open(f"{cn}"+".txt", "a") as bill:
        bill.write("========== MrCoder ==========")
        bill.write(f"\nCustomer Name : {cn}")
        bill.write(f"\nDate : {datetoday}")
        bill.write(f"\nProduct Name - Unit - Cost Per Unit")
        for items in range(0, 100000000):
            p = input("Product Name : ")
            if p == "e":
                print(f"Total Payable Amount = {total}")
                lcsv_refresh()
                bill.close()
                payment()
                bill_maker()
            u = int(input("Enter the unit purchased : "))
            cpp = int(input("Enter the price per unit : "))
            total += (cpp * u)
            if p not in product_list:
                print("Product not available...")
                continue
            elif p in product_list:
                avail = eval(f"{product_list[f'{p}']} - {str(u)}")
                product_list[f"{p}"] = (avail)
            bill.write(f"\n{p} - {u} - {cpp}")
            lcsv_refresh()
        print(f"Total Payable Amount = {total}")
        payment()
        bill.close()

def payment():
    """ This function controls the payement """
    pay = int(input("Enter the type of payement (0 for on-the-spot and 1 for pay-due/pay-later) : "))
    if pay == 0:
        print("Thank You for the payement.....\nPlease visit again.....")
    elif pay == 1:
        due()
        print("No problem you may pay later.....")
    else:
        print("Invalid input....")
        bill_maker()

def due():
    """ This fuction manages the dues """
    print("========== DUES ==========")
    cust_name = input("Customer name : ")
    cust_due = int(input("Enter the amount : "))
    with open('due.csv', 'a') as due:
        if cust_name not in customer_dues:
            due.write(f"{cust_name}, {cust_due}")
            customer_dues[cust_name] = cust_due
        elif cust_name in customer_dues:
            new_due = int(customer_dues[cust_name]) - cust_due
            customer_dues[cust_name] = new_due
            due.write(f"{cust_name}, {new_due}")
        else:
            new_due = cust_due + int(customer_dues[cust_name])
            customer_dues[cust_name] = new_due
            due.write(f"{cust_name}, {new_due}")
        due.close()
    lcsv_refresh()

startup()       # calling the main fuction/starting the program