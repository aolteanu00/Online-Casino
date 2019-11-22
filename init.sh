#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No color

echo -e "${GREEN}Creating database${NC}"
python3 data/database_builder.py

echo -e "${GREEN}Seeding database${NC}"
echo -e "Filling in pokemon data"
python3 data/pokemonAPI.py

echo -e "Filling in rick and morty data"
python3 data/rick_and_morty.py
