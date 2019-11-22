#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No color

echo -e "${GREEN}Creating database${NC}"
python3 data/database_builder.py

echo -e "${GREEN}Seeding database${NC}"