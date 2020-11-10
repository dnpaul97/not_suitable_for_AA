import collections
import enum


class Action(enum.Enum):
    BUY = "Buy"  # Buy A Cocktail
    PERSONALISE = "Personalise"  # Make Your Own Drink
    STOCKUP = "Add"  # Add to stock
    TAKE = "Take"  # Take your earnings from today
    EXIT = "Exit"  # Close down the app
    INVENTORY = "Inventory"  # See inventory of everything


def ask_action():
    possible_values = ", ".join([action.value for action in Action])
    while True:
        answer = input(f"Write action ({possible_values}):\n")
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
        answer = input(f"What do you want to buy?  ({possible_values}):\n")
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
            drinks_add.append(value)
            print("----------------")
            drinks = ([d.value] for d in drinks_add)
            write_csv(f'{drinks_file}', drinks)
            print('Entry added to drinks.csv')

            
            
def read_drinks():
    info = read_csv(f'{drinks_file}')
    for line in info:
        drinks_add.append(Drink(line[0], line[1]))


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
        if action == Action.BUY:
            self.buy()
        elif action == Action.PERSONALISE:
            self.personalise()
        elif action == Action.STOCKUP:
            self.stockup()
        elif action == Action.TAKE:
            self.take()
        elif action == Action.EXIT:
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

    def buy(self):
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
        self.tequila -= ask_quantity("Write how many ml of Tequila do you want to add:")
        self.gin -= ask_quantity("Write how many ml of Gin do you want to add:")
        self.rum -= ask_quantity("Write how many ml of Rum do you want to add:")
        self.vermouth -= ask_quantity("Write how many ml of Vermouth do you want to add:")
        self.tonic_water -= ask_quantity("Write how many ml of Tonic Water do you want to add:")
        self.lime_juice -= ask_quantity("Write how many ml of Lime Juice do you want to add:")
        self.syrup -= ask_quantity("Write how many ml of Syrup do you want to add:")
        

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

    def take(self):
        """
        Take the money from the machine
        """
        print(f"You earned ${self.price} today")
        self.price = 0

    def show_inventory(self):
        """
        Display the quantities of supplies in the machine at the moment
        """
        print(f"The coffee machine has:")
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


if __name__ == '__main__':
    main()

