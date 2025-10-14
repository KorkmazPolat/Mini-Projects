import math

# Constants
AI = 'O'            # A* / Minimax player
RULE_BASED = 'X'    # Perfect rule-based player
EMPTY = ' '

# Winning combinations
winning_combos = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

# Check winner
def check_winner(b, player):
    for combo in winning_combos:
        if all(b[i] == player for i in combo):
            return True
    return False

# Check draw
def is_draw(b):
    return all(s != EMPTY for s in b)

# Get available moves
def available_moves(b):
    return [i for i, spot in enumerate(b) if spot == EMPTY]

# Evaluate board from AI perspective
def evaluate(b):
    if check_winner(b, AI):
        return 10
    elif check_winner(b, RULE_BASED):
        return -10
    else:
        return 0

# Minimax algorithm for A* AI
def minimax(b, is_maximizing):
    score = evaluate(b)
    if score != 0 or is_draw(b):
        return score

    if is_maximizing:
        best = -math.inf
        for move in available_moves(b):
            b[move] = AI
            best = max(best, minimax(b, False))
            b[move] = EMPTY
        return best
    else:
        best = math.inf
        for move in available_moves(b):
            b[move] = RULE_BASED
            best = min(best, minimax(b, True))
            b[move] = EMPTY
        return best

# A* AI move
def ai_move(b):
    best_val = -math.inf
    best_move = None
    for move in available_moves(b):
        b[move] = AI
        move_val = minimax(b, False)
        b[move] = EMPTY
        if move_val > best_val:
            best_val = move_val
            best_move = move
    b[best_move] = AI

# Perfect rule-based move (looks at all possible moves like Minimax)
def perfect_rule_based_move(b):
    best_val = math.inf
    best_move = None
    for move in available_moves(b):
        b[move] = RULE_BASED
        move_val = minimax(b, True)  # Use AI minimax logic from opponent perspective
        b[move] = EMPTY
        if move_val < best_val:
            best_val = move_val
            best_move = move
    b[best_move] = RULE_BASED

# Simulate one game
def play_game(first_player):
    board = [EMPTY]*9
    turn = first_player
    while True:
        if turn == AI:
            ai_move(board)
            if check_winner(board, AI):
                return AI
            turn = RULE_BASED
        else:
            perfect_rule_based_move(board)
            if check_winner(board, RULE_BASED):
                return RULE_BASED
            turn = AI
        if is_draw(board):
            return 'Draw'

# Run 100 games
results = {AI:0, RULE_BASED:0, 'Draw':0}
for i in range(100):
    first = AI if i % 2 == 0 else RULE_BASED
    winner = play_game(first)
    results[winner] += 1

# Print results
print("After 100 games between A* AI and perfect rule-based player:")
print(f"{AI} (A*) wins: {results[AI]}")
print(f"{RULE_BASED} (Perfect rule-based) wins: {results[RULE_BASED]}")
print(f"Draws: {results['Draw']}")
