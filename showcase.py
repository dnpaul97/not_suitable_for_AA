import csv
import sys
import os
import collections
import enum
#
from typing import Dict
from random import randint
#
from Cocktails.classes import Drink
from Cocktails.functions import print_header, print_outline, clear_screen, read_drinks, write_drinks_csv, drinks_add, drinks

class Voucher:
    def __init__(self, personal_email):
        self.voucher_code = "".join(["{}".format(randint(0, 9)) for num in range(0, 5)])
        self.personal_email = personal_email

    def print_voucher_code(self):
        print("Your voucher code is {}.".format(self.voucher_code))

class Membership:
    def __init__(self):
        self.membership: Dict[str, Voucher] = {}

    def create_membership(self):
        name = input("Please input your full name: ")
        email = input("Please enter your email adress: ")
        print("We have sent you our new promotional offers to {}".format(email))
        account = Voucher(email)
        self.membership[name] = account
        account.print_voucher_code()

class AccountPlan:
    def __init__(self, bank: Membership):
        self.bank = bank

    def do_bank_menu(self):
        while True:
            choice = input(
                "PLease type 'YES' if you've read all the terms and conditions and want to create an account.\n"
            )
            if choice not in ["YES"]:
                print("Please enter 'YES' if you a agree to the terms and conditions")
            else:
                return choice

    def run(self):
        while True:
            user_choice = self.do_bank_menu()
            if user_choice == "YES":
                self.bank.create_membership()
                break
            else:
                break


def setupmembership():
    account = Membership()
    account_plan = AccountPlan(account)
    account_plan.run()
    print("Thank you for signing up")

class Action(enum.Enum):
    ORDER = "Order"  # Order A Cocktail or more
    PERSONALISE = "Personalise"  # Make Your Own Drink
    STOCKUP = "Add"  # Add to stock
    RECEIPT = "Receipt"  # See the receipt of your purchases
    RETURN = "Return"  # Return to home menu
    INVENTORY = "Inventory"  # See inventory of everything


def ask_action():
    possible_values = ", ".join([action.value for action in Action])
    while True:
        answer = input(f"Please type what you want to do? ({possible_values}):\n")
        try:
            return Action(answer)
        except ValueError:
            print(f"This answer is not valid: {answer}")


def ask_drink():
    choices = {1: "Margarita", 2: "Gin & Tonic",
               3: "Negroni", 4: "Martini", 5: "Manhattan", 6: "Daiquiri", 0: "back to main menu"}
    possible_values = ", ".join(
        f"{value} - {name}" for value, name in sorted(choices.items()))
    while True:
        answer = input(f"What do you want to order?  ({possible_values}):\n")
        try:
            value = int(answer)
            if value in choices:
                return value
            print(f"This answer is not valid: {answer}")
        except ValueError:
            print(f"This is not a number: {answer}")


def ask_quantity(msg):
    while True:
        answer = input(msg + "\n")
        try:
            value = int(answer)
            if value >= 0:
                return value
            print(f"This answer is not valid: {answer}")
        except ValueError:
            print(f"This is not a number: {answer}")


Consumption = collections.namedtuple(
    "Consumption", "tequila, gin, rum, vermouth, tonic_water, lime_juice, syrup, price")


class NotEnoughSupplyError(Exception):
    def __init__(self, supply):
        msg = f"Sorry, not enough {supply}"
        super(NotEnoughSupplyError, self).__init__(msg)


