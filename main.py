import time
import json
import os
import requests

class pokemon:
    def __init__(self, number, energy):
        self.number = number
        self.energy = 50
        self.hp = hp_from_id(number)
        self.attack = attack_from_id(number)
        self.defense = defense_from_id(number)
        self.special_attack = special_attack_from_id(number)
        self.special_defense = special_defense_from_id(number)
        self.speed = speed_from_id(number)

class player:
    def __init__(self, name):
        self.beans = 0
        self.name = name
        self.pokemon = []

        self.last_harvest = None

    def harvest(self):
        if self.last_harvest == None:
            harvested_beans = 40
        else:
            seconds_since_last_harvest = time.time() - self.last_harvest
            harvested_beans = int(seconds_since_last_harvest / 180)

        if harvested_beans > 80:
            harvested_beans = 80

        if harvested_beans > 0:
            self.beans += harvested_beans
            self.last_harvest = time.time()

            self.save_to_file()

            print(f"You've harvested {harvested_beans} beans!")
        else:
            print("Oops, the tree hasn't produced any beans yet! Wait a little longer!")

    def print_info(self):
        print(f"You currently have {self.beans} beans!\n \n")

    def print_salutations(self):
        return(f"Hey, {self.name}! What would you like to do? Check your beans, harvest or (add more later)?\n")

    def save_to_file(self):
        # make dict of attributes
        player_data = {
            "name": self.name,
            "beans": self.beans,
            "last_harvest": self.last_harvest
        }

        file_name = f"{self.name}.json"
        file = open(file_name, "w")  # open file
        json.dump(player_data, file)  # write player data to file
        file.close()  # close file

    def load_from_file(self):
        file_name = f"{self.name}.json"
        if os.path.exists(file_name):  #check if player file exists
            player_data = json.load(open(file_name))  # open json file

            # set attributes
            self.name = player_data["name"]
            self.beans = player_data["beans"]
            self.last_harvest = player_data["last_harvest"]
        else:
            print("no player file found")

r = requests.get("https://pokeapi.co/api/v2/pokemon/6")
data = r.json()
stats = {x["stat"]["name"]: x[base_stat]for x in data["stats"]}

p1 = player(input("Hey!Whats your name?\n"))
p1.load_from_file()

x = 1
while x == 1:
    player_choice = input(p1.print_salutations())
    if player_choice == "beans":
        p1.print_info()
        input("Press Enter to go back to the main menu.")
    elif player_choice == "harvest":
        p1.harvest()
        input("Press Enter to go back to the main menu.")

