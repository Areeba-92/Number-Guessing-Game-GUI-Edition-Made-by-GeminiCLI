
import random
import json
import time
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class NumberGuessingGame:
    def __init__(self):
        self.leaderboard_file = "leaderboard.txt"
        self.easy_range = (1, 50)
        self.medium_range = (1, 100)
        self.hard_range = (1, 200)
        self.themes = {
            "light": {"bg": "#f0f0f0", "fg": "#333", "button_bg": "#4CAF50", "button_fg": "white", "button_hover": "#45a049", "radio_bg": "#f0f0f0", "radio_fg": "#333", "radio_select": "#f0f0f0"},
            "dark": {"bg": "#333", "fg": "white", "button_bg": "#555", "button_fg": "white", "button_hover": "#444", "radio_bg": "#333", "radio_fg": "white", "radio_select": "#333"},
            "neutral": {"bg": "#e0e0e0", "fg": "#333", "button_bg": "#9e9e9e", "button_fg": "white", "button_hover": "#8e8e8e", "radio_bg": "#e0e0e0", "radio_fg": "#333", "radio_select": "#e0e0e0"},
            "neon": {"bg": "#000", "fg": "#00ff00", "button_bg": "#00ff00", "button_fg": "#000", "button_hover": "#00dd00", "radio_bg": "#000", "radio_fg": "#00ff00", "radio_select": "#000"}
        }
        self.current_theme = "light"

    def set_difficulty(self, difficulty):
        if difficulty == "easy":
            return self.easy_range, 10
        elif difficulty == "medium":
            return self.medium_range, 7
        elif difficulty == "hard":
            return self.hard_range, 5
        else:
            return self.medium_range, 7

    def get_hint(self, secret_number, attempts_left):
        if attempts_left <= 3:
            if secret_number % 2 == 0:
                return "Hint: The number is even."
            else:
                return "Hint: The number is odd."
        return ""

    def play_round(self, difficulty):
        pass

    def adjust_range(self, difficulty, win):
        if difficulty == "easy":
            (min_range, max_range) = self.easy_range
            if win:
                self.easy_range = (min_range, max_range + 20)
            else:
                self.easy_range = (min_range, max(50, max_range - 20))
        elif difficulty == "medium":
            (min_range, max_range) = self.medium_range
            if win:
                self.medium_range = (min_range, max_range + 20)
            else:
                self.medium_range = (min_range, max(100, max_range - 20))
        elif difficulty == "hard":
            (min_range, max_range) = self.hard_range
            if win:
                self.hard_range = (min_range, max_range + 20)
            else:
                self.hard_range = (min_range, max(200, max_range - 20))

    def calculate_score(self, attempts, time_taken, difficulty):
        difficulty_multiplier = {"easy": 1, "medium": 1.5, "hard": 2}
        return int((100 - attempts * 5) * difficulty_multiplier[difficulty] / (time_taken + 1))

    def show_leaderboard(self):
        try:
            with open(self.leaderboard_file, "r") as f:
                leaderboard = json.load(f)
            
            print("--- Leaderboard ---")
            print("Rank | Name        | Score | Attempts | Time (s) | Difficulty")
            print("----------------------------------------------------------------")
            for i, entry in enumerate(leaderboard[:5]):
                print(f"{i+1:<4} | {entry['name']:<11} | {entry['score']:<5} | {entry['attempts']:<8} | {entry['time_taken']:<8.2f} | {entry['difficulty'].capitalize():<10}")
        except (FileNotFoundError, json.JSONDecodeError):
            print("Leaderboard is empty.")

    def update_leaderboard(self, name, score, attempts, time_taken, difficulty):
        try:
            with open(self.leaderboard_file, "r") as f:
                leaderboard = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            leaderboard = []

        entry = {
            "name": name,
            "score": score,
            "attempts": attempts,
            "time_taken": round(time_taken, 2),
            "difficulty": difficulty
        }
        leaderboard.append(entry)
        leaderboard.sort(key=lambda x: x["score"], reverse=True)

        with open(self.leaderboard_file, "w") as f:
            json.dump(leaderboard, f, indent=4)

    def show_instructions(self):
        print('''
        --- Number Guessing Game Instructions ---
        1. Choose a difficulty level: easy, medium, or hard.
        2. Guess the randomly generated number within the given range.
        3. You have a limited number of attempts based on the difficulty.
        4. Hints will be provided in the last few attempts.
        5. Your score is based on attempts, time, and difficulty.
        6. Try to get a high score and make it to the leaderboard!
        ''')

    def save_game(self, secret_number, attempts, attempts_limit, difficulty, start_time):
        game_state = {
            "secret_number": secret_number,
            "attempts": attempts,
            "attempts_limit": attempts_limit,
            "difficulty": difficulty,
            "start_time": start_time
        }
        with open("savegame.json", "w") as f:
            json.dump(game_state, f)
        

    def load_game(self):
        try:
            with open("savegame.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

class GameGUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Number Guessing Game")
        self.geometry("400x400")
        self.attributes("-alpha", 0.0)
        self.username = ""
        self.create_welcome_frame()
        self.fade_in()

    def show_personalized_welcome(self):
        self.username = self.name_entry.get()
        if not self.username:
            messagebox.showerror("Error", "Please enter your name.")
            return

        self.welcome_frame.destroy()
        theme = self.game.themes[self.game.current_theme]
        self.personalized_frame = tk.Frame(self, bg=theme["bg"])
        self.slide_in(self.personalized_frame)

        tk.Label(self.personalized_frame, text=f"Welcome, {self.username}!", font=("Arial", 24, "bold"), bg=theme["bg"], fg=theme["fg"]).pack(pady=40)

        start_button = tk.Button(self.personalized_frame, text="Start Game", command=self.create_widgets, font=("Arial", 12), bg=theme["button_bg"], fg=theme["button_fg"], pady=10, padx=20, relief="raised")
        start_button.pack(pady=20)
        start_button.bind("<Enter>", self.on_enter_main)
        start_button.bind("<Leave>", self.on_leave_main)
        start_button.bind("<Button-1>", self.on_press)
        start_button.bind("<ButtonRelease-1>", self.on_release)

    def create_welcome_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_menu()
        theme = self.game.themes[self.game.current_theme]
        self.welcome_frame = tk.Frame(self, bg=theme["bg"])
        self.slide_in(self.welcome_frame)

        tk.Label(self.welcome_frame, text="Welcome to the Number Guessing Game!", font=("Arial", 18, "bold"), bg=theme["bg"], fg=theme["fg"]).pack(pady=20)
        tk.Label(self.welcome_frame, text="Please enter your name:", font=("Arial", 12), bg=theme["bg"], fg=theme["fg"]).pack(pady=10)

        self.name_entry = tk.Entry(self.welcome_frame, font=("Arial", 14))
        self.name_entry.pack(pady=5)

        continue_button = tk.Button(self.welcome_frame, text="Continue", command=self.show_personalized_welcome, font=("Arial", 12), bg=theme["button_bg"], fg=theme["button_fg"], pady=10, padx=20, relief="raised")
        continue_button.pack(pady=20)
        continue_button.bind("<Enter>", self.on_enter_main)
        continue_button.bind("<Leave>", self.on_leave_main)
        continue_button.bind("<Button-1>", self.on_press)
        continue_button.bind("<ButtonRelease-1>", self.on_release)

    def slide_in(self, widget):
        widget.place(relx=1.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
        x = 1.5
        def animate():
            nonlocal x
            if x > 0.5:
                x -= 0.05
                widget.place(relx=x, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
                self.after(10, animate)
        animate()

    def fade_in_widget(self, widget):
        widget.attributes("-alpha", 0.0)
        alpha = 0.0
        def animate():
            nonlocal alpha
            if alpha < 1.0:
                alpha += 0.1
                widget.attributes("-alpha", alpha)
                self.after(50, animate)
        animate()

    def fade_in(self):
        alpha = self.attributes("-alpha")
        if alpha < 1.0:
            alpha += 0.1
            self.attributes("-alpha", alpha)
            self.after(50, self.fade_in)

    def create_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_menu()
        theme = self.game.themes[self.game.current_theme]
        self.main_frame = tk.Frame(self, bg=theme["bg"])
        self.slide_in(self.main_frame)

        tk.Label(self.main_frame, text="Number Guessing Game", font=("Arial", 24, "bold"), bg=theme["bg"], fg=theme["fg"]).pack(pady=10)

        button_style = {"font": ("Arial", 12), "bg": theme["button_bg"], "fg": theme["button_fg"], "pady": 10, "padx": 20, "width": 20, "relief": "raised"}

        start_button = tk.Button(self.main_frame, text="Start Game", command=self.start_game, **button_style)
        start_button.pack(pady=5)
        start_button.bind("<Enter>", self.on_enter_main)
        start_button.bind("<Leave>", self.on_leave_main)
        start_button.bind("<Button-1>", self.on_press)
        start_button.bind("<ButtonRelease-1>", self.on_release)

        load_button = tk.Button(self.main_frame, text="Load Game", command=self.load_game, **button_style)
        load_button.pack(pady=5)
        load_button.bind("<Enter>", self.on_enter_main)
        load_button.bind("<Leave>", self.on_leave_main)
        load_button.bind("<Button-1>", self.on_press)
        load_button.bind("<ButtonRelease-1>", self.on_release)

        ai_button = tk.Button(self.main_frame, text="AI Opponent Mode", command=self.start_ai_game, **button_style)
        ai_button.pack(pady=5)
        ai_button.bind("<Enter>", self.on_enter_main)
        ai_button.bind("<Leave>", self.on_leave_main)
        ai_button.bind("<Button-1>", self.on_press)
        ai_button.bind("<ButtonRelease-1>", self.on_release)

        leaderboard_button = tk.Button(self.main_frame, text="Show Leaderboard", command=self.show_leaderboard, **button_style)
        leaderboard_button.pack(pady=5)
        leaderboard_button.bind("<Enter>", self.on_enter_main)
        leaderboard_button.bind("<Leave>", self.on_leave_main)
        leaderboard_button.bind("<Button-1>", self.on_press)
        leaderboard_button.bind("<ButtonRelease-1>", self.on_release)

        instructions_button = tk.Button(self.main_frame, text="Instructions", command=self.show_instructions, **button_style)
        instructions_button.pack(pady=5)
        instructions_button.bind("<Enter>", self.on_enter_main)
        instructions_button.bind("<Leave>", self.on_leave_main)
        instructions_button.bind("<Button-1>", self.on_press)
        instructions_button.bind("<ButtonRelease-1>", self.on_release)

        exit_button = tk.Button(self.main_frame, text="Exit", command=self.quit, **button_style)
        exit_button.pack(pady=5)
        exit_button.bind("<Enter>", self.on_enter_main)
        exit_button.bind("<Leave>", self.on_leave_main)
        exit_button.bind("<Button-1>", self.on_press)
        exit_button.bind("<ButtonRelease-1>", self.on_release)

        tk.Label(self.main_frame, text="Change themes in the menu!", font=("Arial", 10, "italic"), bg=theme["bg"], fg=theme["fg"]).pack(pady=20)

    def on_press(self, event):
        event.widget.config(relief="sunken")

    def on_release(self, event):
        event.widget.config(relief="raised")

    def on_enter_main(self, event):
        theme = self.game.themes[self.game.current_theme]
        event.widget.config(bg=theme["button_hover"])

    def on_leave_main(self, event):
        theme = self.game.themes[self.game.current_theme]
        event.widget.config(bg=theme["button_bg"])

    def on_enter_guess(self, event):
        theme = self.game.themes[self.game.current_theme]
        event.widget.config(bg=theme["button_hover"])

    def on_leave_guess(self, event):
        theme = self.game.themes[self.game.current_theme]
        event.widget.config(bg=theme["button_bg"])

    def on_enter_save(self, event):
        event.widget.config(bg="#ff9800")

    def on_leave_save(self, event):
        event.widget.config(bg="#FFA500")

    def create_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Themes", menu=theme_menu)

        for theme_name in self.game.themes:
            theme_menu.add_command(label=theme_name.capitalize(), command=lambda t=theme_name: self.set_theme(t))

    def set_theme(self, theme_name):
        self.game.current_theme = theme_name
        theme = self.game.themes[theme_name]
        self.configure(bg=theme["bg"])
        self.apply_theme_to_widgets(self, theme)

    def apply_theme_to_widgets(self, widget, theme):
        try:
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            try:
                if isinstance(child, tk.Button):
                    child.configure(bg=theme["button_bg"], fg=theme["button_fg"])
                elif isinstance(child, tk.Radiobutton):
                    child.configure(bg=theme["radio_bg"], fg=theme["radio_fg"], selectcolor=theme["radio_select"])
                else:
                    child.configure(bg=theme["bg"], fg=theme["fg"])
            except tk.TclError:
                pass
            if isinstance(child, (tk.Frame, tk.LabelFrame)):
                self.apply_theme_to_widgets(child, theme)

    def start_game(self):
        self.main_frame.destroy()
        theme = self.game.themes[self.game.current_theme]
        self.game_frame = tk.Frame(self, bg=theme["bg"])
        self.slide_in(self.game_frame)

        tk.Label(self.game_frame, text="Choose Difficulty:", font=("Arial", 18, "bold"), bg=theme["bg"], fg=theme["fg"]).pack(pady=10)
        
        self.difficulty_var = tk.StringVar(value="easy")
        radio_style = {"font": ("Arial", 16), "bg": theme["radio_bg"], "fg": theme["radio_fg"], "selectcolor": theme["radio_select"]}
        tk.Radiobutton(self.game_frame, text="Easy", variable=self.difficulty_var, value="easy", **radio_style).pack(anchor="w", pady=5)
        tk.Radiobutton(self.game_frame, text="Medium", variable=self.difficulty_var, value="medium", **radio_style).pack(anchor="w", pady=5)
        tk.Radiobutton(self.game_frame, text="Hard", variable=self.difficulty_var, value="hard", **radio_style).pack(anchor="w", pady=5)

        play_button = tk.Button(self.game_frame, text="Play", command=self.play_game, font=("Arial", 12), bg=theme["button_bg"], fg=theme["button_fg"], pady=10, padx=20, relief="raised")
        play_button.pack(pady=20)
        play_button.bind("<Enter>", self.on_enter_main)
        play_button.bind("<Leave>", self.on_leave_main)
        play_button.bind("<Button-1>", self.on_press)
        play_button.bind("<ButtonRelease-1>", self.on_release)

        back_button = tk.Button(self.game_frame, text="Back to Main Menu", command=self.create_widgets, font=("Arial", 12), bg="#FF6347", fg="white", pady=10, padx=20, relief="raised")
        back_button.pack(pady=5)
        back_button.bind("<Enter>", lambda e: back_button.config(bg="#E55337"))
        back_button.bind("<Leave>", lambda e: back_button.config(bg="#FF6347"))
        back_button.bind("<Button-1>", self.on_press)
        back_button.bind("<ButtonRelease-1>", self.on_release)

    def play_game(self):
        self.game_frame.destroy()
        difficulty = self.difficulty_var.get()
        (min_range, max_range), self.attempts_limit = self.game.set_difficulty(difficulty)
        self.secret_number = random.randint(min_range, max_range)
        self.attempts = 0
        self.start_time = time.time()

        theme = self.game.themes[self.game.current_theme]
        self.play_frame = tk.Frame(self, bg=theme["bg"])
        self.slide_in(self.play_frame)

        tk.Label(self.play_frame, text=f"Guess the number between {min_range} and {max_range}", font=("Arial", 16), bg=theme["bg"], fg=theme["fg"]).pack(pady=10)
        
        self.guess_entry = tk.Entry(self.play_frame, font=("Arial", 14))
        self.guess_entry.pack(pady=5)

        guess_button = tk.Button(self.play_frame, text="Guess", command=self.check_guess, font=("Arial", 12), bg=theme["button_bg"], fg=theme["button_fg"], pady=10, padx=20, relief="raised")
        guess_button.pack(pady=10)
        guess_button.bind("<Enter>", self.on_enter_guess)
        guess_button.bind("<Leave>", self.on_leave_guess)
        guess_button.bind("<Button-1>", self.on_press)
        guess_button.bind("<ButtonRelease-1>", self.on_release)

        save_button = tk.Button(self.play_frame, text="Save Game", command=self.save_game, font=("Arial", 12), bg="#FFA500", fg="white", pady=10, padx=20, relief="raised")
        save_button.pack(pady=5)
        save_button.bind("<Enter>", self.on_enter_save)
        save_button.bind("<Leave>", self.on_leave_save)
        save_button.bind("<Button-1>", self.on_press)
        save_button.bind("<ButtonRelease-1>", self.on_release)

        back_button = tk.Button(self.play_frame, text="Back to Main Menu", command=self.create_widgets, font=("Arial", 12), bg="#FF6347", fg="white", pady=10, padx=20, relief="raised")
        back_button.pack(pady=5)
        back_button.bind("<Enter>", lambda e: back_button.config(bg="#E55337"))
        back_button.bind("<Leave>", lambda e: back_button.config(bg="#FF6347"))
        back_button.bind("<Button-1>", self.on_press)
        back_button.bind("<ButtonRelease-1>", self.on_release)
        
        self.attempts_label = tk.Label(self.play_frame, text=f"Attempts left: {self.attempts_limit - self.attempts}", font=("Arial", 12), bg=theme["bg"], fg=theme["fg"])
        self.attempts_label.pack()

        self.hint_label = tk.Label(self.play_frame, text="", font=("Arial", 12, "italic"), bg=theme["bg"], fg=theme["fg"])
        self.hint_label.pack()

    def save_game(self):
        self.game.save_game(self.secret_number, self.attempts, self.attempts_limit, self.difficulty_var.get(), self.start_time)

    def load_game(self):
        game_state = self.game.load_game()
        if game_state:
            self.secret_number = game_state["secret_number"]
            self.attempts = game_state["attempts"]
            self.attempts_limit = game_state["attempts_limit"]
            self.difficulty_var.set(game_state["difficulty"])
            self.start_time = game_state["start_time"]

            for widget in self.winfo_children():
                widget.destroy()
            self.create_menu()
            theme = self.game.themes[self.game.current_theme]
            self.play_frame = tk.Frame(self, bg=theme["bg"])
            self.play_frame.pack(pady=20, padx=20, fill="both", expand=True)

            (min_range, max_range), _ = self.game.set_difficulty(self.difficulty_var.get())

            tk.Label(self.play_frame, text=f"Guess the number between {min_range} and {max_range}", font=("Arial", 16), bg=theme["bg"], fg=theme["fg"]).pack(pady=10)
            
            self.guess_entry = tk.Entry(self.play_frame, font=("Arial", 14))
            self.guess_entry.pack(pady=5)

            guess_button = tk.Button(self.play_frame, text="Guess", command=self.check_guess, font=("Arial", 12), bg=theme["button_bg"], fg=theme["button_fg"])
            guess_button.pack(pady=10)
            guess_button.bind("<Enter>", self.on_enter_guess)
            guess_button.bind("<Leave>", self.on_leave_guess)

            save_button = tk.Button(self.play_frame, text="Save Game", command=self.save_game, font=("Arial", 12), bg="#FFA500", fg="white")
            save_button.pack(pady=5)
            save_button.bind("<Enter>", self.on_enter_save)
            save_button.bind("<Leave>", self.on_leave_save)
            
            back_button = tk.Button(self.play_frame, text="Back to Main Menu", command=self.create_widgets, font=("Arial", 12), bg="#FF6347", fg="white")
            back_button.pack(pady=5)
            back_button.bind("<Enter>", lambda e: back_button.config(bg="#E55337"))
            back_button.bind("<Leave>", lambda e: back_button.config(bg="#FF6347"))

            self.hint_label = tk.Label(self.play_frame, text="", font=("Arial", 12, "italic"), bg=theme["bg"], fg=theme["fg"])
            self.hint_label.pack()
        else:
            messagebox.showinfo("No Saved Game", "No saved game found.")

    def ai_guess(self):
        if self.ai_min <= self.ai_max:
            guess = (self.ai_min + self.ai_max) // 2
            self.ai_guess_label.config(text=f"Is your number {guess}?")
            self.current_ai_guess = guess
        else:
                        messagebox.showinfo("AI Error", "You might have provided incorrect feedback.")
                        self.ai_frame.destroy()
                        self.create_widgets()
    def ai_feedback(self, feedback):
        if feedback == "higher":
            self.ai_min = self.current_ai_guess + 1
        elif feedback == "lower":
            self.ai_max = self.current_ai_guess - 1
        self.ai_guess()

    def ai_correct(self):
                messagebox.showinfo("AI Wins!", f"The AI guessed your number: {self.current_ai_guess}")
                self.ai_frame.destroy()
                self.create_widgets()
    def show_animated_message(self, message, color):
        message_window = tk.Toplevel(self)
        message_window.overrideredirect(True)
        message_window.geometry("200x50+550+400")
        message_window.attributes("-alpha", 0.0)

        label = tk.Label(message_window, text=message, bg=color, fg="white", font=("Arial", 12, "bold"))
        label.pack(fill="both", expand=True)

        def fade_in():
            alpha = message_window.attributes("-alpha")
            if alpha < 1.0:
                alpha += 0.1
                message_window.attributes("-alpha", alpha)
                message_window.after(50, fade_in)
            else:
                fade_out()

        def fade_out():
            alpha = message_window.attributes("-alpha")
            if alpha > 0.0:
                alpha -= 0.1
                message_window.attributes("-alpha", alpha)
                message_window.after(50, fade_out)
            else:
                message_window.destroy()

        fade_in()

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1

            if guess < self.secret_number:
                self.show_animated_message("Too low!", "#ff9800")
            elif guess > self.secret_number:
                self.show_animated_message("Too high!", "#ff9800")
            else:
                end_time = time.time()
                time_taken = end_time - self.start_time
                score = self.game.calculate_score(self.attempts, time_taken, self.difficulty_var.get())
                self.show_win_window(self.attempts, time_taken, score)
                return

            if self.attempts >= self.attempts_limit:
                self.show_game_over_window(self.secret_number)
            else:
                self.attempts_label.config(text=f"Attempts left: {self.attempts_limit - self.attempts}")
                self.hint_label.config(text=self.game.get_hint(self.secret_number, self.attempts_limit - self.attempts))

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a number.")

    def show_win_window(self, attempts, time_taken, score):
        win_window = tk.Toplevel(self)
        win_window.title("You Won!")
        win_window.geometry("400x300")
        theme = self.game.themes[self.game.current_theme]
        win_window.configure(bg=theme["bg"])

        tk.Label(win_window, text="Congratulations!", font=("Arial", 24, "bold"), bg=theme["bg"], fg=theme["fg"]).pack(pady=20)

        stats_frame = tk.Frame(win_window, bg=theme["bg"])
        stats_frame.pack(pady=10)

        tk.Label(stats_frame, text=f"Attempts: {attempts}", font=("Arial", 14), bg=theme["bg"], fg=theme["fg"]).pack()
        tk.Label(stats_frame, text=f"Time taken: {time_taken:.2f} seconds", font=("Arial", 14), bg=theme["bg"], fg=theme["fg"]).pack()
        tk.Label(stats_frame, text=f"Your score: {score}", font=("Arial", 14), bg=theme["bg"], fg=theme["fg"]).pack()

        self.game.update_leaderboard(self.username, score, attempts, time_taken, self.difficulty_var.get())
        
        self.game.adjust_range(self.difficulty_var.get(), True)
        win_window.after(3000, lambda: [win_window.destroy(), self.create_widgets()])

    def show_game_over_window(self, secret_number):
        game_over_window = tk.Toplevel(self)
        game_over_window.title("Game Over")
        game_over_window.geometry("400x200")
        theme = self.game.themes[self.game.current_theme]
        game_over_window.configure(bg=theme["bg"])

        tk.Label(game_over_window, text="Game Over!", font=("Arial", 24, "bold"), bg=theme["bg"], fg=theme["fg"]).pack(pady=20)
        tk.Label(game_over_window, text=f"The number was {secret_number}", font=("Arial", 14), bg=theme["bg"], fg=theme["fg"]).pack()

        self.game.adjust_range(self.difficulty_var.get(), False)
        game_over_window.after(3000, lambda: [game_over_window.destroy(), self.create_widgets()])

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1

            if guess < self.secret_number:
                self.show_animated_message("Too low!", "#ff9800")
            elif guess > self.secret_number:
                self.show_animated_message("Too high!", "#ff9800")
            else:
                end_time = time.time()
                time_taken = end_time - self.start_time
                score = self.game.calculate_score(self.attempts, time_taken, self.difficulty_var.get())
                self.show_win_window(self.attempts, time_taken, score)
                return

            if self.attempts >= self.attempts_limit:
                self.show_game_over_window(self.secret_number)
            else:
                self.attempts_label.config(text=f"Attempts left: {self.attempts_limit - self.attempts}")
                self.hint_label.config(text=self.game.get_hint(self.secret_number, self.attempts_limit - self.attempts))

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a number.")


    def show_leaderboard(self):
        self.show_custom_leaderboard()

    def show_custom_leaderboard(self):
        try:
            with open(self.game.leaderboard_file, "r") as f:
                leaderboard_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            leaderboard_data = []

        leaderboard_window = tk.Toplevel(self)
        leaderboard_window.title("Leaderboard")
        leaderboard_window.geometry("600x400")
        theme = self.game.themes[self.game.current_theme]
        leaderboard_window.configure(bg=theme["bg"])

        leaderboard_window.attributes("-alpha", 0.0)
        self.fade_in_widget(leaderboard_window)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=theme["bg"],
                        foreground=theme["fg"],
                        rowheight=25,
                        fieldbackground=theme["bg"])
        style.map('Treeview', background=[('selected', theme["button_bg"])])

        tree = ttk.Treeview(leaderboard_window, columns=("Rank", "Name", "Score", "Attempts", "Time", "Difficulty"), show="headings")
        tree.heading("Rank", text="Rank")
        tree.heading("Name", text="Name")
        tree.heading("Score", text="Score")
        tree.heading("Attempts", text="Attempts")
        tree.heading("Time", text="Time (s)")
        tree.heading("Difficulty", text="Difficulty")

        for i, entry in enumerate(leaderboard_data[:10]):
            tree.insert("", "end", values=(i + 1, entry["name"], entry["score"], entry["attempts"], entry["time_taken"], entry["difficulty"].capitalize()))

        tree.pack(pady=20, padx=20, fill="both", expand=True)

    def show_instructions(self):
        self.show_instructions_window()

    def show_instructions_window(self):
        instructions_window = tk.Toplevel(self)
        instructions_window.title("Instructions")
        instructions_window.geometry("500x400")
        theme = self.game.themes[self.game.current_theme]
        instructions_window.configure(bg=theme["bg"])

        instructions_text = '''
        --- Number Guessing Game Instructions ---

        1. Choose a difficulty level: easy, medium, or hard.

        2. Guess the randomly generated number within the given range.

        3. You have a limited number of attempts based on the difficulty.

        4. Hints will be provided in the last few attempts.

        5. Your score is based on attempts, time, and difficulty.

        6. Try to get a high score and make it to the leaderboard!
        '''

        text_widget = tk.Text(instructions_window, font=("Arial", 12), bg=theme["bg"], fg=theme["fg"], wrap="word", bd=0)
        text_widget.insert("1.0", instructions_text)
        text_widget.config(state="disabled")
        text_widget.pack(pady=20, padx=20, fill="both", expand=True)

    def start_ai_game(self):
        self.main_frame.destroy()
        theme = self.game.themes[self.game.current_theme]
        self.ai_frame = tk.Frame(self, bg=theme["bg"])
        self.slide_in(self.ai_frame)

        tk.Label(self.ai_frame, text="AI Opponent Mode", font=("Arial", 24, "bold"), bg=theme["bg"], fg=theme["fg"]).pack(pady=20)
        tk.Label(self.ai_frame, text="Think of a number between 1 and 100.", font=("Arial", 14), bg=theme["bg"], fg=theme["fg"]).pack(pady=10)

        self.ai_guess_label = tk.Label(self.ai_frame, text="", font=("Arial", 16, "bold"), bg=theme["bg"], fg=theme["fg"])
        self.ai_guess_label.pack(pady=20)

        button_frame = tk.Frame(self.ai_frame, bg=theme["bg"])
        button_frame.pack(pady=10)

        higher_button = tk.Button(button_frame, text="Higher", command=lambda: self.ai_feedback("higher"), font=("Arial", 12), bg=theme["button_bg"], fg=theme["button_fg"], pady=10, padx=20, relief="raised")
        higher_button.pack(side="left", padx=10)
        higher_button.bind("<Enter>", self.on_enter_main)
        higher_button.bind("<Leave>", self.on_leave_main)
        higher_button.bind("<Button-1>", self.on_press)
        higher_button.bind("<ButtonRelease-1>", self.on_release)

        lower_button = tk.Button(button_frame, text="Lower", command=lambda: self.ai_feedback("lower"), font=("Arial", 12), bg=theme["button_bg"], fg=theme["button_fg"], pady=10, padx=20, relief="raised")
        lower_button.pack(side="left", padx=10)
        lower_button.bind("<Enter>", self.on_enter_main)
        lower_button.bind("<Leave>", self.on_leave_main)
        lower_button.bind("<Button-1>", self.on_press)
        lower_button.bind("<ButtonRelease-1>", self.on_release)

        correct_button = tk.Button(button_frame, text="Correct", command=self.ai_correct, font=("Arial", 12), bg="#4CAF50", fg="white", pady=10, padx=20, relief="raised")
        correct_button.pack(side="left", padx=10)
        correct_button.bind("<Enter>", lambda e: correct_button.config(bg="#45a049"))
        correct_button.bind("<Leave>", lambda e: correct_button.config(bg="#4CAF50"))
        correct_button.bind("<Button-1>", self.on_press)
        correct_button.bind("<ButtonRelease-1>", self.on_release)

        back_button = tk.Button(self.ai_frame, text="Back to Main Menu", command=self.create_widgets, font=("Arial", 12), bg="#FF6347", fg="white", pady=10, padx=20, relief="raised")
        back_button.pack(pady=20)
        back_button.bind("<Enter>", lambda e: back_button.config(bg="#E55337"))
        back_button.bind("<Leave>", lambda e: back_button.config(bg="#FF6347"))
        back_button.bind("<Button-1>", self.on_press)
        back_button.bind("<ButtonRelease-1>", self.on_release)

        self.ai_min = 1
        self.ai_max = 100
        self.ai_guess()

if __name__ == "__main__":
    game = NumberGuessingGame()
    app = GameGUI(game)
    app.mainloop()
