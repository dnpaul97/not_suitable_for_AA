class Drink():
    '''Describes a drink'''

    def __init__(self, drink, alcoholic, price, tequila, gin, rum, vermouth, tonic, lime, syrup):
        self.drink = drink
        self.alcoholic = alcoholic
        self.price = price
        self.tequila = tequila
        self.gin = gin
        self.rum = rum
        self.vermouth = vermouth
        self.tonic = tonic
        self.lime = lime
        self.syrup = syrup

    def __repr__(self):
        return(f'Drink: {self.drink}, Alcohol: {self.alcoholic}, Price: {self.price}, Tequila: {self.tequila}, Gin: {self.gin}, Rum: {self.rum}, Vermouth: {self.vermouth}, Tonic: {self.tonic}, Lime: {self.lime}, Syrup: {self.syrup}')