class Minibar:
    def __init__(self):
        # quantities of cocktail ingredients
        self.tequila = 500
        self.gin = 540
        self.rum = 500
        self.vermouth = 400
        self.tonic_water = 300
        self.lime_juice = 500
        self.syrup = 150
        self.price = 0
        self.openforbusiness = True

    def execute_action(self, action):
        if action == Action.ORDER:
            self.order()
        elif action == Action.PERSONALISE:
            self.personalise()
        elif action == Action.STOCKUP:
            self.stockup()
        elif action == Action.RECEIPT:
            self.receipt()
        elif action == Action.RETURN:
            self.openforbusiness = False
        elif action == Action.INVENTORY:
            self.show_inventory()
        else:
            raise NotImplementedError(action)

    def available_check(self, consumption):
        """
        Checks if it can afford making cocktail

        :param consumption: the Consumption
        :raise NotEnoughSupplyError: if at least one supply is missing.
        """
        if self.tequila - consumption.tequila < 0:
            raise NotEnoughSupplyError("Tequila")
        elif self.gin - consumption.gin < 0:
            raise NotEnoughSupplyError("Gin")
        elif self.rum - consumption.rum < 0:
            raise NotEnoughSupplyError("Rum")
        elif self.vermouth - consumption.vermouth < 0:
            raise NotEnoughSupplyError("Vermouth")
        elif self.tonic_water - consumption.tonic_water < 0:
            raise NotEnoughSupplyError("Tonic Water")
        elif self.lime_juice - consumption.lime_juice < 0:
            raise NotEnoughSupplyError("Lime Juice")
        elif self.syrup - consumption.syrup < 0:
            raise NotEnoughSupplyError("Syrup")

    def order(self):
        drink = ask_drink()
        if drink == 0:
            return
        margarita_cons = Consumption(
            tequila=250, gin=0, rum=0, vermouth=0, tonic_water=0, lime_juice=250, syrup=0, price=7.50)
        ginandtonic_cons = Consumption(
            tequila=0, gin=180, rum=0, vermouth=0, tonic_water=150, lime_juice=150, syrup=0, price=5.00)
        negroni_cons = Consumption(
            tequila=0, gin=250, rum=0, vermouth=200, tonic_water=0, lime_juice=0, syrup=0, price=8.00)
        martini_cons = Consumption(
            tequila=0, gin=200, rum=0, vermouth=250, tonic_water=0, lime_juice=0, syrup=0, price=8.00)
        manhattan_cons = Consumption(
            tequila=0, gin=0, rum=250, vermouth=200, tonic_water=0, lime_juice=0, syrup=0, price=7.50)
        daiquiri_cons = Consumption(
            tequila=0, gin=0, rum=250, vermouth=0, tonic_water=0, lime_juice=100, syrup=50, price=8.50)
        consumption = {1: margarita_cons, 2: ginandtonic_cons,
                       3: negroni_cons, 4: martini_cons, 5: manhattan_cons, 6: daiquiri_cons}[drink]
        try:
            self.available_check(consumption)
        except NotEnoughSupplyError as exc:
            print(exc)
        else:
            print("I have enough resources, making you a cocktail!")
            self.tequila -= consumption.tequila
            self.gin -= consumption.gin
            self.rum -= consumption.rum
            self.vermouth -= consumption.vermouth
            self.tonic_water -= consumption.tonic_water
            self.lime_juice -= consumption.lime_juice
            self.syrup -= consumption.syrup
            self.price += consumption.price

    def personalise(self):
        """
        Personalise Cocktail
        """
        self.tequila -= ask_quantity(
            "Write how many ml of Tequila do you want to add:")
        self.gin -= ask_quantity("Write how many ml of Gin do you want to add:")
        self.rum -= ask_quantity("Write how many ml of Rum do you want to add:")
        self.vermouth -= ask_quantity(
            "Write how many ml of Vermouth do you want to add:")
        self.tonic_water -= ask_quantity(
            "Write how many ml of Tonic Water do you want to add:")
        self.lime_juice -= ask_quantity(
            "Write how many ml of Lime Juice do you want to add:")
        self.syrup -= ask_quantity(
            "Write how many ml of Syrup do you want to add:")

    def stockup(self):
        """
        Stock Up on Ingredients
        """
        self.tequila += ask_quantity(
            "Write how many ml of Tequila do you want to add to stock:")
        self.gin += ask_quantity(
            "Write how many ml of Gin do you want to add to stock:")
        self.rum += ask_quantity(
            "Write how many ml of Rum do you want to add to stock:")
        self.vermouth += ask_quantity(
            "Write how many ml of Vermouth do you want to add to stock:")
        self.tonic_water += ask_quantity(
            "Write how many ml of Tonic Water do you want to add to stock:")
        self.lime_juice += ask_quantity(
            "Write how many ml of Lime Juice do you want to add to stock:")
        self.syrup += ask_quantity(
            "Write how many ml of Syrup do you want to add to stock:")

    def receipt(self):
        """
        See how much you spent
        """
        print(f"You spent ${self.price} today")
        self.price = 0

    def show_inventory(self):
        """
        Display the quantities of supplies in the machine at the moment
        """
        print(f"The minibar has (ml):")
        print(f"{self.tequila} of Tequila")
        print(f"{self.gin} of Gin")
        print(f"{self.rum} of Rum")
        print(f"{self.vermouth} of Vermouth")
        print(f"{self.tonic_water} of Tonic Water")
        print(f"{self.lime_juice} of Lime Juice")
        print(f"{self.syrup} of Syrup")
        print(f"${self.price} of Cash")


def main():
    machine = Minibar()
    while machine.openforbusiness:
        action = ask_action()
        machine.execute_action(action)

print_header("Cocktails, Price(£)")
print_outline()

path = 'c:\\GENERATION\\'  # Show menu

file = open("drinks.csv", "r")
reader = csv.reader(file)
for line in reader:
    t = line[0], line[2]
    print(t)
    print_outline()

while True:
    print('''Please select an option below:
          [1] Add a New Drink To The Menu (Drink, Alcoholic, Price, Ingredients)
          [2] See Options
          [3] Sign Up to Receive 2 FOR 1 COCKTAILS 
          [4] Exit
          ''')
    option = input('Enter Your Option: ')


    if option == '1':
        clear_screen()
        chances = 3
        while chances >= 0:
            pin = int(input("Please Enter You 4 Digit Pin: "))
            if pin == (1234):
                print("You entered you pin Correctly\n")
                d1 = Drink(input('Add Drink: '), input(
                    'Is drink alcoholic(Y/N)? '), float(input('Price: ')), int(input(
                        'Tequila(ml): ')), int(input('Gin(ml): ')), int(input('Rum(ml): ')), int(input('Vermouth(ml): ')), int(input('Tonic Water(ml): ')), int(input('Lime Juice(ml): ')), int(input('Syrup(ml): ')))
                drinks_add.append(d1)
                print("----------------")
                write_drinks_csv()
                print('Entry added to drinks.csv')
                exit()
            elif pin != ("1234"):
                print("Incorrect Password")
                chances = chances - 1
                if chances == 0:
                    print("\nNo more tries")
                    break

    if option == '2':
        # Cocktail Menu
        clear_screen()
        p1 = int(input('Age: '))
        if p1 < 18:
            print('  Too young to drink. Grow up')
            exit()
        else:
            if __name__ == '__main__':
                main()

        # for drinks_list in drinks:
        #     print(drinks_list)
        
    if option == '3':
        if __name__ == "__main__":
            setupmembership()

    if option == '4':
        exit()
