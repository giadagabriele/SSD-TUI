import csv
import sys
from getpass import getpass
from pathlib import Path
from typing import Any, Callable, Tuple
from wsgiref import headers

import requests
from domains.dress_loan.menu import Entry, Menu, MenuDescription
from valid8 import ValidationError, validate
import jwt
import re
import uuid

from domains.dress.domain import *
from domains.dress_shop.domain import *
from domains.user.domain import *
from domains.dress_shop.secret import *

from jwt.algorithms import get_default_algorithms

api_server = 'https://ssd.pingflood.tk/api/v1'


class App:
    __filename = Path(__file__).parent.parent / 'shoppingList.csv'
    __delimiter = '\t'
    __logged = False
    __key = None
    __id_dictionary = []

    def __init__(self):
        self.__first_menu = self.init_first_menu()
        self.id_user = None
        self.__choice_menu = self.__init_choice_menu()
        self.__dressloan_menu = self.__init_dressloan_menu()
        self.__dress_menu = self.__init_dress_menu()
        self.__dressList = DressList()
        self.__dressloanList = DressLoanList()
        get_default_algorithms()

    def init_first_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('Dressy'),
                            auto_select=lambda: print('\nWelcome! Please select an option\n')) \
            .with_entry(Entry.create('1', 'Login', is_logged=lambda: self.__login())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye Bye!\n'), is_exit=True)) \
            .build()

    def __init_choice_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('Dressy - Choice Menu'),
                            auto_select=lambda: print('\nSelect the menu to display\n')) \
            .with_entry(Entry.create('1', 'Dress Loan', on_selected=lambda: self.__run_dressloan_menu())) \
            .with_entry(Entry.create('2', 'Dress', on_selected=lambda: self.__run_dress_menu())) \
            .with_entry(Entry.create('0', 'Back to Login', on_selected=lambda: print('Logged out\n'), is_exit=True)) \
            .build()

    #commesso può fare tutto
    #user può fare solo sort ed add
    def __init_dressloan_menu(self) -> Menu:
         return Menu.Builder(MenuDescription('Dressy - Dress Loan Menu'),
                            auto_select=lambda: self.__print_dressloans()) \
            .with_entry(Entry.create('1', 'Sort by total price', on_selected=lambda: self.__dressloanList.sort_by_total_price()))\
            .with_entry(Entry.create('2', 'Add dress loan', on_selected=lambda: self.__add_dressloan()))\
            .with_entry(Entry.create('3', 'Edit dress loan end date TODO', on_selected=lambda: self.__edit_dressloan()))\
            .with_entry(Entry.create('4', 'Delete dress loan', on_selected=lambda: self.__remove_dressloan()))\
            .with_entry(Entry.create('0', 'Back to Choice Menu', on_selected=lambda: print('Make a choice\n'), is_exit=True)) \
            .build()

    '''
    add dress loan va aggiunto al menu di dress?
    in teoria io dovrei chiedere l'id del dress quindi potrebbe diventare una cosa tipo
    inserisci indice dress da prenotare (come remove), parte l'add aggiungendo quell'id automaticamente all'oggetto
    e vai come un normale add loan, che poi ovviamente vedrai nel menu dress loan
    '''

    #commesso può fare tutto
    #user può fare solo sort 
    def __init_dress_menu(self) -> Menu:
         return Menu.Builder(MenuDescription('Dressy - Dress Menu'),
                            auto_select=lambda: self.__print_dresses()) \
            .with_entry(Entry.create('1', 'Sort by price', on_selected=lambda: self.__dressList.sort_by_price()))\
            .with_entry(Entry.create('2', 'Add dress', on_selected=lambda: self.__add_dress()))\
            .with_entry(Entry.create('3', 'Edit dress price TODO', on_selected=lambda: self.__edit_dress()))\
            .with_entry(Entry.create('4', 'Delete dress', on_selected=lambda: self.__remove_dress()))\
            .with_entry(Entry.create('0', 'Back to Choice Menu', on_selected=lambda: print('Make a choice\n'), is_exit=True)) \
            .build()

    def run(self) -> None:
        try:
            self.__run()
        except Exception as e:
            print(e)
            print('Panic error!', file=sys.stderr)

    def __run(self) -> None:
        while not self.__first_menu.run() == (True, False):
            try:
                self.__fetch_dressloan()
                self.__fetch_dress()
            except ValueError as e:
                print(e)
            except RuntimeError:
                print('Failed to connect to the server! Try later!')
                return
            self.__choice_menu.run()

    def __run_dressloan_menu(self) -> None:
        self.__dressloan_menu.run()

    def __run_dress_menu(self) -> None:
        self.__dress_menu.run()

    def __login(self) -> bool:
        done = False
        while not done:
            username = self.__read("Username ", Username)
            if username.value == '0':
                return False
            password = self.__read("Password ", Password)
            if password.value == '0':
                return False

            res = requests.post(url=f'{api_server}/login/', data={'username': username, 'password': password},
                                verify=True)

            if res.status_code != 200:
                print('This user does not exist!\n')
            else:
                self.__key = res.json()['access']
                print(self.decode_token_role(self.__key))
                print('Login succeed\n')
                done = True
        return True

    def decode_token_role(self, key):
        secret=secret_key()
        decoded = jwt.decode(key, secret, algorithms=['HS512'])
        return decoded['groups'][0]


    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                if prompt != 'Password':
                    line = input(f'{prompt}: ')
                else:
                    line = input(f'{prompt}: ')

                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print('Format not satisfied\n')

    def __fetch_dress(self) -> None:
        res = requests.get(url=f'{api_server}/dress/',
                           headers={'Authorization': f'Bearer {self.__key}'}, verify=True)

        if res.status_code != 200:
            raise RuntimeError()

        json = res.json()
        if json is None:
            return
        for item in json:
            uuid = DressID(str(item['id']))
            brand = Brand(str(item['brandType']))
            price = Price.create(int(int(item['priceInCents']) / 100), int(item['priceInCents']) % 100)
            material = Material(str(item['materialType']))
            color = Color(str(item['colorType']))
            size = Size(int(item['size']))
            description = Description(str(item['description']))
            deleted = Deleted(bool(item['deleted']))
            dress = Dress(uuid, brand, price, material, color, size, description, deleted)
            self.__dressList.add_dress(dress)

    def __fetch_dressloan(self) -> None:
        res = requests.get(url=f'{api_server}/loan/',
                        headers={'Authorization': f'Bearer {self.__key}'}, verify=True)
        
        if res.status_code != 200:
            raise RuntimeError()

        json = res.json()
        if json is None:
            return

        for item in json:
            uuidDressLoan = DressLoanID(str(item['id']))
            startDate = StartDate(str(item['startDate']))
            endDate = EndDate(str(item['endDate']))
            dressID = DressID(str(item['dress']))
            loaner = UserID(int(item['loaner']))
            totalPrice = Price(int(item['totalPrice']))
            loanDurationDays = DurationDays (int(item['loanDurationDays']))
            insertBy = UserID(int(item['insertBy']))
            terminated = Terminated(bool(item['terminated']))
            dressloan = DressLoan(uuidDressLoan, startDate, endDate, dressID, loaner, totalPrice, loanDurationDays, insertBy, terminated)
            self.__dressloanList.add_dressloan(dressloan)

    def __print_dressloans(self) -> None:
        if self.__dressloanList.length() == 0:
            return
        print_sep = lambda: print('-' * 180)
        print_sep()
        fmt = '%-10s %-30s  %-20s  %-20s %-30s %-10s'
        print(fmt % ('Number', 'Start-Date', 'End-Date', 'Total Price', 'Duration Days', 'Terminated'))      #description? 
        print_sep()
        for index in range(self.__dressloanList.length()):
            item = self.__dressloanList.item(index)
            print(fmt % (index + 1, item.startDate.value, item.endDate.value, 
                            item.totalPrice.__str__(), item.loanDurationDays.value, item.terminated.value))
        print_sep()

    def __print_dresses(self) -> None:
        if self.__dressList.length() == 0:
            return
        print_sep = lambda: print('-' * 180)
        print_sep()
        fmt = '%-10s %-20s  %-20s  %-20s %-20s %-20s %-30s %-10s'
        print(fmt % ('Number', 'Brand', 'Price', 'Material', 'Color', 'Size', 'Description', 'Deleted'))
        print_sep()
        for index in range(self.__dressList.length()):
            item = self.__dressList.item(index)
            print(fmt % (index + 1, item.brand.value, item.price.__str__(), item.material.value,
                         item.color.value, item.size.value, item.description.value, item.deleted.value))
        print_sep()

    def __read_dress(self) -> Tuple[DressID, Brand, Price, Material, Color, Size, Description, Deleted]:        #Date poi nell'add darà problemi?
        dress_uuid = uuid.uuid4()
        dress_uuidStr = str(dress_uuid)
        id = DressID(dress_uuidStr)
        dress_id = id
        brand = self.__read('Brand (GUCCI or ARMANI or VALENTINO)', Brand)
        price = self.__read('Price', Price.parse)
        material = self.__read('Material (WOOL or SILK or COTTON)', Material)
        color = self.__read('Color (BLACK or BLUE or WHITE or RED or PINK or GRAY)', Color)
        size = self.__read('Size (from 38 to 60)', int)
        real_size = Size(size)
        description = self.__read('Description', Description)
        deleted = Deleted(False)
        return dress_id, brand, price, material, color, real_size, description, deleted

                                                                                 #loaner                     #insertBy
    def __read_dressloan(self) -> Tuple[DressLoanID, StartDate, EndDate, DressID, UserID, Price, DurationDays, UserID, Terminated]:
        loan_uuid = uuid.uuid4()
        loan_uuidStr = str(loan_uuid)
        loan_id = DressLoanID(loan_uuidStr)
        start_date = self.__read('Start Date (format yyyy-mm-dd)', StartDate)
        end_date = self.__read('End Date (format yyyy-mm-dd)', EndDate)
        dress_uuid = uuid.uuid4()
        dress_uuidStr = str(dress_uuid)
        dress_id = DressID(dress_uuidStr)   #numero di prova va calcolato
        loaner_id = UserID(4)           #numero di prova va calcolato
        total_price = Price(125)            #numero di prova va calcolato
        duration_days = DurationDays(2)                 #numero di prova va calcolato
        insertby_id = UserID(5)           #numero di prova va calcolato
        terminated = Terminated(False)
        return loan_id, start_date, end_date, dress_id, loaner_id, total_price, duration_days, insertby_id, terminated

    def __add_dress(self) -> None:
        newDress = Dress(*self.__read_dress())
        self.__dressList.add_dress(newDress)
        print('Dress added!\n')
        #chiamata al backend permanente

    def __remove_dress(self) -> None :
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressList.length())
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!\n')
            return
        self.__dressList.remove_dress_by_index(index - 1)
        print('Dress removed!\n')
        #chiamata al backend permanente
    
    def __edit_dress(self) -> None :
        pass
        '''
        qui faremo un edit del prezzo
        quindi lato terminale chiederemo:
            -indice dress (come remove) 
            -inserisci prezzo nuovo
        lato codice dobbiamo prendere tutto il Dress, modificare il campo prezzo
        e dare al backend tramite PUT
        '''
        #chiamata al backend permanente

    def __add_dressloan(self) -> None:
        newDressLoan = DressLoan(*self.__read_dressloan())
        self.__dressloanList.add_dressloan(newDressLoan)
        print('Dress Loan added!\n')
        #chiamata al backend permanente

    def __remove_dressloan(self) -> None :
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressloanList.length())
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!\n')
            return
        self.__dressloanList.remove_dressloan_by_index(index - 1)
        print('Dress removed!\n')
        #chiamata al backend permanente

    def __edit_dressloan(self) -> None :
        pass
        '''
        qui faremo un edit della data finale
        quindi lato terminale chiederemo:
            -indice dress loan (come remove) 
            -inserisci nuova data
        lato codice dobbiamo prendere tutto il DressLoan, modificare il campo end_date
        e dare al backend tramite PUT
        '''
        #chiamata al backend permanente