from data import database_query as query
from collections import namedtuple

Type_Info = namedtuple("type_info", ["name", "double_damage_to", "half_damage_to", "no_damage_to"])
# Key: Name of type
# Value: Type_Info
types_info = dict()
for info in query.pokemon_type_info():
    type_name = info[0]
    types_info[type_name] = Type_Info(*info)


def damage_to(attacker: str, defender: str):
    type_info = types_info[attacker]
    if defender in type_info.double_damage_to:
        return 2
    elif defender in type_info.half_damage_to:
        return .5
    elif defender in type_info.no_damage_to:
        return 0
    else:
        return 1