"""
Hackathon TicTacToe (made in a single file to fit the theme xD)
(i also forgot pygame had sprites)
"""

import random
import math
import pygame

pygame.init()

# COLORS
BASE = (59, 66, 82)
CRUST = (76, 86, 106)
MAUVE = (180, 142, 173)
RED = (191, 97, 106)
MAROON = (165, 66, 66)
PEACH = (208, 135, 112)
YELLOW = (235, 203, 139)
GREEN = (163, 190, 140)
TEAL = (136, 192, 208)
SKY = (129, 161, 193)
BLUE = (94, 129, 172)
CYAN = (143, 188, 187)
BLACK = (46, 52, 64)
WHITE = (236, 239, 244)

class Window():
    """ Main game window class """
    def __init__(self):
        self.info = pygame.display.Info()
        self.width = self.info.current_w
        self.height = self.info.current_w
        self.scale_x = self.width / 1920
        self.scale_y = self.height / 1080

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)

        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Dysfunctional TicTacToe')

        self.is_fullscreen = True
        self.old_size = (1600, 850)

        self.running = False
        self.can_play = False
        self.is_over = False
        self.games_won = 0
        self.games_lost = 0
        self.games_drawn = 0

        self.has_processed_challenge = False
        self.wanted_pos = (0, 0)
        self.current_challenge = Challenge(0, [])
        self.challenge_timer = 0
        self.challenge_message = [0, "", WHITE]
        self.transparent_background = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.transparent_background, (*BLACK, 150), (0, 0, self.width,self.height))

        self.font_big = pygame.font.Font(None, round(200 * ((self.scale_x + self.scale_y) / 2)))
        self.font = pygame.font.Font(None, round(150 * ((self.scale_x + self.scale_y) / 2)))
        self.font_small = pygame.font.Font(None, round(80 * ((self.scale_x + self.scale_y) / 2)))
        self.font_mini = pygame.font.Font(None, round(65 * ((self.scale_x + self.scale_y) / 2)))

        self.tictactoe = TicTacToe()

    @staticmethod
    def is_in_rect(pos, rect):
        """ Check if position is inside a rect """
        if rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]:
            return True

        return False

    @staticmethod
    def is_point_in_circle(pos, circle_center, radius):
        """ Check if position is inside a circle """
        x, y = pos
        cx, cy = circle_center
        distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)

        return distance <= radius

    def run(self):
        """ Main game logic """
        self.running = True
        self.can_play = True
        self.is_over = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_F11:
                        # Toggle fullscreen
                        self.is_fullscreen = not self.is_fullscreen
                        if self.is_fullscreen:
                            self.old_size = (self.width, self.height)
                            self.screen = pygame.display.set_mode(
                                pygame.display.list_modes()[0],
                                pygame.FULLSCREEN
                            )
                        else:
                            self.width, self.height = self.old_size
                            self.screen = pygame.display.set_mode(
                                self.old_size,
                                pygame.RESIZABLE
                            )
                    else:
                        if self.current_challenge.type == 5:
                            key = pygame.key.name(event.key)
                            match self.current_challenge.type:
                                case 5:
                                    key_index = self.current_challenge.extra[0]
                                    if self.current_challenge.challenge[key_index] == key:
                                        self.current_challenge.extra[0] += 1
                        elif event.key == pygame.K_r:
                            # Restart if the game is over
                            if self.is_over:
                                self.is_over = False
                                self.can_play = True
                                self.current_challenge = Challenge(0, [])
                                self.challenge_timer = 0
                                self.tictactoe = TicTacToe()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    board_pos = self.tictactoe.get_board_pos(pos, self)
                    match self.current_challenge.type:
                        case 0:
                            if self.can_play:
                                if board_pos and \
                                    self.tictactoe.board[board_pos[0]][board_pos[1]] == 0:

                                    self.can_play = False
                                    Challenge.get_challenge(self)
                                    self.wanted_pos = board_pos
                        case 1:
                            for answer in self.current_challenge.extra:
                                if Window.is_in_rect(pos, answer[0]):
                                    self.current_challenge.completed = True
                                    self.current_challenge.successful = \
                                        self.current_challenge.challenge[2] == answer[1]
                                    break
                        case 2:
                            for n, target_pos in enumerate(self.current_challenge.challenge):
                                if self.is_point_in_circle(
                                    pos,
                                    target_pos,
                                    round(50 * ((self.scale_x + self.scale_y) / 2))
                                ):
                                    self.current_challenge.challenge.pop(n)
                                    if not self.current_challenge.challenge:
                                        self.current_challenge.completed = True
                                        self.current_challenge.successful = True
                                    break
                        case 3:
                            smallest_num = min(
                                self.current_challenge.challenge,
                                key=lambda x: x[1]
                            )[1]
                            for n, button in enumerate(self.current_challenge.challenge):
                                if self.is_point_in_circle(
                                    pos,
                                    button[0],
                                    round(50 * ((self.scale_x + self.scale_y) / 2))
                                ) and smallest_num == button[1]:
                                    self.current_challenge.challenge.pop(n)
                                    if not self.current_challenge.challenge:
                                        self.current_challenge.completed = True
                                        self.current_challenge.successful = True
                        case 4:
                            if not self.current_challenge.challenge[2]:
                                if self.is_point_in_circle(
                                        pos,
                                        self.current_challenge.challenge[0],
                                        round(50 * ((self.scale_x + self.scale_y) / 2))
                                ):
                                    self.current_challenge.challenge[2] = 1
                                elif self.is_point_in_circle(
                                        pos,
                                        self.current_challenge.challenge[1],
                                        round(50 * ((self.scale_x + self.scale_y) / 2))
                                ):
                                    self.current_challenge.challenge[2] = 2
                elif event.type == pygame.MOUSEBUTTONUP:
                    match self.current_challenge.type:
                        case 4:
                            self.current_challenge.challenge[2] = False
                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    match self.current_challenge.type:
                        case 4:
                            if self.current_challenge.challenge[2] == 1:
                                self.current_challenge.challenge[0] = pos
                            elif self.current_challenge.challenge[2] == 2:
                                self.current_challenge.challenge[1] = pos

                elif event.type == pygame.WINDOWSIZECHANGED:
                    # Handle window resizing
                    self.info = pygame.display.Info()
                    self.width = self.info.current_w
                    self.height = self.info.current_h
                    self.scale_x =  self.width / 1920
                    self.scale_y =  self.height / 1080
                    self.font_big = pygame.font.Font(
                        None,
                        round(200 * ((self.scale_x + self.scale_y) / 2))
                    )
                    self.font = pygame.font.Font(
                        None,
                        round(150 * ((self.scale_x + self.scale_y) / 2))
                    )
                    self.font_small = pygame.font.Font(
                        None,
                        round(80 * ((self.scale_x + self.scale_y) / 2))
                    )
                    self.font_mini = pygame.font.Font(
                        None,
                        round(65 * ((self.scale_x + self.scale_y) / 2))
                    )
                    self.transparent_background = pygame.Surface(
                        (self.width, self.height),
                        pygame.SRCALPHA
                    )
                    pygame.draw.rect(
                        self.transparent_background,
                        (*BLACK, 150),
                        (0, 0, self.width, self.height)
                    )

            if self.current_challenge.completed:
                # Remove the current challenge after it was completed and get ready for the next one
                self.challenge_message = [
                    1.5,
                    "Challenge completed successfully!",
                    GREEN
                ] if self.current_challenge.successful else \
                [
                    1.5,
                    "Challenge failed :(",
                    RED
                ]
                self.challenge_timer = 0
                if self.current_challenge.successful:
                    self.tictactoe.board[self.wanted_pos[0]][self.wanted_pos[1]] = 1
                self.current_challenge = Challenge(0, [])
                self.has_processed_challenge = False
                self.wanted_pos = (0, 0)
                bot_chosen_pos = self.tictactoe.get_move()
                if bot_chosen_pos and self.tictactoe.is_over(self.tictactoe.board) is False:
                    self.tictactoe.board[bot_chosen_pos[0]][bot_chosen_pos[1]] = 2
                self.can_play = True

            # Draw the backgorund
            pygame.draw.rect(self.screen, BASE, (0, 0, self.width, self.height))

            # Draw the board + symbols
            self.tictactoe.draw_board(self)

            # Draw the statistics text
            wins = self.font_small.render(f"Wins: {self.games_won}", True, SKY)
            losses = self.font_small.render(f"Losses: {self.games_lost}", True, SKY)
            draws = self.font_small.render(f"Draws: {self.games_drawn}", True, SKY)

            self.screen.blit(
                losses,
                (
                    round(20 * self.scale_x),
                    round(20 * self.scale_y)
                )
            )
            self.screen.blit(
                wins,
                (
                    round(20 * self.scale_x),
                    round((30 * self.scale_y + losses.get_size()[1]))
                )
            )
            self.screen.blit(
                draws,
                (
                    round(20 * self.scale_x),
                    round((40 * self.scale_y + losses.get_size()[1]+wins.get_size()[1]))
                )
            )

            # Handle game over states
            message = None
            state = self.tictactoe.is_over(self.tictactoe.board)
            match state:
                case 0 if state is not False:
                    message = "Draw"
                    if not self.is_over:
                        self.games_drawn += 1
                case 1:
                    message = "You won :D"
                    if not self.is_over:
                        self.games_won += 1
                case 2:
                    message = "You lost D:"
                    if not self.is_over:
                        self.games_lost += 1

            # Display the game over and play again messages
            if message is not None:
                self.can_play = False
                self.is_over = True

                text = self.font.render(message, True, YELLOW, PEACH)
                text_rect = text.get_rect()

                text_rect.center = (
                    self.width // 2,
                    self.height // 2
                )

                replay_text = self.font_small.render(
                    "Press R to play again...",
                    True,
                    YELLOW,
                    PEACH
                )
                replay_text_rect = replay_text.get_rect()

                replay_text_rect.center = (
                    self.width // 2,
                    round(self.height * 0.9)
                )

                self.screen.blit(text, text_rect)
                self.screen.blit(replay_text, replay_text_rect)

            # Make it so the player cannot play tic tac toe if a challenge is present
            if self.current_challenge.type != 0:
                self.can_play = False
                if not self.has_processed_challenge:
                    self.challenge_timer = 10

            # Handle each challenge
            match self.current_challenge.type:
                case 1: # Quiz question
                    quiz_question = self.font_mini.render(
                        self.current_challenge.challenge[0], # type: ignore
                        True,
                        WHITE,
                        BLUE
                    )
                    quiz_question_rect = quiz_question.get_rect()

                    self.screen.blit(self.transparent_background, (0, 0))

                    offsets = [(0.5, 0.4), (0.5, 0.5), (0.5, 0.6), (0.5, 0.7)]
                    for n, answer in enumerate(self.current_challenge.challenge[1]):
                        quiz_answer = self.font_mini.render(
                            answer, # type: ignore
                            True,
                            BLACK,
                            CYAN
                        )
                        quiz_answer_rect = quiz_answer.get_rect()

                        quiz_answer_rect.center = (
                            round(self.width * offsets[n][0]),
                            round(self.height * offsets[n][1])
                        )

                        self.screen.blit(quiz_answer, quiz_answer_rect)

                        if not self.has_processed_challenge:
                            self.current_challenge.extra.append((quiz_answer_rect, n))# type: ignore

                    quiz_question_rect.center = (
                        self.width // 2,
                        round(self.height * 0.25)
                    )

                    self.screen.blit(quiz_question, quiz_question_rect)

                    self.has_processed_challenge = True
                case 2: # Target click
                    self.screen.blit(self.transparent_background, (0, 0))

                    instructions_text = self.font_mini.render(
                        "Click all targets",
                        True,
                        WHITE,
                        BLUE
                    )
                    instructions_text_rect = instructions_text.get_rect()

                    instructions_text_rect.center = (
                        round(self.width * 0.5),
                        round(self.height * 0.25)
                    )

                    for target_pos in self.current_challenge.challenge:
                        pygame.draw.circle(
                            self.screen,
                            RED,
                            target_pos,
                            round(50 * ((self.scale_x + self.scale_y) / 2))
                        )
                        pygame.draw.circle(
                            self.screen,
                            WHITE,
                            target_pos,
                            round(35 * ((self.scale_x + self.scale_y) / 2))
                        )
                        pygame.draw.circle(
                            self.screen,
                            RED,
                            target_pos,
                            round(20 * ((self.scale_x + self.scale_y) / 2))
                        )

                    self.screen.blit(instructions_text, instructions_text_rect)

                    self.has_processed_challenge = True
                case 3: # Ordered buttons
                    self.screen.blit(self.transparent_background, (0, 0))

                    instructions_text = self.font_mini.render(
                        "Click in order",
                        True,
                        WHITE,
                        BLUE
                    )
                    instructions_text_rect = instructions_text.get_rect()

                    instructions_text_rect.center = (
                        round(self.width * 0.5),
                        round(self.height * 0.25)
                    )

                    smallest_num = min(
                        self.current_challenge.challenge,
                        key=lambda x: x[1]
                    )[1]
                    for button in self.current_challenge.challenge:
                        pygame.draw.circle(
                            self.screen,
                            MAUVE,
                            button[0],
                            round(50 * ((self.scale_x + self.scale_y) / 2))
                        )
                        pygame.draw.circle(
                            self.screen,
                            BLACK,
                            button[0],
                            round(50 * ((self.scale_x + self.scale_y) / 2)),
                            3
                        )
                        number = self.font_mini.render(
                            str(button[1]+1),
                            True,
                            WHITE if not smallest_num == button[1] else MAROON
                        )
                        number_rect = number.get_rect()

                        number_rect.center = (
                            button[0][0],
                            button[0][1]
                        )

                        self.screen.blit(number, number_rect)
                        self.screen.blit(instructions_text, instructions_text_rect)

                    self.has_processed_challenge = True
                case 4: # Magnets
                    self.screen.blit(self.transparent_background, (0, 0))

                    if self.is_point_in_circle(
                        self.current_challenge.challenge[0],
                        self.current_challenge.challenge[1],
                        round(85 * ((self.scale_x + self.scale_y) / 2))
                    ):
                        self.current_challenge.completed = True
                        self.current_challenge.successful = True

                    pygame.draw.circle(
                        self.screen,
                        RED,
                        self.current_challenge.challenge[0],
                        round(50 * ((self.scale_x + self.scale_y) / 2))
                    )
                    pygame.draw.circle(
                        self.screen,
                        CYAN,
                        self.current_challenge.challenge[1],
                        round(50 * ((self.scale_x + self.scale_y) / 2))
                    )

                    instructions_text = self.font_mini.render(
                        "Make the circles touch",
                        True,
                        WHITE,
                        BLUE
                    )
                    instructions_text_rect = instructions_text.get_rect()

                    instructions_text_rect.center = (
                        round(self.width * 0.5),
                        round(self.height * 0.25)
                    )

                    self.screen.blit(instructions_text, instructions_text_rect)

                    self.has_processed_challenge = True
                case 5: # Word typing
                    if not self.has_processed_challenge:
                        self.current_challenge.extra = [0]

                    self.screen.blit(self.transparent_background, (0, 0))

                    if self.current_challenge.extra[0] \
                        == len(self.current_challenge.challenge):
                        self.current_challenge.completed = True
                        self.current_challenge.successful = True

                    instructions_text = self.font_mini.render(
                        f"Type {"".join(self.current_challenge.challenge)}",
                        True,
                        WHITE,
                        BLUE
                    )
                    instructions_text_rect = instructions_text.get_rect()

                    instructions_text_rect.center = (
                        round(self.width * 0.5),
                        round(self.height * 0.25)
                    )

                    letters_text = self.font.render(
                        "".join(self.current_challenge.challenge[:self.current_challenge.extra[0]]),
                        True,
                        WHITE,
                        RED
                    )
                    letters_text_rect = letters_text.get_rect()

                    letters_text_rect.center = (
                        round(self.width * 0.5),
                        round(self.height * 0.5)
                    )

                    self.screen.blit(letters_text, letters_text_rect)
                    self.screen.blit(instructions_text, instructions_text_rect)

                    self.has_processed_challenge = True

            # Draw the challenge status messages (failed or successful)
            if self.challenge_message[0] > 0:
                challenge_message = self.font_small.render(
                    self.challenge_message[1],
                    True,
                    self.challenge_message[2]
                )
                challenge_message_rect = challenge_message.get_rect()

                challenge_message_rect.center = (
                    self.width // 2,
                    round(self.height * 0.1)
                )

                self.screen.blit(challenge_message, challenge_message_rect)

            # Draw the time left for the challenge
            if self.challenge_timer > 0:
                timer = self.font_mini.render(
                    f"Time left: {round(self.challenge_timer)}s",
                    True,
                    WHITE,
                    RED
                )
                timer_rect = timer.get_rect()

                timer_rect.center = (
                    self.width // 2,
                    round(self.height * 0.1)
                )

                self.screen.blit(timer, timer_rect)

            # Update the window
            pygame.display.flip()

            # Cap framerate
            delta_time = self.clock.tick()

            # Handle the challenge timeouts
            if self.challenge_timer > 0:
                self.challenge_timer -= delta_time / 1000
            elif self.current_challenge.type != 0:
                self.current_challenge.completed = True
                self.current_challenge.successful = False

            # Decrement the challenge status message timer
            if self.challenge_message[0] > 0:
                self.challenge_message[0] -= delta_time / 1000

        pygame.quit()

