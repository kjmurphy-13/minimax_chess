from config import *
import chess
import pygame
import math

def evaluate_board(board: chess.Board):
    if board.is_checkmate():
        return -9999 if board.turn == chess.WHITE else 9999

    material_score = 0
    pawn_structure_score = 0
    king_safety_score = 0
    development_score = 0
    center_control_score = 0
    mobility_score = 0
    positional_score = 0

    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0
    }

    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]

    for color in [chess.WHITE, chess.BLACK]:
        sign = 1 if color == chess.WHITE else -1

        for piece_type, value in piece_values.items():
            pieces = board.pieces(piece_type, color)
            material_score += sign * value * len(pieces)
            table = piece_square_tables[piece_type]
            for square in pieces:
                index = square if color == chess.WHITE else 63 - square
                positional_score += sign * table[index]

            if piece_type in [chess.KNIGHT, chess.BISHOP]:
                for square in pieces:
                    if color == chess.WHITE:
                        if piece_type == chess.KNIGHT and square not in [chess.B1, chess.G1]:
                            development_score += sign * 20
                        elif piece_type == chess.BISHOP and square not in [chess.C1, chess.F1]:
                            development_score += sign * 20
                    else:
                        if piece_type == chess.KNIGHT and square not in [chess.B8, chess.G8]:
                            development_score += sign * 20
                        elif piece_type == chess.BISHOP and square not in [chess.C8, chess.F8]:
                            development_score += sign * 20

        pawns = board.pieces(chess.PAWN, color)
        files_with_pawns = {}
        for pawn_square in pawns:
            file = chess.square_file(pawn_square)
            files_with_pawns.setdefault(file, []).append(pawn_square)
        for file, squares in files_with_pawns.items():
            if len(squares) > 1:
                pawn_structure_score += sign * (-10 * (len(squares) - 1))
        for pawn_square in pawns:
            file = chess.square_file(pawn_square)
            adjacent_files = []
            if file - 1 >= 0:
                adjacent_files.append(file - 1)
            if file + 1 <= 7:
                adjacent_files.append(file + 1)
            found_adjacent = any(adj_file in files_with_pawns for adj_file in adjacent_files)
            if not found_adjacent:
                pawn_structure_score += sign * -15

        king_square = list(board.pieces(chess.KING, color))[0]
        enemy_attackers = board.attackers(not color, king_square)
        king_safety_score += sign * (-5 * len(enemy_attackers))
        if color == chess.WHITE and king_square in [chess.G1, chess.C1, chess.G2, chess.C2]:
            king_safety_score += sign * 30
        elif color == chess.BLACK and king_square in [chess.G8, chess.C8, chess.G7, chess.C7]:
            king_safety_score += sign * 30

        for square in center_squares:
            if board.is_attacked_by(color, square):
                center_control_score += sign * 10

        legal_moves = [move for move in board.legal_moves if board.color_at(move.from_square) == color]
        mobility_score += sign * (len(legal_moves) * 2)

    total = (material_score + pawn_structure_score + king_safety_score +
             development_score + center_control_score + mobility_score +
             positional_score)
    return total

def square_to_coords(square):
    file = chess.square_file(square)
    rank = 7 - chess.square_rank(square)
    return (file * SQ_SIZE, rank * SQ_SIZE)

def draw_board(screen):
    for rank in range(8):
        for file in range(8):
            color = WHITE_SQ if (rank + file) % 2 == 0 else BLACK_SQ
            rect = pygame.Rect(file * SQ_SIZE, rank * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, rect)

def draw_pieces(screen, board, piece_font):
    for square, piece in board.piece_map().items():
        x, y = square_to_coords(square)
        piece_text = PIECE_UNICODE[piece]
        text_surface = piece_font.render(piece_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x + SQ_SIZE / 2, y + SQ_SIZE / 2))
        screen.blit(text_surface, text_rect)

def highlight_moves(screen, board, selected_square, user_color):
    if selected_square is None:
        return
    highlight_surf = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
    danger_surf = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
    highlight_surf.fill(HIGHLIGHT_COLOR)
    danger_surf.fill(DANGER_COLOR)

    for move in board.legal_moves:
        if move.from_square == selected_square:
            board.push(move)
            is_danger = board.is_attacked_by(not user_color, move.to_square)
            board.pop()
            x, y = square_to_coords(move.to_square)
            screen.blit(danger_surf if is_danger else highlight_surf, (x, y))


def draw_arrow(screen, start_square, end_square):
    start_x, start_y = square_to_coords(start_square)
    end_x, end_y = square_to_coords(end_square)
    start_center = (start_x + SQ_SIZE / 2, start_y + SQ_SIZE / 2)
    end_center = (end_x + SQ_SIZE / 2, end_y + SQ_SIZE / 2)
    pygame.draw.line(screen, ARROW_COLOR, start_center, end_center, 5)
    angle = math.atan2(end_center[1] - start_center[1], end_center[0] - start_center[0])
    arrow_length = 15
    arrow_angle = math.pi / 6
    left_x = end_center[0] - arrow_length * math.cos(angle - arrow_angle)
    left_y = end_center[1] - arrow_length * math.sin(angle - arrow_angle)
    right_x = end_center[0] - arrow_length * math.cos(angle + arrow_angle)
    right_y = end_center[1] - arrow_length * math.sin(angle + arrow_angle)
    pygame.draw.polygon(screen, ARROW_COLOR, [end_center, (left_x, left_y), (right_x, right_y)])


def animate_move(screen, board, move, piece_font):
    start_x, start_y = square_to_coords(move.from_square)
    end_x, end_y = square_to_coords(move.to_square)
    frames = 10
    clock = pygame.time.Clock()
    for frame in range(1, frames + 1):
        draw_board(screen)
        draw_pieces(screen, board, piece_font)
        interp_x = start_x + (end_x - start_x) * frame / frames
        interp_y = start_y + (end_y - start_y) * frame / frames
        piece = board.piece_at(move.from_square)
        if piece:
            draw_pieces(screen, board, piece_font)
            #piece_text = PIECE_UNICODE[piece]
            #text_surface = piece_font.render(piece_text, True, (0, 0, 0))
            #text_rect = text_surface.get_rect(center=(interp_x + SQ_SIZE / 2, interp_y + SQ_SIZE / 2))
            #screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(FPS)
