import os

from Cocktails.file_editor import read_csv, write_csv
from Cocktails.classes import Drink
drinks_file = 'drinks.csv'


def print_header(title):
    print("| " + title.upper())


def print_outline():
    print("+================================+")


def clear_screen():
    os.system("cls")

def read_drinks():
    info = read_csv(f'{drinks_file}')
    for line in info:
        drinks_add.append(Drink(line[0], line[1]))


def write_drinks_csv():
    drinks = ([d.drink, d.alcoholic, d.price, d.tequila, d.gin, d.rum,
               d.vermouth, d.tonic, d.lime, d.syrup] for d in drinks_add)
    write_csv(f'{drinks_file}', drinks)


drinks_add = []
drinks = []

