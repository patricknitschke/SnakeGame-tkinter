import random
import numpy as np

import tkinter as tk
from PIL import Image, ImageTk

MOVE_INCREMENT = 20
MOVES_PER_SECOND = 10
GAME_SPEED = 1000 // MOVES_PER_SECOND


class SnakeGUI(tk.Canvas): # inherit from canvas superclass
    width: int
    height: int
    score: int
    direction: str
    direction_vector: np.ndarray # (1,2)
    snake_positions: np.ndarray # (n,2), n = size of snake
    food_position: np.ndarray # (1,2)

    def __init__(self):
        self.width = 30 
        self.height = 20 
        super().__init__(  # Superclass constructor
            width=self.width*MOVE_INCREMENT, height=self.height*MOVE_INCREMENT, background="black", highlightthickness=0
        )
        self.load_assets()

        self.snake_positions = np.vstack(
            (np.array([5,5]) * MOVE_INCREMENT, np.array([4,5]) * MOVE_INCREMENT) # TODO load position
        ) 
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.direction = "Right"
        self.direction_vector = np.array([MOVE_INCREMENT,0])
        self.bind_all("<Key>", self.on_key_press)
        self.load_assets()
        self.create_objects()

        self.after(GAME_SPEED, self.perform_actions)

    def load_assets(self):
        '''
        Loads pictures for the snake body and food.
        '''
        try:
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)
            self.food_body_image = Image.open("./assets/food.png")
            self.food_body = ImageTk.PhotoImage(self.food_body_image)
        except IOError as error:
            print(error)
            window.destroy()

    def create_objects(self):
        '''
        Creates all the objects and text boxes.
        '''
        # Create text box, takes 20 spaces-ish vertically
        self.create_text(
            40, 12, text=f"Score: {self.score}", tag="score", fill="white", font=("TkDefaultFont", 14)
        )
        self.create_text(
            140, 12, text=f"Direction: {self.direction}", tag="direction", fill="white", font=("TkDefaultFont", 14)
        )
        # Create objects
        for position in self.snake_positions:
            self.create_image(*position, image=self.snake_body, tag="snake") 
        self.create_image(*self.food_position, image=self.food_body, tag="food")
        self.create_rectangle(7, 27, self.width*MOVE_INCREMENT-7, self.height*MOVE_INCREMENT-7, outline="#525d69")

    def move_snake(self):
        '''
        Update the snake position according to the direction vector.
        '''
        new_head = self.snake_positions[0] + self.direction_vector
        self.snake_positions = np.vstack((new_head, self.snake_positions[:-1]))

        # Move segments to new positions
        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, (*position)) # move, (*ndarray) = unpack np array into tuple

    def perform_actions(self):
        if self.check_collisions():
            return
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)
    
    def check_collisions(self):
        head = self.snake_positions[0]
        body_collision = True in [np.array_equal(head, position) for position in self.snake_positions[1:]]
        return (
            head[0] in (0, self.width*MOVE_INCREMENT) 
            or head[1] in (20, self.height*MOVE_INCREMENT)
            or body_collision
            )

    def on_key_press(self, e):
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposite_directions = ({"Up", "Down"}, {"Left", "Right"}) # set of opposites
        
        # Check new direction allowed
        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposite_directions # use sets to check new dir not opposite
        ):
            self.direction = new_direction

            # Set new direction vector
            self.direction_vector = np.zeros(2)
            if self.direction == "Right":
                self.direction_vector[0] = MOVE_INCREMENT
            elif self.direction == "Left":
                self.direction_vector[0] = -MOVE_INCREMENT
            elif self.direction == "Up":
                self.direction_vector[1] = -MOVE_INCREMENT
            else:
                self.direction_vector[1] = MOVE_INCREMENT

            # Update direction in GUI
            direction_item = self.find_withtag("direction")
            self.itemconfigure(direction_item, text=f"Direction: {self.direction}", tag="direction")

    def check_food_collision(self):
        if np.array_equal(self.snake_positions[0], self.food_position):
            self.score += 1
            self.snake_positions = np.vstack((self.snake_positions, self.snake_positions[-1]))
            
            # Update snake body instantly
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag="snake") 

            # New food position
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), (*self.food_position)) # move, * = unpack position into tuple
            
            # Update score in GUI
            score_item = self.find_withtag("score")
            self.itemconfigure(score_item, text=f"Score: {self.score}", tag="score")
    
    def set_new_food_position(self):
        while True:
            food_x = random.randint(1, self.width - 1) * MOVE_INCREMENT
            food_y = random.randint(3, self.height - 1) * MOVE_INCREMENT
            food_pos = np.array([food_x, food_y])

            if not True in [np.array_equal(food_pos, position) for position in self.snake_positions]:
                return food_pos

        





# Create window
window = tk.Tk()
window.title("TDT4173 Project: Snake Game")
window.resizable(False, False)

# Create and put snake game into window
board = SnakeGUI()
board.pack()

# Run the window
window.mainloop()