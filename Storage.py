import json
import pokebase


class Storage:
    cred = {}
    pokemon = {}

    @staticmethod
    def load_credentials():
        try:
            with open("users.txt", "r") as f:
                Storage.cred = json.load(f)
        except FileNotFoundError:
            with open("users.txt", "w") as f:
                json.dump(Storage.cred, f)

    @staticmethod
    def save_credentials():
        with open("users.txt", "w") as f:
            json.dump(Storage.cred, f)

    @staticmethod
    def load_pokemon():
        try:
            with open("pokemon.txt", "r") as f:
                Storage.pokemon = json.load(f)
        except FileNotFoundError:
            with open("pokemon.txt", "w") as f:
                json.dump(Storage.pokemon, f)

    @staticmethod
    def save_pokemon(user_name, pokemon_name):
        pokemon_name = str(pokebase.pokemon(int(pokemon_name)))
        if user_name not in Storage.pokemon:
            Storage.pokemon[user_name] = {}
        if pokemon_name not in Storage.pokemon[user_name]:
            Storage.pokemon[user_name][pokemon_name] = 0
        Storage.pokemon[user_name][pokemon_name] += 1

        with open("pokemon.txt", "w") as f:
            json.dump(Storage.pokemon, f)


