import streamlit as st
import random
import time
import numpy as np

# Impostazioni del gioco
width = 600  # larghezza della finestra
height = 400  # altezza della finestra
pizza_pos = [width // 2, height - 50]  # posizione della pizza
pizza_speed = 10  # velocità di movimento della pizza
life = 5  # vita iniziale

# Lista degli ingredienti
ingredients = ['peperone', 'olive', 'pomodoro', 'birra']

# Funzione per aggiornare la posizione
def move_pizza(pizza_pos, direction):
    if direction == "left" and pizza_pos[0] > 0:
        pizza_pos[0] -= pizza_speed
    elif direction == "right" and pizza_pos[0] < width - 100:
        pizza_pos[0] += pizza_speed
    return pizza_pos

# Funzione per generare ingredienti
def generate_ingredient():
    ingredient = random.choice(ingredients)
    x_pos = random.randint(0, width - 50)
    y_pos = 0
    speed = random.randint(3, 7)
    return {"ingredient": ingredient, "x_pos": x_pos, "y_pos": y_pos, "speed": speed}

# Funzione di disegno per la pizza
def draw_pizza(pizza_pos):
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Pizza_slice.svg/512px-Pizza_slice.svg.png", width=100, use_column_width=False)
    st.markdown(f"Pizza is at position: {pizza_pos}")

# Funzione per la logica del gioco
def game_loop():
    global pizza_pos, life
    ingredients_falling = []
    score = 0
    while life > 0:
        # Generare nuovi ingredienti
        if random.random() < 0.1:
            ingredients_falling.append(generate_ingredient())

        # Muovere i nuovi ingredienti
        for ingredient in ingredients_falling:
            ingredient["y_pos"] += ingredient["speed"]

        # Controlla se gli ingredienti hanno colpito la pizza
        for ingredient in ingredients_falling:
            if ingredient["y_pos"] > height - 50 and abs(ingredient["x_pos"] - pizza_pos[0]) < 100:
                if ingredient["ingredient"] == "birra":
                    life -= 1  # La birra danneggia la pizza
                    ingredients_falling.remove(ingredient)
                score += 1

        # Rimuovere ingredienti che escono dallo schermo
        ingredients_falling = [i for i in ingredients_falling if i["y_pos"] < height]

        # Disegnare la scena
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Pizza_slice.svg/512px-Pizza_slice.svg.png", width=100, use_column_width=False)
        for ingredient in ingredients_falling:
            st.markdown(f"Ingredient {ingredient['ingredient']} at ({ingredient['x_pos']}, {ingredient['y_pos']})")

        st.markdown(f"Life: {life}  Score: {score}")
        time.sleep(0.2)

# Funzione per il movimento
def move_game(direction):
    global pizza_pos
    pizza_pos = move_pizza(pizza_pos, direction)
    return pizza_pos

# Funzione principale
def run_game():
    st.title("Battaglia di Pizza vs. Birra")
    st.subheader("Sopravvivi il più a lungo possibile evitando gli ingredienti pazzi!")

    # Spazio per i comandi
    move_left = st.button("Move Left")
    move_right = st.button("Move Right")

    if move_left:
        pizza_pos = move_game("left")
    if move_right:
        pizza_pos = move_game("right")
    
    # Avvia il gioco
    game_loop()

if __name__ == "__main__":
    run_game()
