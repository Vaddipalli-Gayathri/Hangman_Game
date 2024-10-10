import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame

# Initialize pygame mixer for sound effectsr
pygame.mixer.init()

# Load sound effects
correct_sound = pygame.mixer.Sound(r"C:\Users\dell\Desktop\project\correct.wav")  # Replace with your correct guess sound file
wrong_sound = pygame.mixer.Sound(r"C:\Users\dell\Desktop\project\wrong.wav")      # Replace with your wrong guess sound file
win_sound = pygame.mixer.Sound(r"C:\Users\dell\Desktop\project\win.wav")          # Replace with your win sound file
lose_sound = pygame.mixer.Sound(r"C:\Users\dell\Desktop\project\lose.wav")        # Replace with your lose sound file

# List of words for the game
words = ["apple", "banana", "grape", "orange", "strawberry", "watermelon"]

# Function to start a new game
def start_new_game():
    global word_to_guess, guessed_word, guessed_letters, incorrect_guesses, max_incorrect_guesses
    word_to_guess = random.choice(words)
    guessed_word = ['_'] * len(word_to_guess)
    guessed_letters = []
    incorrect_guesses = 0
    max_incorrect_guesses = 6
    update_display()
    result_label.config(text="")
    input_entry.config(state="normal")
    guess_button.config(state="normal")

# Function to update the display (guessed word and guessed letters)
def update_display():
    word_display.config(text=" ".join(guessed_word))
    guessed_letters_display.config(text="Guessed Letters: " + ", ".join(guessed_letters))
    remaining_guesses_display.config(text=f"Remaining incorrect guesses: {max_incorrect_guesses - incorrect_guesses}")

# Function to check a guessed letter
def guess_letter():
    global incorrect_guesses
    guess = input_entry.get().lower()
    input_entry.delete(0, tk.END)
    
    if len(guess) != 1 or not guess.isalpha():
        result_label.config(text="Please enter a single valid letter.")
        return
    
    if guess in guessed_letters:
        result_label.config(text="You've already guessed that letter!")
        return

    guessed_letters.append(guess)

    if guess in word_to_guess:
        for i, letter in enumerate(word_to_guess):
            if letter == guess:
                guessed_word[i] = guess
        result_label.config(text="Good guess!")
        pygame.mixer.Sound.play(correct_sound)  # Play correct guess sound
    else:
        incorrect_guesses += 1
        result_label.config(text="Wrong guess!")
        pygame.mixer.Sound.play(wrong_sound)  # Play wrong guess sound
    
    update_display()
    check_game_over()

# Function to check if the game is over (win or lose)
def check_game_over():
    if '_' not in guessed_word:
        result_label.config(text="Congratulations! You've guessed the word!", fg="green")
        pygame.mixer.Sound.play(win_sound)  # Play win sound
        input_entry.config(state="disabled")
        guess_button.config(state="disabled")
    elif incorrect_guesses >= max_incorrect_guesses:
        result_label.config(text=f"You've run out of guesses! The word was: {word_to_guess}", fg="red")
        pygame.mixer.Sound.play(lose_sound)  # Play lose sound
        input_entry.config(state="disabled")
        guess_button.config(state="disabled")

# Create the main window
root = tk.Tk()
root.title("Hangman Game")

# Load and set the background image
bg_image = Image.open("background.jpg")  # Replace with the path to your image
bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas to hold the background image
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Word display label
word_display = tk.Label(root, text="Word to guess: ", font=("Helvetica", 24), bg="#ffffff", borderwidth=0)
canvas.create_window(400, 100, window=word_display)

# Guessed letters display label
guessed_letters_display = tk.Label(root, text="Guessed Letters: ", font=("Helvetica", 16), bg="#ffffff", borderwidth=0)
canvas.create_window(400, 180, window=guessed_letters_display)

# Remaining guesses display label
remaining_guesses_display = tk.Label(root, text="Remaining incorrect guesses: 6", font=("Helvetica", 16), bg="#ffffff", borderwidth=0)
canvas.create_window(400, 220, window=remaining_guesses_display)

# Input field for guesses
input_entry = tk.Entry(root, font=("Helvetica", 16), width=5)
canvas.create_window(400, 280, window=input_entry)

# Button to submit guesses
guess_button = tk.Button(root, text="Guess", font=("Helvetica", 16), command=guess_letter)
canvas.create_window(400, 340, window=guess_button)

# Result label to show feedback
result_label = tk.Label(root, text="", font=("Helvetica", 16), bg="#ffffff", borderwidth=0)
canvas.create_window(400, 400, window=result_label)

# Button to start a new game
new_game_button = tk.Button(root, text="Start New Game", font=("Helvetica", 16), command=start_new_game)
canvas.create_window(400, 460, window=new_game_button)

# Start the game
start_new_game()

# Run the application
root.mainloop()