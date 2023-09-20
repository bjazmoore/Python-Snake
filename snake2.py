import tkinter as tk
from random import randint

class SnakeGame:
    def __init__(self, master):
        self.direction = 'D'  # Let's start by moving right
        self.speed_text_id = None
        self.starting_speed = 400 # Initial speed
        self.speed = self.starting_speed


        self.master = master
        self.master.title('Snake Game')

        self.score = 0
        self.cell_size = 20
        self.width = 20
        self.height = 20

        self.canvas = tk.Canvas(self.master, width=self.width * self.cell_size, height=self.height * self.cell_size)
        self.canvas.pack()

        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.food = self.generate_food()

        self.canvas.bind("<Key>", self.key_press)
        self.canvas.focus_set()

        self.play_again_text_id = None
        self.start_text_id = None
        self.game_started = False
        self.display_start_message()

        #self.draw()
        #self.move_snake()

    def draw(self):
        self.canvas.delete(tk.ALL)

        # Draw snake
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                         x * self.cell_size + self.cell_size, y * self.cell_size + self.cell_size,
                                         fill='green')

        # Draw food
        x, y = self.food
        self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                     x * self.cell_size + self.cell_size, y * self.cell_size + self.cell_size,
                                     fill='red')

        # Display score
        self.canvas.create_text(10, 10, anchor=tk.NW, text=f"Score: {self.score}", font=("Arial", 14), fill="black")

        # Delete previous speed text
        if self.speed_text_id:
            self.canvas.delete(self.speed_text_id)

        # Display the snake speed
        snake_speed = 450 - self.speed
        self.speed_text_id = self.canvas.create_text(self.width * self.cell_size - 10, 10, anchor="ne",
                                            text=f"Speed: {snake_speed}", font=("Arial", 14), fill="black")



    def key_press(self, event):
        new_direction = event.keysym.upper()  # Convert to uppercase

        if not self.game_started:
            if new_direction == 'SPACE':
                if self.play_again_text_id:
                    self.canvas.delete(self.play_again_text_id)
                if self.start_text_id:
                    self.canvas.delete(self.start_text_id)
                self.reset_game()
                self.move_snake()
                return

        # Check if the key pressed is one of the allowed keys
        if new_direction not in ['W', 'S', 'A', 'D']:
            return  # Exit without making any changes

        if self.direction == 'W' and new_direction != 'S':
            self.direction = new_direction
        elif self.direction == 'S' and new_direction != 'W':
            self.direction = new_direction
        elif self.direction == 'A' and new_direction != 'D':
            self.direction = new_direction
        elif self.direction == 'D' and new_direction != 'A':
            self.direction = new_direction

    def move_based_on_direction(self):
        last_move = self.snake[-1]
        #print(f"moving: self.snake[-1]= {self.snake[-1]}, self.direction= {self.direction}, self.snake= {self.snake}")
        new_head = last_move
        if self.direction == 'W':
            new_head = (last_move[0], last_move[1] - 1)
        elif self.direction == 'S':
            new_head = (last_move[0], last_move[1] + 1)
        elif self.direction == 'A':
            new_head = (last_move[0] - 1, last_move[1])
        elif self.direction == 'D':
            new_head = (last_move[0] + 1, last_move[1])


        self.snake.append(new_head)
        # Remove the tail if not eating food
        # Check if the snake has eaten the food
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop(0)

        #print(f"moved: self.snake= {self.snake}")

    def generate_food(self):
        while True:
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def move_snake(self):
        if len(self.snake) == 0:  # Check if the snake has any segments left - this should never be an issue
            return

        self.move_based_on_direction()

        head = self.snake[-1]
        x, y = head

        #print(f"x= {x}, y= {y}, self.snake[:-1]= {self.snake[:-1]}, self.snake= {self.snake}")
        if (x < 0 or x >= self.width or y < 0 or y >= self.height or
            head in self.snake[:-1]):
            self.end_game()
            return

        self.draw()
        self.speed = max(50, int(self.starting_speed * (0.95 ** self.score)))
        print (f"speed = {self.speed}")
        self.master.after(self.speed, self.move_snake)

    def end_game(self):
        self.canvas.delete(tk.ALL)
        self.play_again_text_id = self.canvas.create_text(self.width * self.cell_size / 2,
                                                          self.height * self.cell_size / 2,
                                                          text=f"Game Over\nScore: {self.score}\nPress Space to Play Again",
                                                          font=("Arial", 14), fill="black")
        self.game_started = False

    def display_start_message(self):
        self.start_text_id = self.canvas.create_text(self.width * self.cell_size / 2,
                                                     self.height * self.cell_size / 2,
                                                     text="Press Space to Begin", font=("Arial", 16),fill="red")

    def reset_game(self):
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.direction = 'W'
        self.food = self.generate_food()
        self.score = 0
        self.speed = self.starting_speed
        self.game_started = True
        if self.play_again_text_id:
            self.canvas.delete(self.play_again_text_id)
        self.draw()
        self.move_snake()


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
