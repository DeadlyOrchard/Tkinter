from Pokemon import Pokemon, EggGroupBtn
import tkinter as tk
import os, sys

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.state('zoomed')
        self.root.title('Pokedex Breeding')
        icon_path = os.path.join(os.path.dirname(sys.executable), 'icon.png')
        icon = tk.PhotoImage(file = icon_path)
        self.root.iconphoto(False, icon)
        
        # fonts and colors
        header = ('Courier', 24)
        bgc = '#ccc'
        fgc = '#ddd'
        
        # dynamic sizing
        self.screenwidth, self.screenheight = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        w, h = self.screenwidth, 50 # egg group label dimensions
        egg_group_fr = tk.Frame(self.root, width=w, height=h)
        egg_group_fr.grid(column=1, row=1, columnspan=2)
        color_fr = tk.Frame(egg_group_fr, bg=bgc, width=w, height=h)
        color_fr.grid(column=1, row=1, columnspan=2)
        
        w, h = self.screenwidth // 5, self.screenheight - 50 # egg groups list dimensions
        egg_list_fr = tk.Frame(self.root, width=w, height=h)
        egg_list_fr.grid(column=2, row=2)
        color_fr = tk.Frame(egg_list_fr, bg=bgc, width=w, height=h)
        color_fr.grid(column=1, row=1, rowspan=21)
        
        w, h = self.screenwidth // 5 * 4, self.screenheight - 50 # displayed pokemon dimensions
        self.pokemon_fr = tk.Frame(self.root, width=w, height=h)
        self.pokemon_fr.grid(column=1, row=2)
        color_fr = tk.Frame(self.pokemon_fr, bg=fgc, width=w, height=h)
        color_fr.grid(column=1, row=1, columnspan=5, rowspan=2)
        
        # pokedex things
        filename = os.path.join(os.path.dirname(sys.executable), 'pokedex.txt')
        pokedex_fv = open(filename, 'r')
        eggs = {'amorphous', 'bug', 'ditto', 'dragon', 'fairy', 'field', 'flying', 'grass', 'human-like', 'mineral', 'monster', 'undiscovered', 'water 1', 'water 2', 'water 3'}
        self.pokedex = {'amorphous': None, 'bug': None, 'ditto': None, 'dragon': None, 'fairy': None, 'field': None, 'flying': None, 'grass': None, 'human-like': None, 'mineral': None, 'monster': None, 'undiscovered': None, 'water 1': None, 'water 2': None, 'water 3': None}
        for line in pokedex_fv:
            fline = line.strip()
            if fline in eggs:
                egg = fline
                new = True
            elif len(fline) != 0:
                if new:
                    self.pokedex[egg] = []
                new = False
                id = fline[0:fline.find('!')]
                species = fline[fline.find('!') + 1:fline.find(':')]
                gender = fline[fline.find('-') + 1:fline.find('|')]
                ivs = {'hp': None, 'atk': None, 'def': None, 'spatk': None, 'spdef': None, 'spe': None}
                nums = fline[fline.find('|') + 1::].split()
                num = 0
                for key in ivs.keys():
                    ivs[key] = int(nums[num])
                    num += 1
                self.pokedex[egg].append(Pokemon(species, egg, gender, ivs, self, id))
        pokedex_fv.close()
        
        # label vars
        self.onscreen_egg_group = tk.StringVar()
        self.onscreen_egg_group.set('Please Select Egg Group')
        self.egg_groups = {'amorphous': tk.StringVar(), 'bug': tk.StringVar(), 'dragon': tk.StringVar(), 'fairy': tk.StringVar(), 'field': tk.StringVar(), 'flying': tk.StringVar(), 'grass': tk.StringVar(), 'human-like': tk.StringVar(), 'mineral': tk.StringVar(), 'monster': tk.StringVar(), 'water 1': tk.StringVar(), 'water 2': tk.StringVar(), 'water 3': tk.StringVar(), 'ditto': tk.StringVar(), 'undiscovered': tk.StringVar()}
        for group, list in self.pokedex.items():
            diff = 20 - len(group)
            if list == None:
                num = '0'
            else:
                num = str(len(list))
            self.egg_groups[group].set(group.title() + (diff * '.') + '(' + num + ')')
        
        # labels
        onscreen_egg_group_lb = tk.Label(egg_group_fr, textvariable=self.onscreen_egg_group, font=header, bg=bgc)
        onscreen_egg_group_lb.grid(column=1, row=1, columnspan=2)
        egg_group_btns = [tk.Label(egg_list_fr, text='Egg Groups', font=header, bg=bgc)]
        for group in self.egg_groups.keys():
            egg_group_btns.append(EggGroupBtn(egg_list_fr, self.egg_groups[group], self))
        i = 1
        for btn in egg_group_btns:
            btn.grid(column=1, row=i)
            i += 1
        self.displayed_poke = []
        self.root.mainloop()
    def view(self, egg_group):
        for pokemon in self.displayed_poke:
            pokemon.grid_remove()
        self.onscreen_egg_group.set(egg_group)
        self.displayed_poke.clear()
        if self.pokedex[egg_group.lower()] != None:
            for pokemon in self.pokedex[egg_group.lower()]:
                valid = True
                if len(self.displayed_poke) == 11:
                    valid = False
                if valid:
                    self.displayed_poke.append(pokemon)
        if len(self.displayed_poke) < 10:
            self.displayed_poke.append(tk.Button(self.pokemon_fr, text='\u2295', font=('Courier', 78), bg='#ddd', command=self.add_poke))
        col, r = 1, 1
        for pokemon in self.displayed_poke:
            pokemon.grid(column=col, row=r, sticky='nsew')
            if col >= 5:
                r += 1
                col = 1
            else:
                col += 1
        for group, list in self.pokedex.items():
            diff = 20 - len(group)
            if list == None:
                num = '0'
            else:
                num = str(len(list))
            self.egg_groups[group].set(group.title() + (diff * '.') + '(' + num + ')')
    def get_poke_size(self):
        return self.pokemon_fr.winfo_width() // 5
    def add_poke(self):
        win = tk.Toplevel(self.root)
        win.title('Add Pokemon')
        name = tk.StringVar()
        name.set('Unnamed')
        species = tk.StringVar()
        gender = tk.IntVar()
        HP = tk.StringVar()
        ATK = tk.StringVar()
        DEF = tk.StringVar()
        SPATK = tk.StringVar()
        SPDEF = tk.StringVar()
        SPE = tk.StringVar()
        errors = tk.StringVar()
        dict = {tk.Label(win, text='Name: ', font=('Courier', 18)): tk.Entry(win, textvariable=name, font=('Courier', 18)),
                  tk.Label(win, text='Species: ', font=('Courier', 18)): tk.Entry(win, textvariable=species, font=('Courier', 18)),
                  tk.Label(win, text='Gender: ', font=('Courier', 18)): [tk.Radiobutton(win, text='Male', variable=gender, value=1, font=('Courier', 18)), tk.Radiobutton(win, text='Female', variable=gender, value=2, font=('Courier', 18)), tk.Radiobutton(win, text='Genderless', variable=gender, value=3, font=('Courier', 18))],
                  tk.Label(win, text='HP: ', font=('Courier', 18)): tk.Entry(win, textvariable=HP, font=('Courier', 18)),
                  tk.Label(win, text='ATK: ', font=('Courier', 18)): tk.Entry(win, textvariable=ATK, font=('Courier', 18)),
                  tk.Label(win, text='DEF: ', font=('Courier', 18)): tk.Entry(win, textvariable=DEF, font=('Courier', 18)),
                  tk.Label(win, text='SpATK: ', font=('Courier', 18)): tk.Entry(win, textvariable=SPATK, font=('Courier', 18)),
                  tk.Label(win, text='SpDEF: ', font=('Courier', 18)): tk.Entry(win, textvariable=SPDEF, font=('Courier', 18)),
                  tk.Label(win, text='SPE: ', font=('Courier', 18)): tk.Entry(win, textvariable=SPE, font=('Courier', 18)),
                  tk.Label(win, text='Confirm', font=('Courier', 18)): tk.Button(win, fg='green', text='\u2713', font=('Courier', 18), command=lambda: self.save_poke([species.get(), name.get(), gender.get(), {'hp': int(HP.get()), 'atk': int(ATK.get()), 'def': int(DEF.get()), 'spatk': int(SPATK.get()), 'spdef': int(SPDEF.get()), 'spe': int(SPE.get())}, errors])),
                  tk.Label(win, textvariable=errors, font=('Courier', 18)): None
                  }
        i = 1
        for key, val in dict.items():
            if type(val) != list and val != None:
                key.grid(column=1, row=i)
                val.grid(column=2, row=i, columnspan=3, sticky='ew')
                i += 1
            elif type(val) == list:
                key.grid(column=1, row=3)
                j = 2
                for item in val:
                    item.grid(column=j, row=3)
                    j += 1
                i += 1
            elif val == None:
                key.grid(column=1, row=11, columnspan=4)
    def save_poke(self, info): # info is list type [species, name, gender, ivs_dict, error_msg]
        filename = os.path.join(os.path.dirname(sys.executable), 'pokemon_info.txt')
        pokemon_info_fv = open(filename, 'r')
        valid_species = False
        found_current_egg_group = False
        eggs = {'amorphous', 'bug', 'ditto', 'dragon', 'fairy', 'field', 'flying', 'grass', 'human-like', 'mineral', 'monster', 'undiscovered', 'water 1', 'water 2', 'water 3'}
        egg_groups = []
        for line in pokemon_info_fv:
            fline = line.strip()
            if fline == self.onscreen_egg_group.get().lower():
                found_current_egg_group = True
            elif found_current_egg_group and fline == info[0].lower():
                valid_species = True
            if fline in eggs:
                current_egg = fline
            elif fline == info[0].lower():
                egg_groups.append(current_egg)
        if valid_species:
            if self.pokedex[self.onscreen_egg_group.get().lower()] == None:
                self.pokedex[self.onscreen_egg_group.get().lower()] = []
            total = 0
            for group in self.pokedex.keys():
                if self.pokedex[group] != None:
                    total += len(self.pokedex[group])
            if info[2] == 1:
                gender = 'male'
            elif info[2] == 2:
                gender = 'female'
            elif info[2] == 3:
                gender = 'genderless'
            for group in egg_groups:
                pokemon = Pokemon(info[0], group, gender, info[3], self, total)
                if self.pokedex[group] == None:
                    self.pokedex[group] = []
                self.pokedex[group].append(pokemon)
            self.view(self.onscreen_egg_group.get())
            filename = os.path.join(os.path.dirname(sys.executable), 'pokedex.txt')
            pokedex_fv = open(filename, 'w')
            string = ''
            for key, val in self.pokedex.items():
                string += key + '\n'
                if val != None:
                    for pokemon in val:
                        string += str(pokemon.get_id()) + '!' + pokemon.get_species() + ':' + pokemon.get_name() + '-' + pokemon.get_gender() + '|' + str(pokemon.get_hp()) + ' ' + str(pokemon.get_atk()) + ' ' + str(pokemon.get_def()) + ' ' + str(pokemon.get_spatk()) + ' ' + str(pokemon.get_spdef()) + ' ' + str(pokemon.get_spe()) + '\n'
                string += '\n'
            pokedex_fv.write(string)
            pokedex_fv.close()
        else:
            info[4].set(f'{info[0]} does not belong to the {self.onscreen_egg_group.get()} egg group!')
    def delete_poke(self, id):
        for group, list in self.pokedex.items():
            if list != None:
                for pokemon in list:
                    if pokemon.get_id() == id:
                        self.pokedex[group].remove(pokemon)
                        break
        filename = os.path.join(os.path.dirname(sys.executable), 'pokedex.txt')
        pokedex_fv = open(filename, 'w')
        string = ''
        for key, val in self.pokedex.items():
            string += key + '\n'
            if val != None:
                for pokemon in val:
                    string += pokemon.get_species() + ':' + pokemon.get_name() + '-' + pokemon.get_gender() + '|' + str(pokemon.get_hp()) + ' ' + str(pokemon.get_atk()) + ' ' + str(pokemon.get_def()) + ' ' + str(pokemon.get_spatk()) + ' ' + str(pokemon.get_spdef()) + ' ' + str(pokemon.get_spe()) + '\n'
            string += '\n'
        pokedex_fv.write(string)
        pokedex_fv.close()
        self.view(self.onscreen_egg_group.get())
        
GUI()
