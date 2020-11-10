from typing import Dict
from random import randint

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
                "Enter 'YES' to create an account.\n"
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


if __name__ == "__main__":
    setupmembership()

