import unittest
from pokemon_game import type_logic, pokemon_game


class TestPokemonTypes(unittest.TestCase):
    def test_damage_relations(self):
        self.assertEqual(type_logic.damage_to("poison", "rock"), .5)
        self.assertEqual(type_logic.damage_to("flying", "electric"), .5)
        self.assertEqual(type_logic.damage_to("ghost", "ghost"), 2)
        self.assertEqual(type_logic.damage_to("ghost", "normal"), 0)
        self.assertEqual(type_logic.damage_to("grass", "steel"), .5)
        self.assertEqual(type_logic.damage_to("water", "psychic"), 1)
        self.assertEqual(type_logic.damage_to("psychic", "dark"), 0)
        self.assertEqual(type_logic.damage_to("normal", "steel"), 0.5)


class TestPokemonBattle(unittest.TestCase):
    def test(self):
        self.assertEqual(pokemon_game.user_balance_lost(pokemon_game.get_pokemon("raticate"),
                                                                pokemon_game.get_pokemon("kabutops"), 10), -5)
        self.assertEqual(pokemon_game.user_balance_lost(pokemon_game.get_pokemon("kadabra"),
                                                                pokemon_game.get_pokemon("ekans"), 10), 10)
        self.assertEqual(pokemon_game.user_balance_lost(pokemon_game.get_pokemon("poliwhirl"),
                                                                pokemon_game.get_pokemon("tangela"), 10), -10)
        self.assertEqual(pokemon_game.user_balance_lost(pokemon_game.get_pokemon("skiploom"),
                                                                pokemon_game.get_pokemon("dugtrio"), 10), 10)

    def test_type(self):
        self.assertEqual(pokemon_game.get_pokemon("charmander").first_type, "fire")
        self.assertEqual(pokemon_game.get_pokemon("charmander").second_type, "fire")
        self.assertEqual(pokemon_game.get_pokemon("venusaur").first_type, "grass")
        self.assertEqual(pokemon_game.get_pokemon("venusaur").second_type, "poison")
        self.assertEqual(pokemon_game.get_pokemon("teddiursa").first_type, "normal")
        self.assertEqual(pokemon_game.get_pokemon("teddiursa").second_type, "normal")
        self.assertEqual(pokemon_game.get_pokemon("steelix").first_type, "steel")
        self.assertEqual(pokemon_game.get_pokemon("steelix").second_type, "ground")


if __name__ == '__main__':
    unittest.main()
