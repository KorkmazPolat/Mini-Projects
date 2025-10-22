import random
import argparse

try:
    import tkinter as tk
except Exception:
    tk = None

# --- Moves and outcomes ---
moves = ["rock", "paper", "scissors"]

def outcome(me, opp):
    if me == opp:
        return "draw"
    if (me == "rock" and opp == "scissors") or \
       (me == "paper" and opp == "rock") or \
       (me == "scissors" and opp == "paper"):
        return "win"
    return "lose"

# --- Simple 2-step conditional AI ---
class RPS_AI:
    def __init__(self):
        self.history = []  # [(my_move, opp_move, result)]
        self.stats = {}    # {((res1, opp1), (res2, opp2)): {opp_next: count}}

    def observe(self, my_move, opp_move):
        res = outcome(my_move, opp_move)
        self.history.append((my_move, opp_move, res))
        if len(self.history) >= 3:
            # take last 2 rounds as context
            key = ((self.history[-3][2], self.history[-3][1]),
                   (self.history[-2][2], self.history[-2][1]))
            next_opp = opp_move
            if key not in self.stats:
                self.stats[key] = {"rock": 0, "paper": 0, "scissors": 0}
            self.stats[key][next_opp] += 1
        return res

    def predict_explained(self):
        """Return (ai_move, info) where info explains the prediction.

        info includes:
          - context: ((res, opp), (res, opp)) or None
          - counts: dict of raw counts for predicted opponent move
          - distribution: normalized probabilities over moves
          - opp_guess: most likely opponent move (string)
          - reason: 'conditional-2step' | 'uniform-random'
        """
        if len(self.history) < 2:
            opp_guess = random.choice(moves)
            dist = {m: 1/3 for m in moves}
            reason = "uniform-random"
            context = None
            counts = {m: 0 for m in moves}
        else:
            context = ((self.history[-2][2], self.history[-2][1]),
                       (self.history[-1][2], self.history[-1][1]))
            counts = self.stats.get(context, {m: 0 for m in moves})
            if context in self.stats and sum(counts.values()) > 0:
                opp_guess = max(counts, key=counts.get)
                total = sum(counts.values())
                dist = {m: counts[m] / total for m in moves}
                reason = "conditional-2step"
            else:
                opp_guess = random.choice(moves)
                dist = {m: 1/3 for m in moves}
                reason = "uniform-random"

        # choose move that beats predicted opponent move
        if opp_guess == "rock":
            ai_move = "paper"
        elif opp_guess == "paper":
            ai_move = "scissors"
        else:
            ai_move = "rock"

        info = {
            "context": context,
            "counts": counts,
            "distribution": dist,
            "opp_guess": opp_guess,
            "reason": reason,
            "chosen": ai_move,
        }
        return ai_move, info

    def predict(self):
        ai_move, _ = self.predict_explained()
        return ai_move

# --- Game loop ---
def play():
    print("Rock-Paper-Scissors (2-step Conditional Probability AI)")
    print("Enter r/p/s or q to quit\n")

    ai = RPS_AI()
    w = d = l = 0
    round_no = 1

    while True:
        you = input(f"Round {round_no} - your move: ").strip().lower()
        if you in {"q", "quit"}:
            break
        if you not in {"r", "p", "s", "rock", "paper", "scissors"}:
            print("Please type r, p or s.")
            continue

        you = {"r": "rock", "p": "paper", "s": "scissors"}.get(you, you)
        ai_move, info = ai.predict_explained()
        result = ai.observe(you, ai_move)

        if result == "win":
            w += 1
        elif result == "draw":
            d += 1
        else:
            l += 1

        print(f"You: {you} | AI: {ai_move} => {result.upper()}")
        # Analytics
        dist = info["distribution"]
        counts = info["counts"]
        reason = info["reason"]
        context = info["context"]
        print("AI prediction details:")
        print(f"  - Method: {reason}  Context: {context}")
        print("  - Distribution (your next move):")
        for m in moves:
            print(f"    {m:<9} -> {dist[m]*100:.1f}% (count={counts.get(m,0)})")
        print(f"  - Predicted you would play: {info['opp_guess']}, so AI chose: {info['chosen']}")
        print(f"Score W/D/L: {w}/{d}/{l}\n")
        round_no += 1

    print(f"Final Score: {w} Wins, {d} Draws, {l} Losses")


