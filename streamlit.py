import streamlit as st
import numpy as np

# Константы
GRID_SIZE = 5  # Размер сетки
PLAYER_SYMBOL = "🟢"  # Символ игрока

# Инициализация состояния
if 'player_position' not in st.session_state:
    st.session_state.player_position = [0, 0]  # Начальная позиция игрока

# Функция для отображения клеточного поля
def display_grid():
    grid = np.full((GRID_SIZE, GRID_SIZE), '⬜️')  # Создаем пустую сетку
    x, y = st.session_state.player_position
    grid[x, y] = PLAYER_SYMBOL  # Устанавливаем позицию игрока
    st.write(grid)

# Функции для перемещения игрока
def move_up():
    if st.session_state.player_position[0] > 0:
        st.session_state.player_position[0] -= 1

def move_down():
    if st.session_state.player_position[0] < GRID_SIZE - 1:
        st.session_state.player_position[0] += 1

def move_left():
    if st.session_state.player_position[1] > 0:
        st.session_state.player_position[1] -= 1

def move_right():
    if st.session_state.player_position[1] < GRID_SIZE - 1:
        st.session_state.player_position[1] += 1

# Отображение кнопок для управления
st.title("Клеточное поле")
display_grid()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("↑"):
        move_up()
with col2:
    if st.button("←"):
        move_left()
with col3:
    if st.button("→"):
        move_right()
with col1:
    if st.button("↓"):
        move_down()

# Обновление поля после нажатия кнопок
display_grid()
