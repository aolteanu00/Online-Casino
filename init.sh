#!/bin/bash

GREEN='\033[0;32m'
RED='\e[31m'
NC='\033[0m' # No color

echo -e "${GREEN}Creating python virtual environment${NC}"
python3 -m venv venv || echo "Please refer to the Step 2 in the README.md to install virtual environment"

echo -e "${GREEN}Creating python virtual environment${NC}"
source venv/bin/activate || . venv/bin/activate

echo -e "${GREEN}Install required packages to the environment${NC}"
pip3 install -r requirements.txt

echo -e "${GREEN}Creating database${NC}"
python data/database_builder.py

echo -e "${GREEN}Seeding database${NC}"
echo -e "${RED}This will take a long time depending on your internet connection and API server load${NC}"
echo -e "Filling in pokemon data"
python data/pokemonAPI.py
echo -e "Filling in rick and morty data"
python data/rick_and_morty.py
echo -e "Filling in currency ratios data"
python data/currencyExchangeAPI.py
