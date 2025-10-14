import math

# Constants
HUMAN = 'X'
AI = 'O'
EMPTY = ' '

# Initialize board
board = [EMPTY] * 9

# Winning combinations
winning_combos = [
    [0,1,2], [3,4,5], [6,7,8],  # rows
    [0,3,6], [1,4,7], [2,5,8],  # cols
    [0,4,8], [2,4,6]             # diagonals
]

# Print the board
def print_board():
    for i in range(3):
        print(board[i*3] + '|' + board[i*3+1] + '|' + board[i*3+2])
        if i < 2:
            print('-+-+-')
    print()

# Check for a winner
def check_winner(b, player):
    for combo in winning_combos:
        if all(b[i] == player for i in combo):
            return True
    return False

# Check for draw
def is_draw(b):
    return all(s != EMPTY for s in b)

# Get available moves
def available_moves(b):
    return [i for i, spot in enumerate(b) if spot == EMPTY]

# Heuristic for A* (score of board)
def evaluate(b):
    if check_winner(b, AI):
        return 10
    elif check_winner(b, HUMAN):
        return -10
    else:
        return 0

# A* / Minimax search
def minimax(b, depth, is_maximizing):
    score = evaluate(b)
    if score != 0 or is_draw(b):
        return score
    
    if is_maximizing:
        best = -math.inf
        for move in available_moves(b):
            b[move] = AI
            best = max(best, minimax(b, depth + 1, False))
            b[move] = EMPTY
        return best
    else:
        best = math.inf
        for move in available_moves(b):
            b[move] = HUMAN
            best = min(best, minimax(b, depth + 1, True))
            b[move] = EMPTY
        return best

# AI chooses the best move
def ai_move():
    best_val = -math.inf
    best_move = -1
    for move in available_moves(board):
        board[move] = AI
        move_val = minimax(board, 0, False)
        board[move] = EMPTY
        if move_val > best_val:
            best_val = move_val
            best_move = move
    board[best_move] = AI

# Main game loop
def play_game():
    print("You are X, AI is O")
    print_board()
    
    while True:
        # Human move
        move = int(input("Enter your move (0-8): "))
        if board[move] != EMPTY:
            print("Invalid move, try again.")
            continue
        board[move] = HUMAN
        print_board()
        if check_winner(board, HUMAN):
            print("You win!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        
        # AI move
        ai_move()
        print("AI moved:")
        print_board()
        if check_winner(board, AI):
            print("AI wins!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

# Start game
play_game()
