import tkinter as tk
import math

board = [' ' for _ in range(9)]

winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),(0, 3, 6), (1, 4, 7), (2, 5, 8),(0, 4, 8), (2, 4, 6)]

window = tk.Tk()
window.title("Tic-Tac-Toe")

def check_winner(player):
    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_full(board):
    return ' ' not in board

def minimax(board, depth, is_maximizing):
    if check_winner('O'):
        return 1
    elif check_winner('X'):
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                eval = minimax(board, depth + 1, False)
                board[i] = ' '
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(board, depth + 1, True)
                board[i] = ' '
                min_eval = min(min_eval, eval)
        return min_eval

def best_move(board):
    best_eval = -math.inf
    best_move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            eval = minimax(board, 0, False)
            board[i] = ' '
            if eval > best_eval:
                best_eval = eval
                best_move = i
    return best_move

game_over = False

def end_game(message):
    global game_over
    game_over = True
    result_label.config(text=message)
    for b in buttons:
        b.config(state='disabled')  # no more moves once the game is decided

def player_move(button, index):
    if game_over:
        return
    if board[index] == ' ':
        button.config(text='X', state='disabled')
        board[index] = 'X'
        if check_winner('X'):
            end_game("You win!")
        elif is_full(board):
            end_game("It's a draw!")
        else:
            ai_move()

def ai_move():
    ai_index = best_move(board)
    button = buttons[ai_index]
    button.config(text='O', state='disabled')
    board[ai_index] = 'O'
    if check_winner('O'):
        end_game("AI wins!")
    elif is_full(board):
        end_game("It's a draw!")

buttons = []
for i in range(9):
    row = i // 3
    col = i % 3
    button = tk.Button(window, text=' ', width=10, height=3,
                      command=lambda idx=i: player_move(buttons[idx], idx))
    button.grid(row=row, column=col)
    buttons.append(button)

result_label = tk.Label(window, text='', font=("Ubuntu", 16))
result_label.grid(row=3, column=0, columnspan=3)

window.mainloop()
