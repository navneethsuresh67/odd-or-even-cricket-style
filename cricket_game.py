"""
╔══════════════════════════════════════════════════════════════╗
║         CRICKET ODD OR EVEN — Python Assignment              ║
║              BSc CS 2nd Year — Tkinter GUI                   ║
╚══════════════════════════════════════════════════════════════╝

Concepts Used:
  ✔ Functions         - each action is a separate function
  ✔ Lists             - scoreboard history
  ✔ Dictionaries      - player and opponent stats
  ✔ GUI (tkinter)     - buttons, labels, frames
  ✔ if/else logic     - game rules
  ✔ random module     - opponent's number
"""

import tkinter as tk
import random

# ─────────────────────────────────────────────────
#  GAME DATA  (Dictionary)
# ─────────────────────────────────────────────────

player = {
    "name":   "You",
    "runs":   0,
    "balls":  0,
    "out":    False,
}

opponent = {
    "name":   "CPU",
    "runs":   0,
    "balls":  0,
    "out":    False,
}

game = {
    "phase":       "toss",    # toss → player_bat → cpu_bat → result
    "player_choice": None,    # "odd" or "even"
    "target":      0,
    "history":     [],        # List of ball-by-ball results
    "max_balls":   6,         # 1 over per side
}

# ─────────────────────────────────────────────────
#  COLOURS & FONTS
# ─────────────────────────────────────────────────

BG       = "#0a3d0a"   # cricket ground green
PANEL    = "#0d5c0d"
DARK     = "#061f06"
GOLD     = "#ffd700"
WHITE    = "#ffffff"
RED      = "#ff4444"
GREEN    = "#44ff88"
BLUE     = "#44aaff"
ORANGE   = "#ff8c00"
GRAY     = "#888888"
CREAM    = "#fffde7"

F_BIG    = ("Courier New", 26, "bold")
F_MED    = ("Courier New", 16, "bold")
F_SMALL  = ("Courier New", 12)
F_TINY   = ("Courier New", 10)

# ─────────────────────────────────────────────────
#  FUNCTIONS
# ─────────────────────────────────────────────────

def reset_game():
    """Reset all game data to start fresh."""
    player["runs"]  = 0
    player["balls"] = 0
    player["out"]   = False
    opponent["runs"]  = 0
    opponent["balls"] = 0
    opponent["out"]   = False
    game["phase"]     = "toss"
    game["player_choice"] = None
    game["target"]    = 0
    game["history"]   = []
    show_toss_screen()


def choose_odd_even(choice):
    """Player picks Odd or Even for the toss."""
    game["player_choice"] = choice
    cpu_number    = random.randint(1, 6)
    player_number = random.randint(1, 6)
    total         = cpu_number + player_number
    is_odd        = (total % 2 != 0)

    result_text = (
        f"You picked: {choice.upper()}\n"
        f"Your number: {player_number}  |  CPU: {cpu_number}\n"
        f"Total = {total}  →  {'ODD' if is_odd else 'EVEN'}"
    )

    # Check who won toss
    player_won_toss = (choice == "odd" and is_odd) or (choice == "even" and not is_odd)

    if player_won_toss:
        toss_label.config(text=result_text + "\n\n🏆 YOU WON THE TOSS!", fg=GOLD)
        bat_btn.config(state="normal")
        bowl_btn.config(state="normal")
    else:
        toss_label.config(text=result_text + "\n\n💀 CPU WON THE TOSS!\nCPU chose to BAT first.", fg=RED)
        # CPU bats first automatically
        root.after(1500, lambda: start_phase("cpu_bat"))


def player_bats_first():
    """Player chose to bat."""
    start_phase("player_bat")


def player_bowls_first():
    """Player chose to bowl → CPU bats first."""
    start_phase("cpu_bat")


def start_phase(phase):
    """Switch to batting or bowling phase."""
    game["phase"] = phase
    if phase == "player_bat":
        show_batting_screen()
    elif phase == "cpu_bat":
        show_cpu_batting_screen()