class TicTacToe:
    """ TicTacToe class for the board and bot """
    def __init__(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

    def is_over(self, board):
        """ Check if the board state is a game over state """
        # Check rows for a winner
        for row in board:
            if row[0] == row[1] == row[2] and row[0] != 0:
                return row[0]

        # Check columns for a winner
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 0:
                return board[0][col]

        # Check diagonals for a winner
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
            return board[0][0]

        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
            return board[0][2]

        # Check if the game is a draw
        if all(all(cell != 0 for cell in row) for row in board):
            return 0

        return False

    def get_move(self):
        """ Get the best move for the bot using a simple system """
        copied_board = self.board.copy()

        player = 1
        bot = 2

        # Check if the bot can win in the next move
        for i in range(3):
            for j in range(3):
                if copied_board[i][j] == 0:
                    copied_board[i][j] = bot
                    if self.is_over(copied_board) == bot:
                        copied_board[i][j] = 0
                        return (i, j)
                    copied_board[i][j] = 0

        # Check if the bot can block the opponent from winning
        for i in range(3):
            for j in range(3):
                if copied_board[i][j] == 0:
                    copied_board[i][j] = player
                    if self.is_over(copied_board) == player:
                        copied_board[i][j] = 0
                        return (i, j)
                    copied_board[i][j] = 0

        # Take the center if available
        if copied_board[1][1] == 0:
            return (1, 1)

        # Take the opposite corner if the opponent is in a corner
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for corner in corners:
            if copied_board[corner[0]][corner[1]] == player:
                opposite_corner = (2 - corner[0], 2 - corner[1])
                if copied_board[opposite_corner[0]][opposite_corner[1]] == 0:
                    return opposite_corner

        # Take any available corner
        available_corners = [
            corner for corner in corners if copied_board[corner[0]][corner[1]] == 0
        ]
        if available_corners:
            return random.choice(available_corners)

        # Take any available side
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        available_sides = [side for side in sides if copied_board[side[0]][side[1]] == 0]
        if available_sides:
            return random.choice(available_sides)

        return False

    def draw_board(self, window: Window):
        """ Draw the board to the screen """
        center_x = window.width // 2
        center_y = window.height // 2

        # Draw background
        pygame.draw.rect(window.screen,
                         BLUE,
                         (
                            round(center_x - 330 * window.scale_x),
                            round(center_y - 330 * window.scale_y),
                            round(660 * window.scale_x),
                            round(660 * window.scale_y)
                         )
        )

        # Vertical lines
        pygame.draw.line(
            window.screen,
            MAUVE,
            (round(center_x - 100 * window.scale_x), round(center_y - 310 * window.scale_y)),
            (round(center_x - 100 * window.scale_x), round(center_y + 310 * window.scale_y)),
            round(15 * ((window.scale_x + window.scale_y) / 2))
        )
        pygame.draw.line(
            window.screen,
            MAUVE,
            (round(center_x + 100 * window.scale_x), round(center_y - 310 * window.scale_y)),
            (round(center_x + 100 * window.scale_x), round(center_y + 310 * window.scale_y)),
            round(15 * ((window.scale_x + window.scale_y) / 2))
        )

        # Horizontal lines
        pygame.draw.line(
            window.screen,
            MAUVE,
            (round(center_x - 310 * window.scale_x), round(center_y - 100 * window.scale_y)),
            (round(center_x + 310 * window.scale_x), round(center_y - 100 * window.scale_y)),
            round(15 * ((window.scale_x + window.scale_y) / 2))
        )
        pygame.draw.line(
            window.screen,
            MAUVE,
            (round(center_x - 310 * window.scale_x), round(center_y + 100 * window.scale_y)),
            (round(center_x + 310 * window.scale_x), round(center_y + 100 * window.scale_y)),
            round(15 * ((window.scale_x + window.scale_y) / 2))
        )

        # Draw symbols
        for row_index, line in enumerate(self.board):
            for col_index, symbol in enumerate(line):
                if symbol != 0:
                    text = window.font_big.render(
                        "X" if symbol == 1 else "O",
                        True,
                        TEAL if symbol == 1 else MAROON
                    )
                    text_rect = text.get_rect()

                    text_rect.center = (
                        round(center_x + (col_index - 1) * (200 * window.scale_x)),
                        round(center_y + (row_index - 1) * (200 * window.scale_y))
                    )

                    window.screen.blit(text, text_rect)

    def get_board_pos(self, pos, window: Window):
        """ Convert window position to board position """
        center_x = window.width // 2
        center_y = window.height // 2
        x, y = pos

        # Check if the position is out of bounds
        if x < center_x - 300 * window.scale_x or x > center_x + 300 * window.scale_x \
            or y < center_y - 300 * window.scale_y or y > center_y + 300 * window.scale_y:
            return None

        # Calculate the column based on x position
        if x < center_x - 100 * window.scale_x:
            col = 0
        elif center_x - 100 * window.scale_x <= x <= center_x + 100 * window.scale_x:
            col = 1
        else:
            col = 2

        # Calculate the row based on y position
        if y < center_y - 100 * window.scale_y:
            row = 0
        elif center_y - 100 * window.scale_y <= y <= center_y + 100 * window.scale_y:
            row = 1
        else:
            row = 2

        return row, col

class Quiz:
    """ Quiz challenge class """
    questions = [
        ["Which of the following is a mutable data type in Python?", [
            "Tuple",
            "String",
            "List",
            "Integer"
        ], 2],
        ["Which programming language is primarily used for web development?", [
            "C++",
            "Python",
            "JavaScript",
            "Java"
        ], 2],
        ["What does 'HTML' stand for?", [
            "Hyper Trainer Marking Language",
            "Hyper Text Marketing Language",
            "Hyper Text Markup Language",
            "Hyper Text Markup Leveler"
        ], 2],
        ["Which keyword is used to create a function in Python?", [
            "func",
            "def",
            "function",
            "define"
        ], 1],
        ["What does CSS stand for?", [
            "Cascading Style Sheets",
            "Computer Style Sheets",
            "Creative Style Sheets",
            "Colorful Style Sheets"
        ], 0],
        ["Which method is used to add an element to the end of a list in Python?", [
            "append()",
            "add()",
            "insert()",
            "push()"
        ], 0],
        ["Which of the following is a Python framework for web development?", [
            "Django",
            "NumPy",
            "React",
            "Laravel"
        ], 0],
        ["What does SQL stand for?", [
            "Structured Query Language",
            "Simple Query Language",
            "Structured Question Language",
            "Simple Question Language"
        ], 0],
        ["Which of these is not a programming language?", [
            "Java",
            "Python",
            "HTML",
            "Swift"
        ], 2],
        ["Which of these sorting algorithms has the best average-case time complexity?", [
            "Bubble Sort",
            "Quick Sort",
            "Selection Sort",
            "Insertion Sort"
        ], 1],
        ["What does 'OOP' stand for in programming?", [
            "Object-Oriented Programming",
            "Operational Object Programming",
            "Object-Oriented Process",
            "Operational Object Process"
        ], 0],
    ]

    @staticmethod
    def get_random_question():
        """ Gets a random question and shuffles the answers """
        random_question = random.choice(Quiz.questions)
        answer = random_question[1][random_question[2]]
        random.shuffle(random_question[1])
        random_question[2] = random_question[1].index(answer)
        return random_question

class Dictionary:
    """ Dictionary class to store words """
    word_list = [
        "apple",
        "lewis",
        "banana",
        "computer",
        "laptop",
        "keyboard",
        "orange",
        "insland",
        "rocket",
        "carrot",
        "rose",
        "mountain",
        "rainbow"
    ]

    @staticmethod
    def get_random_word():
        """ Gets a random word from the dictionary """
        return random.choice(Dictionary.word_list)

class Challenge:
    """ Main challenge class """
    challenges = [1, 2, 3, 4, 5]
    queue = []

    def __init__(self, challenge_type, challenge):
        self.type = challenge_type
        self.challenge = challenge
        self.extra = []
        self.completed = False
        self.successful = False

    @staticmethod
    def get_challenge(window: Window):
        """ Give a random challenge to the player """
        if not Challenge.queue:
            new_challenges = Challenge.challenges.copy()
            random.shuffle(new_challenges)
            Challenge.queue = new_challenges
        random_num = Challenge.queue.pop(0)
        match random_num:
            case 1:
                window.current_challenge = Challenge(1, Quiz.get_random_question())
            case 2:
                target_positions = [
                    (
                        random.randint(round(0.15 * window.width), round(0.85 * window.width) - 1),
                        random.randint(round(0.15 * window.height), round(0.85 * window.height) - 1)
                    ) for _ in range(7)
                ]
                window.current_challenge = Challenge(2, target_positions)
            case 3:
                number_positions = [
                    ((
                        random.randint(round(0.15 * window.width), round(0.85 * window.width) - 1),
                        random.randint(round(0.15 * window.height), round(0.85 * window.height) - 1)
                    ), n) for n in range(5)
                ]
                window.current_challenge = Challenge(3, number_positions)
            case 4:
                x_pos = (
                    random.randint(round(0.15 * window.width), round(0.85 * window.width) - 1),
                    random.randint(round(0.15 * window.height), round(0.85 * window.height) - 1)
                )
                box_pos = (
                    random.randint(round(0.15 * window.width), round(0.85 * window.width) - 1),
                    random.randint(round(0.15 * window.height), round(0.85 * window.height) - 1)
                )
                window.current_challenge = Challenge(4, [x_pos, box_pos, False])
            case 5:
                window.current_challenge = Challenge(5, Dictionary.get_random_word())

if __name__ == "__main__":
    game_window = Window()
    game_window.run()