def start_gui():
    if tk is None:
        print("Tkinter not available. Please run CLI mode.")
        return 1

    ai = RPS_AI()
    state = {"w": 0, "d": 0, "l": 0, "round": 1}

    root = tk.Tk()
    root.title("Rock-Paper-Scissors — Basic UI")

    title = tk.Label(root, text="Rock-Paper-Scissors (AI)", font=("Helvetica", 14, "bold"))
    title.pack(pady=6)

    score_var = tk.StringVar()
    def update_score():
        score_var.set(f"Round {state['round']}  |  W/D/L: {state['w']}/{state['d']}/{state['l']}")
    score = tk.Label(root, textvariable=score_var, font=("Helvetica", 12))
    score.pack(pady=4)
    update_score()

    result_var = tk.StringVar(value="Make your move!")
    result_label = tk.Label(root, textvariable=result_var, font=("Helvetica", 12))
    result_label.pack(pady=6)

    analytics = tk.Text(root, height=12, width=60)
    analytics.pack(padx=8, pady=6)
    analytics.insert("1.0", "Analytics will appear here after each round.\n")
    analytics.config(state=tk.DISABLED)

    def set_analytics(text: str):
        analytics.config(state=tk.NORMAL)
        analytics.delete("1.0", tk.END)
        analytics.insert("1.0", text)
        analytics.config(state=tk.DISABLED)

    def do_round(you: str):
        ai_move, info = ai.predict_explained()
        res = ai.observe(you, ai_move)
        if res == "win":
            state["w"] += 1
        elif res == "draw":
            state["d"] += 1
        else:
            state["l"] += 1
        state["round"] += 1
        result_var.set(f"You: {you} | AI: {ai_move} => {res.upper()}")
        update_score()

        dist = info["distribution"]
        counts = info["counts"]
        lines = []
        lines.append("AI prediction (your next move):")
        for m in moves:
            lines.append(f"  {m:<9} -> {dist[m]*100:.1f}% (count={counts.get(m,0)})")
        lines.append(f"Predicted: {info['opp_guess']}  |  Decision: {info['chosen']}  |  Method: {info['reason']}")
        lines.append(f"Context: {info['context']}")
        set_analytics("\n".join(lines))

    btns = tk.Frame(root)
    btns.pack(pady=8)
    tk.Button(btns, text="Rock", width=10, command=lambda: do_round("rock")).grid(row=0, column=0, padx=5)
    tk.Button(btns, text="Paper", width=10, command=lambda: do_round("paper")).grid(row=0, column=1, padx=5)
    tk.Button(btns, text="Scissors", width=10, command=lambda: do_round("scissors")).grid(row=0, column=2, padx=5)

    def reset():
        ai.history.clear()
        ai.stats.clear()
        state.update({"w": 0, "d": 0, "l": 0, "round": 1})
        result_var.set("Make your move!")
        update_score()
        set_analytics("Analytics will appear here after each round.\n")

    tk.Button(root, text="Reset", command=reset).pack(pady=4)

    root.mainloop()
    return 0


def main():
    parser = argparse.ArgumentParser(description="Play RPS in CLI or GUI with a basic AI.")
    parser.add_argument("--mode", choices=["cli", "gui"], default=("gui" if tk is not None else "cli"), help="Run in CLI or GUI mode")
    args = parser.parse_args()

    if args.mode == "gui":
        return start_gui()
    else:
        play()
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
