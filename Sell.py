from __future__ import print_function
import os, sys
from tkinter import Tk, Label, Entry, Button, StringVar, CENTER
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

class Gui:
    def __init__(self):
        print('Getting Settings...')
        self.settings = {}
        self.settings['staff members'] = set()
        staff_members = self.get_data('Settings!B3:B')
        for row in staff_members:
            for column in row:
                self.settings['staff members'].add(column)
        
        self.settings['products'] = set()
        products = self.get_data('Settings!D2:D')
        for row in products:
            for column in row:
                self.settings['products'].add(column)
        print('Getting sales info...')
        self.sale_row = 3
        sales = self.get_data('Inventory!A3:F')
        self.sales_by_product = {}
        if type(sales) is list:
            self.sale_row = len(sales) + 3 # so that new sales can be written to the spreadsheet more easily
            # create dicts of inventory sales based on product and staff
            for row in sales:
                staff = row[0]
                product = row[4]
                amount = int(row[5])
                if product not in self.sales_by_product.keys():
                    self.sales_by_product[product] = {}
                if staff not in self.sales_by_product[product].keys():
                    self.sales_by_product[product][staff] = amount
                else:
                    self.sales_by_product[product][staff] += amount
        else:
            self.sale_row = 3
        
        # create dict of inventory purchases based on product so that it's easier to calculate live inventory
        purchases = self.get_data('Inventory!G3:I')
        self.purchases = {}
        if type(purchases) is list:
            for row in purchases:
                product = row[1]
                amount = int(row[2])
                if product not in self.purchases.keys():
                    self.purchases[product] = amount
                else:
                    self.purchases[product] += amount
        # calculate live inventory dict with products as keys and amounts as values
        total_sales = {}
        for product, staff_members in self.sales_by_product.items():
            current_total = 0
            for staff, amount in staff_members.items():
                current_total += amount
            total_sales[product] = current_total
        self.live_inventory = {}
        for product, amount in self.purchases.items():
            if product in total_sales.keys():
                self.live_inventory[product] = int(amount) - int(total_sales[product])
            else:
                self.live_inventory[product] = int(amount)
        print('Updating spreadsheets...')
        self.update_spreadsheets()
        print('Done!')
        self.root = Tk()
        self.root.title('Sell | MedEsthetics')
        self.staff = StringVar()
        self.client = StringVar()
        self.product1 = StringVar()
        self.amount1 = StringVar()
        self.product2 = StringVar()
        self.amount2 = StringVar()
        self.warning = StringVar()
        widgets = {Label(self.root, text='Staff Member', font=('Courier', 18)): Entry(self.root, textvariable=self.staff, font=('Courier', 18), justify=CENTER),
                   Label(self.root, text='Client', font=('Courier', 18)): Entry(self.root, textvariable=self.client, font=('Courier', 18), justify=CENTER),
                   Label(self.root, text='Product', font=('Courier', 18)): [Entry(self.root, textvariable=self.product1, font=('Courier', 18), justify=CENTER), Entry(self.root, textvariable=self.product2, font=('Courier', 18), justify=CENTER)],
                   Label(self.root, text='Amount', font=('Courier', 18)): [Entry(self.root, textvariable=self.amount1, font=('Courier', 18), justify=CENTER), Entry(self.root, textvariable=self.amount2, font=('Courier', 18), justify=CENTER)]}
        col, r = 1, 1
        for key, item in widgets.items():
            key.grid(column=col, row=r)
            if type(item) is list:
                for thing in item:
                    r += 1
                    thing.grid(column=col, row=r)
            else:
                r += 1
                item.grid(column=col, row=r)
            r = 1
            col += 1
        btn = Button(self.root, text='Sell', font=('Courier', 18), command=self.sell)
        btn.grid(column=2, row=4, sticky='nsew', columnspan=2)
        warning = Label(self.root, textvariable=self.warning, font=('Courier', 12))
        warning.grid(column=1, row=5, columnspan=4)
        self.root.mainloop()
    def sell(self):
        # this if statement is too long, but it makes sure that the staff member id, product, and amount are valid
        if self.staff.get().lower() in self.settings['staff members'] and self.product1.get().lower() in self.settings['products'] and self.product2.get().lower() in self.settings['products'] and self.product1.get().lower() in self.live_inventory.keys() and self.product2.get().lower() in self.live_inventory.keys() and self.live_inventory[self.product1.get().lower()] > 0 and self.live_inventory[self.product2.get().lower()] > 0 and self.amount1.get().isdigit() and self.amount2.get().isdigit():
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            if getattr(sys, 'frozen', False):
                BASEDIR = sys._MEIPASS
            else:
                BASEDIR = os.path.dirname(os.path.realpath('keys.json'))
            path = os.path.join(BASEDIR, "data", "keys.json")
            creds = service_account.Credentials.from_service_account_file(path, scopes=SCOPES)
            SPREADSHEET_ID = '1GPxrEsZVkDGwSf1sV9h92ivj3IzmVp9MajJJI4w56RU'

            service = build('sheets', 'v4', credentials=creds, static_discovery=False)
            sheet = service.spreadsheets()
            
            user = datetime.now()
            date = str(user.date())
            time = str(user.time())
            sales = {
                'majorDimension': 'ROWS',
                'values': [
                    [self.staff.get(), self.client.get().title(), date, time, self.product1.get().lower(), self.amount1.get()],
                    [self.staff.get(), self.client.get().title(), date, time, self.product2.get().lower(), self.amount2.get()]]
             }
            sheet.values().update(spreadsheetId=SPREADSHEET_ID, valueInputOption='USER_ENTERED', range=f'Inventory!a{self.sale_row}:f{self.sale_row + 1}', body=sales).execute()
            self.sale_row += 2
            
            # update sales dict
            if self.product1.get().lower() not in self.sales_by_product.keys():
                self.sales_by_product[self.product1.get().lower()] = {}
            if self.staff.get() not in self.sales_by_product[self.product1.get().lower()].keys():
                self.sales_by_product[self.product1.get().lower()][self.staff.get()] = int(self.amount1.get())
            else:
                self.sales_by_product[self.product1.get().lower()][self.staff.get()] += int(self.amount1.get())
            if self.product2.get().lower() not in self.sales_by_product.keys():
                self.sales_by_product[self.product2.get().lower()] = {}
            if self.staff.get() not in self.sales_by_product[self.product2.get().lower()].keys():
                self.sales_by_product[self.product2.get().lower()][self.staff.get()] = int(self.amount2.get())
            else:
                self.sales_by_product[self.product2.get().lower()][self.staff.get()] += int(self.amount2.get())
            self.live_inventory[self.product1.get().lower()] -= int(self.amount1.get())
            self.live_inventory[self.product2.get().lower()] -= int(self.amount2.get())
            self.update_spreadsheets()
            self.warn("Success!")
        else:
            self.warn("We either don't recognize you, we don't sell that product, or we don't have that product in inventory.")
    def warn(self, msg):
        self.warning.set(msg)
    def get_data(self, range):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        if getattr(sys, 'frozen', False):
            BASEDIR = sys._MEIPASS
        else:
            BASEDIR = os.path.dirname(os.path.realpath('keys.json'))
        path = os.path.join(BASEDIR, "data", "keys.json")
        creds = service_account.Credentials.from_service_account_file(path, scopes=SCOPES)
        SPREADSHEET_ID = '1GPxrEsZVkDGwSf1sV9h92ivj3IzmVp9MajJJI4w56RU'
        service = build('sheets', 'v4', credentials=creds, static_discovery=False)
        sheet = service.spreadsheets()
        response = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range).execute()
        if 'values' in response.keys():
            return response['values']
        else:
            return response
    def update_spreadsheets(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        if getattr(sys, 'frozen', False):
            BASEDIR = sys._MEIPASS
        else:
            BASEDIR = os.path.dirname(os.path.realpath('keys.json'))
        path = os.path.join(BASEDIR, "data", "keys.json")
        creds = service_account.Credentials.from_service_account_file(path, scopes=SCOPES)
        SPREADSHEET_ID = '1GPxrEsZVkDGwSf1sV9h92ivj3IzmVp9MajJJI4w56RU'
        service = build('sheets', 'v4', credentials=creds, static_discovery=False)
        sheet = service.spreadsheets()
        
        if len(self.sales_by_product.keys()) > 0:
            # create tables from dicts to update spreadsheets
            sales_by_product_table = []
            for product, staff_members in self.sales_by_product.items():
                sales_by_product_table.append([product])
                total = 0
                for staff, amount in staff_members.items():
                    sales_by_product_table.append([staff, amount])
                    total += amount
                sales_by_product_table.append(['', total])
                sales_by_product_table.append([])
            write_sales_by_product = {'majorDimension': 'ROWS', 'values': sales_by_product_table}
            sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range='Product Sales!a1:b').execute()
            sheet.values().update(spreadsheetId=SPREADSHEET_ID, valueInputOption='USER_ENTERED', range=f'Product Sales!a1:b{len(sales_by_product_table)}', body=write_sales_by_product).execute()
        live_inventory_table = []
        for product, amount in self.live_inventory.items():
            live_inventory_table.append([product, amount])
        write_live_inventory = {'majorDimension': 'ROWS', 'values': live_inventory_table}
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, valueInputOption='USER_ENTERED', range=f'Inventory!j3:k{len(live_inventory_table) + 3}', body=write_live_inventory).execute()
Gui()