def play_ball(player_num):
    """
    Core game logic for one ball.
    Player picks a number (1-6).
    CPU picks random number (1-6).
    If both ODD or both EVEN → OUT!
    Otherwise → runs scored = player's number.
    """
    if game["phase"] != "player_bat":
        return

    cpu_num  = random.randint(1, 6)
    both_odd  = (player_num % 2 != 0) and (cpu_num % 2 != 0)
    both_even = (player_num % 2 == 0) and (cpu_num % 2 == 0)
    is_out    = both_odd or both_even

    player["balls"] += 1

    if is_out:
        player["out"] = True
        result = "OUT! 🏏"
        color  = RED
        game["history"].append(f"Ball {player['balls']}: You={player_num} CPU={cpu_num} → OUT")
    else:
        player["runs"] += player_num
        result = f"+{player_num} RUNS! 🏃"
        color  = GREEN
        game["history"].append(f"Ball {player['balls']}: You={player_num} CPU={cpu_num} → +{player_num}")

    # Update display
    ball_result_label.config(text=f"You: {player_num}  |  CPU: {cpu_num}\n{result}", fg=color)
    update_scoreboard()

    # Check if innings over
    if player["out"] or player["balls"] >= game["max_balls"]:
        game["target"] = player["runs"] + 1
        root.after(1200, lambda: start_phase("cpu_bat"))


def cpu_play_ball():
    """CPU batting logic — same odd/even rules."""
    if game["phase"] != "cpu_bat":
        return

    cpu_num    = random.randint(1, 6)
    player_num = random.randint(1, 6)   # simulated bowler number
    both_odd   = (cpu_num % 2 != 0) and (player_num % 2 != 0)
    both_even  = (cpu_num % 2 == 0) and (player_num % 2 == 0)
    is_out     = both_odd or both_even

    opponent["balls"] += 1

    if is_out:
        opponent["out"] = True
        result = "CPU OUT! 🎉"
        color  = GREEN
        game["history"].append(f"Ball {opponent['balls']}: CPU={cpu_num} You={player_num} → CPU OUT")
    else:
        opponent["runs"] += cpu_num
        result = f"CPU +{cpu_num} RUNS"
        color  = RED
        game["history"].append(f"Ball {opponent['balls']}: CPU={cpu_num} You={player_num} → +{cpu_num}")

    # Update CPU score display
    cpu_ball_label.config(
        text=f"CPU: {cpu_num}  |  You (bowl): {player_num}\n{result}", fg=color
    )
    cpu_score_label.config(
        text=f"CPU Score: {opponent['runs']} / {'OUT' if opponent['out'] else str(opponent['balls']) + ' balls'}",
        fg=WHITE
    )

    # Check target
    if game["target"] > 0 and opponent["runs"] >= game["target"]:
        root.after(800, show_result)
        return

    if opponent["out"] or opponent["balls"] >= game["max_balls"]:
        root.after(800, show_result)
    else:
        root.after(700, cpu_play_ball)   # auto-play next ball


def show_result():
    """Show final result screen."""
    game["phase"] = "result"
    clear_screen()

    p_runs = player["runs"]
    c_runs = opponent["runs"]

    if p_runs > c_runs:
        title  = "🏆 YOU WIN! 🏆"
        t_col  = GOLD
        msg    = f"You won by {p_runs - c_runs} runs!"
    elif c_runs > p_runs:
        title  = "💀 CPU WINS!"
        t_col  = RED
        msg    = f"CPU won by {c_runs - p_runs} runs!"
    else:
        title  = "🤝 IT'S A TIE!"
        t_col  = BLUE
        msg    = "What a match! Scores are equal!"

    # Result panel
    res_frame = tk.Frame(main_frame, bg=DARK, bd=2, relief="solid")
    res_frame.pack(pady=20, padx=20, fill="x")

    tk.Label(res_frame, text="MATCH RESULT", font=F_MED,
             bg=DARK, fg=GRAY).pack(pady=(10, 0))
    tk.Label(res_frame, text=title, font=F_BIG,
             bg=DARK, fg=t_col).pack(pady=5)
    tk.Label(res_frame, text=msg, font=F_MED,
             bg=DARK, fg=WHITE).pack(pady=5)

    # Scores
    score_frame = tk.Frame(main_frame, bg=PANEL)
    score_frame.pack(pady=10, padx=20, fill="x")

    tk.Label(score_frame, text=f"🏏 Your Score:  {p_runs} runs",
             font=F_MED, bg=PANEL, fg=GREEN).pack(pady=5)
    tk.Label(score_frame, text=f"🤖 CPU Score:   {c_runs} runs",
             font=F_MED, bg=PANEL, fg=ORANGE).pack(pady=5)

    # Ball-by-ball history (List display)
    tk.Label(main_frame, text="── Ball by Ball ──",
             font=F_SMALL, bg=BG, fg=GRAY).pack(pady=(10, 2))

    history_frame = tk.Frame(main_frame, bg=DARK)
    history_frame.pack(padx=20, fill="x")

    for entry in game["history"]:   # iterating our List
        tk.Label(history_frame, text=entry, font=F_TINY,
                 bg=DARK, fg=CREAM, anchor="w").pack(fill="x", padx=8)

    # Play again button
    tk.Button(main_frame, text="🔄  PLAY AGAIN",
              font=F_MED, bg=GOLD, fg=DARK,
              relief="flat", cursor="hand2",
              command=reset_game, pady=8, padx=20).pack(pady=20)


