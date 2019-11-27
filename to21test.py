import os, random
from flask import Flask, session, render_template, redirect, url_for, request, flash
from data import database_query
from pokemon_game.routes import pokemon_game
import to21help as help
import random

help.createDB()
help.initializeDB()
command = "SELECT * FROM gameinfo;"
print(help.runsqlcommand(command))

print(help.getdeckid())
print(help.getUserAmt())
print(help.getUserNumCards())
print(help.getDealerAmt())
print(help.getDealerNumCards())

print(2)

command = "UPDATE gameinfo SET userTotal=20, userNumCards=5, dealerTotal=15, dealerNumCards=3;"
help.runsqlcommand(command)

print(help.getdeckid())
print(help.getUserAmt())
print(help.getUserNumCards())
print(help.getDealerAmt())
print(help.getDealerNumCards())
