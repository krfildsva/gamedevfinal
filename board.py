import random
import pygame
from settings import CARD_SIZE, GAP, MARGIN

class Card:
    def __init__(self, value, row, col):
        self.value = value            # A string like "apple", etc.
        self.revealed = False
        self.matched = False
        self.row = row
        self.col = col
        self.x = MARGIN + col * (CARD_SIZE + GAP)
        self.y = MARGIN + row * (CARD_SIZE + GAP)
        self.flip_progress = 0  # 0 (back) → 1 (front)

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cards = []
        self.revealed_cards = []
        self.score = 0  # Score increases only on a successful match.
        self.generate_board()

    def generate_board(self):
        num_cards = self.rows * self.cols
        if num_cards % 2 != 0:
            raise ValueError("Board size must be even to pair cards!")
        num_pairs = num_cards // 2
        available_images = [
            "apple", "avacado", "cherry", "cow", "crocodile", "deer",
            "dragon-fruit", "fox", "hippo", "mango", "meerkat", "strawberry",
            "tiger", "watermelon"
        ]
        if num_pairs > len(available_images):
            raise ValueError("Not enough images available for this board size!")
        # Randomly choose the required number of images, duplicate, and shuffle.
        chosen_images = random.sample(available_images, num_pairs)
        values = chosen_images * 2
        random.shuffle(values)
        self.cards = [
            [Card(values.pop(), r, c) for c in range(self.cols)]
            for r in range(self.rows)
        ]

    def handle_click(self, mx, my, flipping_cards, assets):
        # Prevent clicking if two cards are already revealed.
        if len(self.revealed_cards) >= 2:
            return

        for row in self.cards:
            for card in row:
                if card.x <= mx <= card.x + CARD_SIZE and card.y <= my <= card.y + CARD_SIZE:
                    if not card.revealed and not card.matched:
                        card.revealed = True
                        self.revealed_cards.append(card)
                        flipping_cards[(card.row, card.col)] = 0  # Start flip animation

                        if len(self.revealed_cards) == 2:
                            pygame.time.set_timer(pygame.USEREVENT, 700)

                        if assets["sounds"].get("flip"):
                            assets["sounds"]["flip"].play()

    def check_match(self, assets):
        if len(self.revealed_cards) == 2:
            card1, card2 = self.revealed_cards
            if card1.value == card2.value:
                card1.matched = card2.matched = True
                self.score += 1  # Increase score only on a match.
                if assets["sounds"].get("match"):
                    assets["sounds"]["match"].play()
            else:
                card1.revealed = card2.revealed = False
            self.revealed_cards.clear()

    def check_win(self):
        return all(card.matched for row in self.cards for card in row)
