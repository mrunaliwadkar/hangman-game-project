import tkinter as tk
import random

# Hangman stages (ASCII art)
hangman_stages = [
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
"""
]

# List of words
words = ["python", "hangman", "game", "computer", "programming", "developer", "software", "algorithm", "function", "variable"]

# Hints for each word
word_hints = {
    "python": "A popular programming language",
    "hangman": "A word-guessing game",
    "game": "A form of entertainment",
    "computer": "An electronic device for processing data",
    "programming": "Writing code",
    "developer": "A software creator",
    "software": "Programs and applications",
    "algorithm": "Step-by-step procedure",
    "function": "A block of reusable code",
    "variable": "A container for storing data"
}

# Global variables for game state
word = ""
guessed = set()
wrong = 0
display = []
hints_used = 0
max_hints = 2
root = None
word_label = None
guess_entry = None
guess_button = None
feedback_label = None
hangman_label = None
guessed_label = None
hint_button = None
hint_label = None
restart_button = None


def init_game():
    global word, guessed, wrong, display, hints_used
    word = random.choice(words).lower()
    guessed = set()
    wrong = 0
    hints_used = 0
    display = ['_'] * len(word)

def update_display():
    word_label.config(text=' '.join(display))
    guessed_label.config(text=f"Guessed letters: {' '.join(sorted(guessed))}")
    hangman_label.config(text=hangman_stages[wrong])
    hint_label.config(text=f"Hints remaining: {max_hints - hints_used}")

def guess():
    global wrong
    letter = guess_entry.get().lower().strip()
    guess_entry.delete(0, tk.END)

    if not letter or len(letter) != 1 or not letter.isalpha():
        feedback_label.config(text="Please enter a single letter!")
        return

    if letter in guessed:
        feedback_label.config(text="Already guessed!")
        return

    guessed.add(letter)

    if letter in word:
        for i, l in enumerate(word):
            if l == letter:
                display[i] = letter
        feedback_label.config(text="Correct!")
        if '_' not in display:
            feedback_label.config(text="You win!")
            guess_button.config(state=tk.DISABLED)
    else:
        wrong += 1
        feedback_label.config(text="Incorrect!")
        if wrong == 6:
            feedback_label.config(text=f"You lose! The word was '{word}'")
            guess_button.config(state=tk.DISABLED)

    update_display()

def use_hint():
    global hints_used
    if hints_used >= max_hints:
        feedback_label.config(text="No more hints available!", fg='red')
        return
    
    if word in word_hints:
        feedback_label.config(text=f"Hint: {word_hints[word]}", fg='darkblue')
        hints_used += 1
        hint_button.config(state=tk.DISABLED if hints_used >= max_hints else tk.NORMAL)
        update_display()

def restart_game():
    global word, guessed, wrong, display, hints_used, guess_button, hint_button
    init_game()
    guess_button.config(state=tk.NORMAL)
    hint_button.config(state=tk.NORMAL)
    update_display()
    feedback_label.config(text="New game started!", fg='green')
    guess_entry.focus()

def main():
    global root, word_label, guess_entry, guess_button, feedback_label, hangman_label, guessed_label, hint_button, hint_label
    init_game()

    # GUI setup
    root = tk.Tk()
    root.title("Hangman Game")
    root.geometry("650x800")
    root.config(bg='#E8F4F8')  # Light blue background
    root.resizable(False, False)

    # Title
    title_label = tk.Label(root, text="🎯 HANGMAN GAME 🎯", font=('Helvetica', 32, 'bold'), 
                           bg='#E8F4F8', fg='#2E4057')
    title_label.pack(pady=20)

    # Separator
    separator1 = tk.Frame(root, height=3, bg='#3498DB')
    separator1.pack(fill=tk.X, padx=30)

    # Hangman display
    hangman_frame = tk.Frame(root, bg='#FFFFFF', relief='ridge', bd=2)
    hangman_frame.pack(pady=20, padx=20)
    hangman_label = tk.Label(hangman_frame, text=hangman_stages[0], font=('Courier', 12, 'bold'), 
                            justify=tk.LEFT, bg='#FFFFFF', fg='#2C3E50')
    hangman_label.pack(padx=10, pady=10)

    # Separator
    separator2 = tk.Frame(root, height=3, bg='#3498DB')
    separator2.pack(fill=tk.X, padx=30)

    # Word display
    word_label = tk.Label(root, text=' '.join(display), font=('Helvetica', 36, 'bold'), 
                         bg='#E8F4F8', fg='#E74C3C')
    word_label.pack(pady=25)

    # Guess input
    guess_frame = tk.Frame(root, bg='#FFFFFF', relief='groove', bd=2)
    guess_frame.pack(pady=20, padx=20)
    tk.Label(guess_frame, text="Enter a letter:", font=('Helvetica', 14, 'bold'), 
            bg='#FFFFFF', fg='#2E4057').pack(side=tk.LEFT, padx=15, pady=10)
    guess_entry = tk.Entry(guess_frame, width=10, font=('Helvetica', 16), 
                          bg='#F8F9FA', fg='#2C3E50', relief='sunken', bd=2)
    guess_entry.pack(side=tk.LEFT, padx=10, pady=10)
    guess_button = tk.Button(guess_frame, text="Guess", command=guess, 
                            bg='#28A745', fg='white', font=('Helvetica', 12, 'bold'),
                            padx=20, pady=8, cursor='hand2', relief='raised', bd=3)
    guess_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Feedback
    feedback_label = tk.Label(root, text="", font=('Helvetica', 14, 'bold'), 
                             bg='#E8F4F8', fg='#FF6B35', wraplength=600)
    feedback_label.pack(pady=15)

    # Guessed letters
    guessed_label = tk.Label(root, text="Guessed letters: ", font=('Helvetica', 12), 
                            bg='#E8F4F8', fg='#6C757D', wraplength=600)
    guessed_label.pack(pady=10)

    # Separator
    separator3 = tk.Frame(root, height=3, bg='#3498DB')
    separator3.pack(fill=tk.X, padx=30, pady=10)

    # Buttons
    button_frame = tk.Frame(root, bg='#E8F4F8')
    button_frame.pack(pady=20)
    
    hint_button = tk.Button(button_frame, text="💡 Get Hint", command=use_hint, 
                           bg='#FFC107', fg='#2E4057', font=('Helvetica', 12, 'bold'),
                           padx=15, pady=8, cursor='hand2', relief='raised', bd=3)
    hint_button.pack(side=tk.LEFT, padx=10)
    
    hint_label = tk.Label(button_frame, text=f"Hints: {max_hints - hints_used}", 
                         font=('Helvetica', 12, 'bold'), bg='#E8F4F8', fg='#2E4057')
    hint_label.pack(side=tk.LEFT, padx=10)
    
    restart_button = tk.Button(button_frame, text="🔄 Restart", command=restart_game, 
                              bg='#DC3545', fg='white', font=('Helvetica', 12, 'bold'),
                              padx=15, pady=8, cursor='hand2', relief='raised', bd=3)
    restart_button.pack(side=tk.LEFT, padx=10)

    guess_entry.focus()
    root.mainloop()

if __name__ == "__main__":
    main()
