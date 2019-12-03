# Big Cheef's Suprise Mechanics by MAWD™

## Roles:                                </br>
Mohidul Abedin - Project Manager, Balance </br>
William Cao - Pokemon Game </br>
Devin Lin - Rick and Morty Game </br>
Alex Olteanu - To21 game </br>

## Description
Our website is a collection of top-tier, big-brain, and purely skill based games. Use our IN-GAME currency to play Pokemon Versus, to21 (not blackjack btw) and Rick and Morty trivia. You can also redeem your winnings from the games into your paypal account or (maybe) buy MICROTRANSACTIONS. 

## API and Frontend Framework
  - [PokeApi](https://docs.google.com/document/d/1hMbL36d5qqFLfufHOqUMWwraWFudfJdekqp6urex0KU/edit)
  - [Currency Exchange](https://docs.google.com/document/d/1yTckLoGBHA-C37hhukXOc76Jh_770L7m3Moj-wMFeUU/edit)
  - [Deck of Cards](https://docs.google.com/document/d/1oCJhl-NoNNpekMLd4C4jBXhpL9xvm6ZrVIdfoqbq-Vc/edit#heading=h.cx298swl620u)
  - [Rick and Morty](https://docs.google.com/document/d/1oK0klhp__LHP9kxb3D70cbbI46i1mMnmDMI4y1XS3B4/edit)
  - [Bootstrap](https://getbootstrap.com/docs/4.3/getting-started/introduction/)

## Instructions to Run
1. Open a terminal. Run the following lines in the terminal to clone the repository and change directory into it.
    ```bash
    git clone https://github.com/Mabedin00/MAWD.git && cd MAWD
    ```
2. Install python virtualenv if it has not been done so already.  
    ```bash
    # For macOS and Linux
    python3 -m pip install virtualenv
3. Create a virtual environment by running:
    ```bash   
    python3 -m venv venv
    # If this command does not work, try
    python -m venv venv
    ```
4. Activate the virtual environment
    ```bash
    # If you are using Bash:
    . venv/bin/activate
    # If you are using zsh:
    source venv/bin/activate
    ```
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    # If this command does not work, try running:
    pip3 install -r requirements.txt
    ```
6. Initialize the database by running the following:
    ```bash
    python3 data/database_builder.py
    python3 initDatabase.py
    # If these commands do not work, try running
    python data/database_builder.py
    python initDatabase.py
    ```
7. Start the web server by running:
    ```bash
    python3 app.py
    ```
8. Open a web browser and type the following into the address "127.0.0.1:5000"
