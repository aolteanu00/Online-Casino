import unittest
from pokemon_game import type_logic


class TestPokemonTypes(unittest.TestCase):
    def test_damage_relations(self):
        self.assertEqual(type_logic.damage_to("poison", "rock"), .5)
        self.assertEqual(type_logic.damage_to("flying", "electric"), .5)
        self.assertEqual(type_logic.damage_to("ghost", "ghost"), 2)
        self.assertEqual(type_logic.damage_to("ghost", "normal"), 0)
        self.assertEqual(type_logic.damage_to("grass", "steel"), .5)
        self.assertEqual(type_logic.damage_to("water", "psychic"), 1)
        self.assertEqual(type_logic.damage_to("psychic", "dark"), 0)


if __name__ == '__main__':
    unittest.main()