def update_scoreboard():
    """Update the live score display during batting."""
    score_label.config(
        text=f"Score: {player['runs']} / {'OUT' if player['out'] else str(player['balls']) + ' balls'}",
        fg=WHITE
    )


# ─────────────────────────────────────────────────
#  SCREEN BUILDER FUNCTIONS
# ─────────────────────────────────────────────────

def clear_screen():
    """Remove all widgets from main frame."""
    for widget in main_frame.winfo_children():
        widget.destroy()


def show_toss_screen():
    """Build the toss screen."""
    clear_screen()
    global toss_label, bat_btn, bowl_btn

    tk.Label(main_frame, text="🏏  CRICKET  ODD or EVEN  🏏",
             font=F_BIG, bg=BG, fg=GOLD).pack(pady=(20, 5))
    tk.Label(main_frame, text="BSc CS Python Assignment",
             font=F_TINY, bg=BG, fg=GRAY).pack()

    # Toss panel
    toss_frame = tk.Frame(main_frame, bg=PANEL, bd=2, relief="solid")
    toss_frame.pack(pady=15, padx=30, fill="x")

    tk.Label(toss_frame, text="STEP 1 — TOSS",
             font=F_MED, bg=PANEL, fg=GOLD).pack(pady=(10, 4))
    tk.Label(toss_frame,
             text="Pick ODD or EVEN.\nBoth players show a number (1-6).\nIf total matches your pick → YOU win the toss!",
             font=F_SMALL, bg=PANEL, fg=WHITE, justify="center").pack(pady=4)

    # Odd / Even buttons
    btn_row = tk.Frame(toss_frame, bg=PANEL)
    btn_row.pack(pady=12)

    tk.Button(btn_row, text="ODD", font=F_MED,
              bg="#c0392b", fg=WHITE, width=10,
              relief="flat", cursor="hand2", pady=10,
              command=lambda: choose_odd_even("odd")).pack(side="left", padx=15)

    tk.Button(btn_row, text="EVEN", font=F_MED,
              bg="#2980b9", fg=WHITE, width=10,
              relief="flat", cursor="hand2", pady=10,
              command=lambda: choose_odd_even("even")).pack(side="left", padx=15)

    toss_label = tk.Label(toss_frame, text="", font=F_SMALL,
                          bg=PANEL, fg=WHITE, justify="center")
    toss_label.pack(pady=8)

    # Bat or Bowl choice (hidden until toss won)
    choice_frame = tk.Frame(main_frame, bg=BG)
    choice_frame.pack(pady=10)

    tk.Label(choice_frame, text="STEP 2 — Choose to BAT or BOWL",
             font=F_MED, bg=BG, fg=GOLD).pack(pady=(0, 8))

    bat_btn = tk.Button(choice_frame, text="🏏  BAT FIRST", font=F_MED,
                        bg=GREEN, fg=DARK, width=14,
                        relief="flat", cursor="hand2", pady=8,
                        state="disabled", command=player_bats_first)
    bat_btn.pack(side="left", padx=15)

    bowl_btn = tk.Button(choice_frame, text="🎯  BOWL FIRST", font=F_MED,
                         bg=ORANGE, fg=DARK, width=14,
                         relief="flat", cursor="hand2", pady=8,
                         state="disabled", command=player_bowls_first)
    bowl_btn.pack(side="left", padx=15)


