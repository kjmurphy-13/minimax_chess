from board import evaluate_board
import chess
import time
import math

def minimax(board: chess.Board, depth, alpha, beta, maximizing, start_time, time_limit, visited=None):
    if visited is None:
        visited = set()
    board_fen = board.fen()
    # If this board has been seen before in this branch, apply a heavy penalty.
    if board_fen in visited:
        penalty = 100
        return (evaluate_board(board) - penalty if maximizing else evaluate_board(board) + penalty), None

    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None
    if time.time() - start_time > time_limit:
        return evaluate_board(board), None

    # Add current position to visited set for cycle detection.
    visited = visited.copy()
    visited.add(board_fen)

    best_move = None
    last_move = board.move_stack[-1] if board.move_stack else None
    if maximizing:
        max_eval = -math.inf
        for move in board.legal_moves:
            reversal_penalty = 20 if (last_move and move.from_square == last_move.to_square and move.to_square == last_move.from_square) else 0

            board.push(move)
            eval_score, _ = minimax(board, depth - 1, alpha, beta, False, start_time, time_limit, visited)
            board.pop()
            eval_score -= reversal_penalty
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in board.legal_moves:
            reversal_penalty = 20 if (last_move and move.from_square == last_move.to_square and move.to_square == last_move.from_square) else 0

            board.push(move)
            eval_score, _ = minimax(board, depth - 1, alpha, beta, True, start_time, time_limit, visited)
            board.pop()
            eval_score += reversal_penalty
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def compute_best_move(board: chess.Board, max_depth, time_limit, is_maximizing):
    best_move = None
    start_time = time.time()
    depth = 1
    while True:
        if time.time() - start_time > time_limit:
            break
        score, move = minimax(board, depth, -math.inf, math.inf, is_maximizing, start_time, time_limit)
        if move is not None:
            best_move = move
        depth += 1
        if depth > max_depth:
            break
    return best_move