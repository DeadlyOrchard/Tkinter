from tkinter import Button, Label, Frame

class Pokemon:
    def __init__(self, species, egg_group, gender, ivs, gui, id, name='Unnamed'):
        self.__id = id
        self.set_species(species)
        self.set_egg_group(egg_group)
        self.set_gender(gender)
        self.set_ivs(ivs)
        self.set_egg_group(egg_group)
        self.set_name(name)
        self.__gui = gui
        self.__root = Frame(self.__gui.pokemon_fr, bg='#ddd')
        self.setup()
    def setup(self):
        self.__labels = [
            Label(self.__root, text='', bg='#ddd'),
            Label(self.__root, text=f'{self.get_name()}', font=('Courier', 18), bg='#ddd'),
            Label(self.__root, text=f'{self.get_species()} - {self.get_gender()}', font=('Courier', 18), bg='#ddd'),
            Label(self.__root, text=f'HP: {self.get_hp()}', font=('Courier', 18), bg='#ddd'),
            Label(self.__root, text=f'ATK: {self.get_atk()}', font=('Courier', 18), bg='#ddd'),
            Label(self.__root, text=f'DEF: {self.get_def()}', font=('Courier', 18), bg='#ddd'),
            Label(self.__root, text=f'SpATK: {self.get_spatk()}', font=('Courier', 18), bg='#ddd'),
            Label(self.__root, text=f'SpDEF: {self.get_spdef()}', font=('Courier', 18), bg='#ddd'),
            Label(self.__root, text=f'SPE: {self.get_spe()}', font=('Courier', 18), bg='#ddd'),
            Label(self.__root, text=f'Perfection: {self.get_perf()}', font=('Courier', 18), bg='#ddd')
            ]
        btn = Button(self.__root, text='\u2715', command=self.delete)
        btn.grid(column=2, row=1)
        i = 1
        for label in self.__labels:
            label.grid(column=1, row=i)
            i += 1
    def set_species(self, species):
        self.__species = species.title()
    def set_name(self, name):
        self.__name = name
    def set_egg_group(self, group):
        groups = {'amorphous', 'bug', 'ditto', 'dragon', 'fairy', 'field', 'flying', 'grass', 'human-like', 'mineral', 'monster', 'undiscovered', 'water 1', 'water 2', 'water 3'}
        if group in groups:
            self.__egg_group = group
        else:
            raise Exception(f'Egg group assignment error\nGroup: {group}')
    def set_gender(self, gender):
        if gender.lower() == 'male' or gender.lower() == 'female' or gender.lower() == 'genderless':
            self.__gender = gender.title()
        else:
            raise Exception(f'Gender assignment error\nGender: {gender}')
    def set_ivs(self, ivs):
        formatted = True
        for iv in ivs.values():
            if type(iv) is not int and not iv.isdigit():
                formatted = False
        if formatted and min(ivs.values()) >= 0 and max(ivs.values()) <= 31:
            self.__hp = ivs['hp']
            self.__atk = ivs['atk']
            self.__def = ivs['def']
            self.__spatk = ivs['spatk']
            self.__spdef = ivs['spdef']
            self.__spe = ivs['spe']
            self.__ivs = {'hp': self.get_hp(), 'atk': self.get_atk(), 'def': self.get_def(), 'spatk': self.get_spatk(), 'spdef': self.get_spdef(), 'spe': self.get_spe()}
        else:
            raise Exception(f'IVs assignment error\nIVs: {ivs}')
    def set_master(self, master):
        self.__master = master
    def get_master(self):
        return self.__master
    def get_name(self):
        return self.__name
    def get_species(self):
        return self.__species
    def get_egg_group(self):
        return self.__egg_group
    def get_gender(self):
        return self.__gender
    def get_ivs(self):
        return self.__ivs
    def get_hp(self):
        return self.__hp
    def get_atk(self):
        return self.__atk
    def get_def(self):
        return self.__def
    def get_spatk(self):
        return self.__spatk
    def get_spdef(self):
        return self.__spdef
    def get_spe(self):
        return self.__spe
    def get_perf(self):
        total = 0
        for val in self.get_ivs().values():
            total += val
        return f'{round((total / 186) * 100)}%'
    def get_id(self):
        return self.__id
    def grid(self, column=1, row=1, sticky=None):
        self.__root.grid(column=column, row=row)
    def grid_remove(self):
        self.__root.grid_remove()
    def delete(self):
        self.__gui.delete_poke(self.get_id())
    def __str__(self):
        string = f'{self.get_species()}: {self.get_name()} - {self.get_gender()}'
        for key, val in self.get_ivs().items():
            string += f'\n.....{key}: {val}'
        return string

class EggGroupBtn:
    def __init__(self, master, text_var, gui):
        self.gui = gui
        self.btn = Button(master, textvariable=text_var, font=('Courier', 18), bg='#ccc', command=self.selected)
        string = text_var.get()
        group = ''
        for char in string:
            if char == '.':
                break
            group += char
        self.group = group
        self.btn.bind('<Enter>', self.enter)
        self.btn.bind('<Leave>', self.leave)
    def enter(self, e):
        self.btn['background'] = '#ddd'
    def leave(self, e):
        self.btn['background'] = '#ccc'
    def get_group(self):
        return self.group
    def selected(self):
        self.gui.view(self.get_group())
    def grid(self, column=1, row=1):
        self.btn.grid(column=column, row=row, sticky='nsew')
