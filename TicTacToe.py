import tkinter as tk
from tkinter import messagebox
import math
import winsound 

root = tk.Tk()
root.title("Ultimate Tic-Tac-Toe")
root.geometry("420x600")
root.configure(bg="#141426")

current_player = "X"
buttons = []
mode = None
game_over = False
scores = {"X": 0, "O": 0}


# SOUND EFFECTS
def click_sound():
    try:
        winsound.Beep(1000, 100)
    except:
        pass


# AI

def check_winner_board(board, player):
    wins = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    for combo in wins:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False


def minimax(board, depth, is_maximizing):
    if check_winner_board(board, "O"):
        return 1
    if check_winner_board(board, "X"):
        return -1
    if "" not in board:
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth+1, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth+1, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score


def best_move():
    board = [buttons[i]["text"] for i in range(9)]
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move


# LOGIC

def check_winner():
    global game_over

    wins = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]

    for combo in wins:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            for i in combo:
                buttons[i].config(bg="#00ff88")
            winner = buttons[combo[0]]["text"]
            scores[winner] += 1
            update_score()
            messagebox.showinfo("Winner", f"🏆 Player {winner} Wins!")
            game_over = True
            return

    if all(button["text"] != "" for button in buttons):
        messagebox.showinfo("Draw", "It's a Draw!")
        game_over = True


def button_click(index):
    global current_player

    if buttons[index]["text"] == "" and not game_over:
        click_sound()

        buttons[index]["text"] = current_player
        buttons[index].config(
            fg="#ff4d6d" if current_player == "X" else "#4cc9f0"
        )

        check_winner()

        if not game_over:
            toggle_player()
            if mode == "AI" and current_player == "O":
                root.after(400, ai_turn)


def ai_turn():
    move = best_move()
    if move is not None:
        button_click(move)


def toggle_player():
    global current_player
    current_player = "O" if current_player == "X" else "X"
    label.config(text=f"Turn: {current_player}")


# RESET

def reset_board():
    global current_player, game_over
    current_player = "X"
    game_over = False
    label.config(text=f"Turn: {current_player}")

    for button in buttons:
        button.config(text="", bg="#1f1f3d")


def reset_scores():
    global scores
    scores = {"X": 0, "O": 0}
    update_score()


def update_score():
    score_label.config(text=f"Score  X: {scores['X']}   O: {scores['O']}")


# HUMAN OR AI MODE

def start_human():
    global mode
    mode = "HUMAN"
    start_frame.pack_forget()
    game_frame.pack()


def start_ai():
    global mode
    mode = "AI"
    start_frame.pack_forget()
    game_frame.pack()


# USER INTERFACE

start_frame = tk.Frame(root, bg="#141426")
start_frame.pack()

tk.Label(start_frame, text="ULTIMATE TIC-TAC-TOE",
         font=("Arial", 22, "bold"),
         fg="white", bg="#141426").pack(pady=40)

tk.Button(start_frame, text="Human vs Human",
          font=("Arial", 14), bg="#7209b7", fg="white",
          width=20, command=start_human).pack(pady=10)

tk.Button(start_frame, text="Human vs AI (Unbeatable)",
          font=("Arial", 14), bg="#3a0ca3", fg="white",
          width=20, command=start_ai).pack(pady=10)


game_frame = tk.Frame(root, bg="#141426")

for i in range(9):
    btn = tk.Button(game_frame, text="", font=("Arial", 28, "bold"),
                    width=5, height=2,
                    bg="#1f1f3d", activebackground="#2a2a5e",
                    command=lambda i=i: button_click(i))
    btn.grid(row=i//3, column=i%3, padx=6, pady=6)
    buttons.append(btn)

label = tk.Label(game_frame, text="Turn: X",
                 font=("Arial", 14),
                 fg="white", bg="#141426")
label.grid(row=3, column=0, columnspan=3, pady=10)

score_label = tk.Label(game_frame, text="Score  X: 0   O: 0",
                       font=("Arial", 12),
                       fg="#00ffcc", bg="#141426")
score_label.grid(row=4, column=0, columnspan=3)

tk.Button(game_frame, text="Restart Board",
          bg="#f72585", fg="white",
          command=reset_board).grid(row=5, column=0, columnspan=3, pady=6)

tk.Button(game_frame, text="Reset Scores",
          bg="#b5179e", fg="white",
          command=reset_scores).grid(row=6, column=0, columnspan=3, pady=6)


root.mainloop()
