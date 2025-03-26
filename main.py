from board import *
from ai import compute_best_move
from main_menu import main_menu
import pygame
import chess
import time


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Megan's Chess Practice")

    # For one-letter representation, a standard system font works fine.
    piece_font = pygame.font.SysFont("Segoe UI Symbol", 48)
    clock = pygame.time.Clock()

    ai_depth, ai_time = main_menu(screen)

    board = chess.Board()
    selected_square = None
    recommended_move = None
    user_color = chess.WHITE

    def update_recommendation():
        nonlocal recommended_move
        if board.turn == user_color:
            recommended_move = compute_best_move(board, ai_depth, ai_time, True)
        else:
            recommended_move = None

    update_recommendation()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == user_color:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                file = mouse_x // SQ_SIZE
                rank = mouse_y // SQ_SIZE
                clicked_square = chess.square(file, 7 - rank)
                piece = board.piece_at(clicked_square)
                if selected_square is None:
                    if piece is not None and piece.color == user_color:
                        selected_square = clicked_square
                else:
                    move = chess.Move(selected_square, clicked_square)
                    if move in board.legal_moves:
                        animate_move(screen, board, move, piece_font)
                        board.push(move)
                        selected_square = None
                        update_recommendation()
                    else:
                        if piece is not None and piece.color == user_color:
                            selected_square = clicked_square
                        else:
                            selected_square = None

        if board.turn != user_color and not board.is_game_over():
            pygame.display.flip()
            time.sleep(0.5)
            ai_move = compute_best_move(board, ai_depth, ai_time, False)
            if ai_move is None:
                break
            animate_move(screen, board, ai_move, piece_font)
            board.push(ai_move)
            update_recommendation()

        draw_board(screen)
        draw_pieces(screen, board, piece_font)

        if selected_square is not None:
            highlight_moves(screen, board, selected_square, user_color)
            if recommended_move is not None and recommended_move.from_square == selected_square:
                draw_arrow(screen, recommended_move.from_square, recommended_move.to_square)

        pygame.display.flip()
        clock.tick(FPS)

        if board.is_game_over():
            print("Game over:", board.result())
            time.sleep(3)
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()