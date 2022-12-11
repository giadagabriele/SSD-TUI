import csv
import getpass
import json
import os
import re
import sys
import uuid
from getpass import getpass
from pathlib import Path
from typing import Any, Callable, Tuple
from wsgiref import headers

import jwt
import requests
from jwt.algorithms import get_default_algorithms
from rich.console import Console
from rich.status import Status
from rich import inspect
from valid8 import ValidationError, validate

from domains.dress.domain import *
from domains.dress_loan.menu import Entry, Menu, MenuDescription
from domains.dress_shop.domain import *
from domains.user.domain import *
from settings import *

api_server = settings['BASE_URL']

class App:
    __key = None
    __refreshKey = None
    __userID = None
    __role = None
    __username = None
    __console = None

    def __init__(self):
        self.__console=Console()
        self.__first_menu = self.init_first_menu()
        self.id_user = None
        self.__choice_menu = self.__init_choice_menu()
        self.__dressloan_menu_commessi = self.__init_dressloan_menu_commessi()
        self.__dressloan_menu_user = self.__init_dressloan_menu_user()
        self.__dress_menu_commessi = self.__init_dress_menu_commessi()
        self.__dress_menu_user = self.__init_dress_menu_user()
        self.__dressList = DressList()
        self.__dressloanList = DressLoanList()
        get_default_algorithms()

    def init_first_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('Dressy'),
                            auto_select=lambda: print('\nWelcome! Please select an option\n')) \
            .with_entry(Entry.create('1', 'Login', is_logged=lambda: self.__login())) \
            .with_entry(Entry.create('2', 'Logout', on_selected=lambda: self.__logout(), is_exit=True)) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye Bye!\n'), is_exit=True)) \
            .build()

    def __init_choice_menu(self) -> Menu:
        return Menu.Builder(MenuDescription('Dressy - Choice Menu'),
                            auto_select=lambda: print('\nSelect the menu to display\n')) \
            .with_entry(Entry.create('1', 'Dress Loan', on_selected=lambda: self.__run_dressloan_menu())) \
            .with_entry(Entry.create('2', 'Dress', on_selected=lambda: self.__run_dress_menu())) \
            .with_entry(Entry.create('0', 'Back to Login', on_selected=lambda: print('Logged out\n'), is_exit=True)) \
            .build()

    def __init_dressloan_menu_commessi(self) -> Menu:
         return Menu.Builder(MenuDescription('Dressy - Dress Loan Menu'),
                            auto_select=lambda: self.__print_dressloans()) \
            .with_entry(Entry.create('1', 'Sort by total price', on_selected=lambda: self.__dressloanList.sort_by_total_price()))\
            .with_entry(Entry.create('2', 'Extend loan', on_selected=lambda: self.__edit_dressloan_end_date()))\
            .with_entry(Entry.create('3', 'Close loan', on_selected=lambda: self.__remove_dressloan()))\
            .with_entry(Entry.create('0', 'Back to Choice Menu', on_selected=lambda: print('Make a choice\n'), is_exit=True)) \
            .build()

    def __init_dressloan_menu_user(self) -> Menu:
         return Menu.Builder(MenuDescription('Dressy - Dress Loan Menu'),
                            auto_select=lambda: self.__print_dressloans()) \
            .with_entry(Entry.create('1', 'Sort by total price', on_selected=lambda: self.__dressloanList.sort_by_total_price()))\
            .with_entry(Entry.create('0', 'Back to Choice Menu', on_selected=lambda: print('Make a choice\n'), is_exit=True)) \
            .build()

    def __init_dress_menu_commessi(self) -> Menu:
         return Menu.Builder(MenuDescription('Dressy - Dress Menu'),
                            auto_select=lambda: self.__print_dresses()) \
            .with_entry(Entry.create('1', 'Sort by price', on_selected=lambda: self.__dressList.sort_by_price()))\
            .with_entry(Entry.create('2', 'Add dress', on_selected=lambda: self.__add_dress()))\
            .with_entry(Entry.create('3', 'Edit dress price', on_selected=lambda: self.__edit_dress_price()))\
            .with_entry(Entry.create('4', 'Make dress unavailable', on_selected=lambda: self.__remove_dress()))\
            .with_entry(Entry.create('5', 'Reserve', on_selected=lambda: self.__add_dressloan()))\
            .with_entry(Entry.create('0', 'Back to Choice Menu', on_selected=lambda: print('Make a choice\n'), is_exit=True)) \
            .build()

    def __init_dress_menu_user(self) -> Menu:
         return Menu.Builder(MenuDescription('Dressy - Dress Menu'),
                            auto_select=lambda: self.__print_dresses()) \
            .with_entry(Entry.create('1', 'Sort by price', on_selected=lambda: self.__dressList.sort_by_price()))\
            .with_entry(Entry.create('2', 'Reserve', on_selected=lambda: self.__add_dressloan()))\
            .with_entry(Entry.create('0', 'Back to Choice Menu', on_selected=lambda: print('Make a choice\n'), is_exit=True)) \
            .build()

    def run(self) -> None:
        try:
            self.__run()
        except KeyboardInterrupt:
            self.__console.print("\nBye!")
            sys.exit()
        except Exception as e:
            print(e)
            print('Panic error!', file=sys.stderr)

    def __run(self) -> None:
        while not self.__first_menu.run() == (True, False):
            try:
                self.__fetch_dress()
                self.__fetch_dressloan()
            except ValueError as e:
                print(e)
            except RuntimeError:
                print('Failed to connect to the server! Try later!')
                return
            self.__choice_menu.run()

    def __run_dressloan_menu(self) -> None:
        if self.__role =='commessi':
            self.__dressloan_menu_commessi.run()
        elif  self.__role =='user':
            self.__dressloan_menu_user.run()

    def __run_dress_menu(self) -> None:
        if  self.__role =='commessi':
            self.__dress_menu_commessi.run()
        elif  self.__role =='user':
            self.__dress_menu_user.run()

    def __login(self) -> bool:
        done = False
        while not done:
            try:
                f = open("token.txt", "r")
            except:
                f = open("token.txt", "w")
                f.close()
                f = open("token.txt", "r")
            files = f.read()

            if files and files != '' and len(files) > 0:
                credentials = json.loads(files)
                self.__key = credentials['access']
                self.__refreshKey = credentials['refresh']
                try:
                    self.decode_token_role(self.__key)
                    self.__console.print(f"\nHello, [bold cyan]{self.__username}[/bold cyan]")
                    self.__console.print("[i](If you want insert new credentials, do logout or delete token.txt)[/i]\n")
                    done = True
                except jwt.ExpiredSignatureError as e:
                    self.__console.print("\nToken [bold red]Expired[/bold red]\n")

                    with self.__console.status("Token renew...") as status:
                        self.__tokenRenew()
                        self.decode_token_role(self.__key)
                        self.__console.print("\nToken [bold green]renewed[/bold green]\n")
                    
                    self.__console.print(f"\nHello, [bold cyan]{self.__username}[/bold cyan]")
                    self.__console.print("[i](If you want insert new credentials, do logout or delete token.txt)[/i]\n")
                    done = True
                except jwt.InvalidSignatureError as e:
                    self.__console.print("[bold red]Token invalid![/bold red]")
                    self.__console.print("Logout or delete token.txt and run again!\n")
                    done = False

            else:
                username = self.__read("Username", Username)
                if username.value == '0':
                    return False
                password = self.__read("Password", Password)
                if password.value == '0':
                    return False
                with self.__console.status("Login...") as status:
                    res = requests.post(url=f'{api_server}/login/', data={'username': username, 'password': password},
                                        verify=True)

                if res.status_code != 200:
                    self.__console.print('[bold red]This user does not exist![/bold red]\n')
                else:
                    self.__key = res.json()['access']
                    self.__refreshKey = res.json()['refresh']
                    self.__console.print('Login [bold green]success[/bold green]\n')
                    self.decode_token_role(self.__key)
                    self.__console.print(f"\nHello, [bold cyan]{self.__username}[/bold cyan]")
                    self.__console.print("[i](If you want insert new credentials, do logout or delete token.txt)[/i]\n")
                    f = open("token.txt", "w")
                    f.write(json.dumps(res.json()))
                    f.close()
                    done = True
        return True

    def __tokenRenew(self) -> None:
        res = requests.post(url=f'{api_server}/token/refresh/', json={'refresh': self.__refreshKey},verify=True)
        self.__key=res.json()['access']
        f = open("token.txt", "w")
        f.write(json.dumps({
            "access": self.__key,
            "refresh": self.__refreshKey
        }))
        f.close()
    
    def __logout(self) -> bool:
        if os.path.exists("token.txt"):
            os.remove("token.txt")
        print("Logout!")
        return True

    def decode_token_role(self, key):
        secret = settings['SECRET_KEY']
        decoded = jwt.decode(key, secret, algorithms=['HS512'])
        self.__userID = decoded['user_id']
        self.__role = decoded['groups'][0]
        self.__username = decoded['username']


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
        self.__dressList.clear() 
        res = requests.get(url=f'{api_server}/dress/', verify=True, headers={'Authorization': f'Bearer {self.__key}'})    
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
        self.__dressloanList.clear()
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
        fmt = '%-10s %-30s  %-20s  %-20s %-30s %-20s %-10s'
        print(fmt % ('Number', 'Start-Date', 'End-Date', 'Total Price', 'Duration Days', 'Loaner ID', 'Terminated'))      #description? 
        print_sep()
        for index in range(self.__dressloanList.length()):
            item = self.__dressloanList.item(index)
            print(fmt % (index + 1, item.startDate.value, item.endDate.value, 
                            item.totalPrice.__str__(), item.loanDurationDays.value, item.loaner.value, item.terminated.value))
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
        dress_id = DressID(dress_uuidStr)      #numero tmp verrà sovrascritto con i dati aggiornati dal backend
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
        loan_id = DressLoanID(loan_uuidStr)     #numero tmp verrà sovrascritto con i dati aggiornati dal backend
        start_date = self.__read('Start Date (format yyyy-mm-dd)', StartDate)
        end_date = self.__read('End Date (format yyyy-mm-dd)', EndDate)
        dress_uuid = uuid.uuid4()
        dress_uuidStr = str(dress_uuid)
        dress_id = DressID(dress_uuidStr)  #numero tmp verrà sovrascritto tramite indice di dress
        loaner_id = self.__read('Loaner (if you are a user PRESS ENTER)', str)
        if loaner_id == "":
            loaner_id = self.__userID
        real_loaner_id = UserID(int(loaner_id))      
        total_price = Price(125)            #numero tmp verrà sovrascritto con i dati aggiornati dal backend
        duration_days = DurationDays(2)            #numero tmp verrà sovrascritto con i dati aggiornati dal backend
        insertby_id = UserID(3)       #numero tmp verrà sovrascritto tramite login
        terminated = Terminated(False)
        return loan_id, start_date, end_date, dress_id, real_loaner_id, total_price, duration_days, insertby_id, terminated

    def __add_dress(self) -> None:
        newDress = Dress(*self.__read_dress())
              
        newDressJSON = {
        "brandType": newDress.brand.value,
        "priceInCents": newDress.price.value_in_cents,
        "materialType": newDress.material.value,
        "colorType": newDress.color.value,
        "size": newDress.size.value,
        "description": newDress.description.value,
        "deleted": newDress.deleted.value,
        }

        res = requests.post(url=f'{api_server}/dress/', json=newDressJSON, verify=True, headers={'Authorization': f'Bearer {self.__key}'})

        self.__fetch_dress()

        print('Dress added!\n')


    def __remove_dress(self) -> None :
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressList.length())
            return int(value)


        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!\n')
            return

        oldDress = self.__dressList.item(index - 1)

        self.__dressList.remove_dress_by_index(index - 1)

        res = requests.delete(url=f'{api_server}/dress/{oldDress.id.value}', verify=True, headers={'Authorization': f'Bearer {self.__key}'})
        #print(res)

        self.__fetch_dress()

        print('Dress marked as unavailable!\n')
    
    def __edit_dress_price(self) -> None :
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressList.length())
            return int(value)


        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!\n')
            return

        edited_dress = self.__dressList.item(index - 1)
        edited_price = self.__read('Price', Price.parse)
        edited_dress.price = edited_price
        

        newEditedDressJSON = {
        "brandType": edited_dress.brand.value,
        "priceInCents": edited_dress.price.value_in_cents,
        "materialType": edited_dress.material.value,
        "colorType": edited_dress.color.value,
        "size": edited_dress.size.value,
        "description": edited_dress.description.value,
        "deleted": edited_dress.deleted.value,
        }

        res = requests.put(url=f'{api_server}/dress/{edited_dress.id.value}', json=newEditedDressJSON, verify=True, headers={'Authorization': f'Bearer {self.__key}'})
        #print(res.json())

        self.__fetch_dress()

        print('Dress price edited!\n')
        

    def __add_dressloan(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressList.length())
            return int(value)
        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Selected!\n')
            return
        dress_selected = self.__dressList.item(index - 1)
        newDressLoan = DressLoan(*self.__read_dressloan())
        newDressLoan.dressID = DressID(dress_selected.id.value)
        newDressLoan.insertBy = UserID(self.__userID)
        newDressLoanJSON = {
        "startDate": newDressLoan.startDate.value,
        "endDate": newDressLoan.endDate.value,
        "dress": newDressLoan.dressID.value,
        "loaner": newDressLoan.loaner.value,
        }
        res = requests.post(url=f'{api_server}/loan/', json=newDressLoanJSON, verify=True, headers={'Authorization': f'Bearer {self.__key}'})
        #print(res)
        self.__fetch_dressloan()
        
        print('Reserved!\n')

    def __remove_dressloan(self) -> None :
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressloanList.length())
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!\n')
            return

        oldDressLoan = self.__dressloanList.item(index - 1)

        self.__dressloanList.remove_dressloan_by_index(index - 1)

        res = requests.delete(url=f'{api_server}/loan/{oldDressLoan.uuid.value}', verify=True, headers={'Authorization': f'Bearer {self.__key}'})

        self.__fetch_dressloan()

        print('Dress Loan marked as terminated!\n')


    def __edit_dressloan_end_date(self) -> None :
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__dressloanList.length())
            return int(value)


        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!\n')
            return

        edited_dressloan = self.__dressloanList.item(index - 1)
        edited_end_date = self.__read('End Date (format yyyy-mm-dd)', EndDate)
        edited_dressloan.endDate = edited_end_date
        

        newEditedDressLoanJSON = {
        "startDate": edited_dressloan.startDate.value,
        "endDate": edited_dressloan.endDate.value,
        "dress": edited_dressloan.dressID.value,
        "loaner": edited_dressloan.loaner.value,
        }
        

        res = requests.put(url=f'{api_server}/loan/{edited_dressloan.uuid.value}', json=newEditedDressLoanJSON, verify=True, headers={'Authorization': f'Bearer {self.__key}'})
        #print(res.json())

        self.__fetch_dressloan()

        print('End date extended!\n')