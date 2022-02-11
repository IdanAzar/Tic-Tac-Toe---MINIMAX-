import const
import pygame
import numpy as np
import minmax


def initialize_screen():
    pygame.init()

    # creating screen
    screen = pygame.display.set_mode(const.SCREEN_SIZE)

    # name the screen
    pygame.display.set_caption(' TIC TAC TOE ')

    # fill back ground color
    screen.fill(const.BG_COLOR)

    return screen


def initialize_matrix():
    return np.zeros((const.BOARD_ROWS, const.BOARD_COLS))


def draw_line(window):
    # first horizontal line
    pygame.draw.line(window, const.LINE_COLOR, (0, 200), (600, 200), const.LINE_WIDTH)

    # second horizontal line
    pygame.draw.line(window, const.LINE_COLOR, (0, 400), (600, 400), const.LINE_WIDTH)

    # first vertical line
    pygame.draw.line(window, const.LINE_COLOR, (200, 0), (200, 600), const.LINE_WIDTH)

    # second vertical line
    pygame.draw.line(window, const.LINE_COLOR, (400, 0), (400, 600), const.LINE_WIDTH)


def draw_on_screen(window, matrix):
    for row in range(const.BOARD_ROWS):
        for col in range(const.BOARD_COLS):
            # draw X on square position
            if matrix[row][col] == 1:
                pygame.draw.line(window, const.X_COLOR,
                                 (col * const.LENGTH_SQUARE + const.SPACE_LINES, row * const.LENGTH_SQUARE +
                                  const.LENGTH_SQUARE - const.SPACE_LINES),
                                 (col * const.LENGTH_SQUARE + const.LENGTH_SQUARE - const.SPACE_LINES,
                                  row * const.LENGTH_SQUARE + const.SPACE_LINES),
                                 const.X_WIDTH)
                pygame.draw.line(window, const.X_COLOR,
                                 (col * const.LENGTH_SQUARE + const.SPACE_LINES, row * const.LENGTH_SQUARE +
                                  const.SPACE_LINES),
                                 (col * const.LENGTH_SQUARE + const.LENGTH_SQUARE - const.SPACE_LINES,
                                  row * const.LENGTH_SQUARE + const.LENGTH_SQUARE - const.SPACE_LINES),
                                 const.X_WIDTH)
            elif matrix[row][col] == 2:
                # draw O on square position
                pygame.draw.circle(window, const.CIRCLE_COLOR,
                                   (int(col * const.LENGTH_SQUARE + (const.LENGTH_SQUARE // 2)),
                                    int(row * const.LENGTH_SQUARE + (const.LENGTH_SQUARE // 2))),
                                   const.CIRCLE_RADIUS, const.CIRCLE_WIDTH)


def mark_square(matrix, row, col, player):
    matrix[row][col] = player


def available_square(matrix, row, col):
    return matrix[row][col] == 0


def matrix_is_full(matrix):
    for row in range(const.BOARD_ROWS):
        for col in range(const.BOARD_COLS):
            if available_square(matrix, row, col):
                return False
    return True


def check_winner(window, board, player):
    # check vertical lines
    for col in range(const.BOARD_COLS):
        if board[0][col] == player and board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            draw_vertical_line(window, col, player)
            return True

    # check horizontal lines
    for row in range(const.BOARD_ROWS):
        if board[row][0] == player and board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            draw_horizontal_line(window, row, player)
            return True

    # check asc diagonal
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] == player:
        draw_asc_diagonal(window, player)
        return True

    # check DESC diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] == player:
        draw_desc_diagonal(window, player)
        return True

    # player does not win yet
    return False


def draw_vertical_line(screen, col, player):
    # X pose doesn't change in vertical lines
    pos_x = col * const.LENGTH_SQUARE + const.LENGTH_SQUARE // 2

    # set color vertical line according to player
    if player == 1:
        color = const.X_COLOR
    else:
        color = const.CIRCLE_COLOR

    # draw vertical line
    pygame.draw.line(screen, color, (pos_x, 15), (pos_x, const.SCREEN_SIZE[1] - 15), const.LINE_WIDTH)


def draw_horizontal_line(screen, row, player):
    # Y pose doesn't change in vertical lines
    pos_y = row * const.LENGTH_SQUARE + const.LENGTH_SQUARE // 2

    # set color horizontal line according to player
    if player == 1:
        color = const.X_COLOR
    else:
        color = const.CIRCLE_COLOR

    # draw horizontal line
    pygame.draw.line(screen, color, (15, pos_y), (const.SCREEN_SIZE[0] - 15, pos_y), const.LINE_WIDTH)


def draw_asc_diagonal(screen, player):
    # set color asc diagonal line according to player
    if player == 1:
        color = const.X_COLOR
    else:
        color = const.CIRCLE_COLOR

    # draw asc diagonal line
    pygame.draw.line(screen, color, (15, const.SCREEN_SIZE[1] - 15), (const.SCREEN_SIZE[0] - 15, 15), const.LINE_WIDTH)


def draw_desc_diagonal(screen, player):
    # set color desc diagonal line according to player
    if player == 1:
        color = const.X_COLOR
    else:
        color = const.CIRCLE_COLOR

    # draw desc diagonal line
    pygame.draw.line(screen, color, (15, 15), (const.SCREEN_SIZE[0] - 15, const.SCREEN_SIZE[1] - 15), const.LINE_WIDTH)


def restart(window, board):
    window.fill(const.BG_COLOR)
    draw_line(window)
    for row in range(const.BOARD_ROWS):
        for col in range(const.BOARD_COLS):
            board[row][col] = const.EMPTY
    # set current player to player 1 and start new game so no one wins yet
    return 1, False


def game():
    print("\nTo reset game press p.\nplayer 1 is X\nBOT is O\nPress on clear square to see O turn\nHAVE FUN")

    # Init game screen and board
    window = initialize_screen()
    board = initialize_matrix()

    # draw horizontal and vertical lines
    draw_line(window)

    # creating starting player to be X (by the rules...)
    player = 1

    # game loop
    run = True
    is_win = False
    while run:
        for event in pygame.event.get():
            # check for exit
            if event.type == pygame.QUIT:
                run = False

            # check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and not is_win:
                # getting the console cords between 0-2
                row_console = int(event.pos[1] // const.LENGTH_SQUARE)  # row index
                col_console = int(event.pos[0] // const.LENGTH_SQUARE)  # col index

                # mark chosen square if it is available
                if available_square(board, row_console, col_console):
                    if player == 1:
                        mark_square(board, row_console, col_console, player)
                        if check_winner(window, board, player):
                            is_win = True
                        player = 2
                    else:
                        indexes = minmax.ai_result(board)
                        row_console, col_console = indexes[0], indexes[1]
                        mark_square(board, row_console, col_console, player)
                        if check_winner(window, board, player):
                            is_win = True
                        player = 1

                    # draw current board
                    draw_on_screen(window, board)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player, is_win = restart(window, board)

        pygame.display.update()


def main():
    game()


if __name__ == '__main__':
    main()