def show_batting_screen():
    """Build the batting screen."""
    clear_screen()
    global ball_result_label, score_label

    tk.Label(main_frame, text="🏏  YOUR BATTING INNINGS",
             font=F_BIG, bg=BG, fg=GOLD).pack(pady=(15, 3))

    target_txt = f"Target to set: Score as many as you can in {game['max_balls']} balls!"
    tk.Label(main_frame, text=target_txt,
             font=F_SMALL, bg=BG, fg=CREAM).pack()

    # Rules reminder
    rule_frame = tk.Frame(main_frame, bg=DARK)
    rule_frame.pack(padx=30, pady=8, fill="x")
    tk.Label(rule_frame,
             text="Rule: Pick a number 1-6. If BOTH numbers are ODD or BOTH are EVEN → YOU'RE OUT!",
             font=F_TINY, bg=DARK, fg=GRAY, wraplength=500).pack(pady=6)

    # Score display
    score_label = tk.Label(main_frame, text="Score: 0 / 0 balls",
                           font=F_MED, bg=BG, fg=WHITE)
    score_label.pack(pady=4)

    # Number buttons 1-6
    tk.Label(main_frame, text="Pick your number:",
             font=F_MED, bg=BG, fg=GOLD).pack(pady=(8, 4))

    btn_frame = tk.Frame(main_frame, bg=BG)
    btn_frame.pack()

    colors = ["#e74c3c","#e67e22","#f1c40f","#2ecc71","#3498db","#9b59b6"]
    for i in range(1, 7):
        tk.Button(btn_frame, text=str(i), font=F_BIG,
                  bg=colors[i-1], fg=WHITE,
                  width=3, height=1,
                  relief="flat", cursor="hand2",
                  command=lambda n=i: play_ball(n)).pack(side="left", padx=6)

    # Result display
    ball_result_label = tk.Label(main_frame, text="",
                                 font=F_MED, bg=BG, fg=WHITE, justify="center")
    ball_result_label.pack(pady=12)


def show_cpu_batting_screen():
    """Build the CPU batting screen."""
    clear_screen()
    global cpu_ball_label, cpu_score_label

    if game["target"] > 0:
        header = f"🎯  CPU IS CHASING {game['target']} RUNS"
        sub    = f"You scored {player['runs']} runs. CPU needs {game['target']} to win!"
    else:
        header = "🤖  CPU IS BATTING FIRST"
        sub    = f"CPU gets {game['max_balls']} balls. Then you chase!"

    tk.Label(main_frame, text=header, font=F_BIG, bg=BG, fg=RED).pack(pady=(15, 3))
    tk.Label(main_frame, text=sub, font=F_SMALL, bg=BG, fg=CREAM).pack()

    # Score
    cpu_score_label = tk.Label(main_frame,
                               text="CPU Score: 0 / 0 balls",
                               font=F_MED, bg=BG, fg=WHITE)
    cpu_score_label.pack(pady=10)

    # Animation label
    cpu_ball_label = tk.Label(main_frame, text="CPU is playing...",
                              font=F_MED, bg=BG, fg=ORANGE, justify="center")
    cpu_ball_label.pack(pady=10)

    tk.Label(main_frame, text="(Sit back and watch! 👀)",
             font=F_SMALL, bg=BG, fg=GRAY).pack()

    # Auto start CPU batting
    root.after(800, cpu_play_ball)


# ─────────────────────────────────────────────────
#  MAIN WINDOW SETUP
# ─────────────────────────────────────────────────

root = tk.Tk()
root.title("🏏 Cricket Odd or Even — Python Assignment")
root.geometry("600x580")
root.resizable(False, False)
root.configure(bg=BG)

# Header bar
header_bar = tk.Frame(root, bg=DARK, height=40)
header_bar.pack(fill="x")
tk.Label(header_bar, text="🏏  CRICKET ODD OR EVEN  🏏",
         font=("Courier New", 13, "bold"),
         bg=DARK, fg=GOLD).pack(pady=6)

# Main scrollable frame
main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=10, pady=5)

# Start the game
show_toss_screen()

root.mainloop()
