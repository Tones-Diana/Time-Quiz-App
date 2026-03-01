import customtkinter as ctk
from tkinter import messagebox
import random

# Visual Configurations
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Database with 10 questions per category
quiz_data = {
    "General Knowledge": [
        {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin", "Rome"], "answer": "Paris"},
        {"question": "How many continents are there?", "options": ["5", "6", "7", "8"], "answer": "7"},
        {"question": "Who painted the Mona Lisa?", "options": ["Picasso", "Da Vinci", "Van Gogh", "Dali"], "answer": "Da Vinci"},
        {"question": "What is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific"},
        {"question": "What is the chemical symbol for Gold?", "options": ["Ag", "Fe", "Au", "Pb"], "answer": "Au"},
        {"question": "Which is the highest mountain in the world?", "options": ["K2", "Everest", "Fuji", "Mont Blanc"], "answer": "Everest"},
        {"question": "In what year did World War II begin?", "options": ["1914", "1939", "1945", "1918"], "answer": "1939"},
        {"question": "How many legs does a spider have?", "options": ["6", "8", "4", "10"], "answer": "8"},
        {"question": "What is the official language of Brazil?", "options": ["Spanish", "English", "Portuguese", "French"], "answer": "Portuguese"},
        {"question": "Which planet is known as the Red Planet?", "options": ["Venus", "Jupiter", "Mars", "Saturn"], "answer": "Mars"}
    ],
    "Mathematics": [
        {"question": "What is 2 + 2 * 2?", "options": ["8", "6", "4", "10"], "answer": "6"},
        {"question": "What is the square root of 81?", "options": ["7", "8", "9", "10"], "answer": "9"},
        {"question": "What is 15% of 200?", "options": ["20", "30", "40", "15"], "answer": "30"},
        {"question": "What is 12 x 12?", "options": ["124", "144", "164", "112"], "answer": "144"},
        {"question": "A triangle with all sides equal is called?", "options": ["Isosceles", "Right", "Equilateral", "Scalene"], "answer": "Equilateral"},
        {"question": "7 x 8 = ?", "options": ["54", "56", "64", "48"], "answer": "56"},
        {"question": "What is the approximate value of Pi?", "options": ["3.12", "3.14", "3.16", "3.18"], "answer": "3.14"},
        {"question": "What is 100 divided by 4?", "options": ["20", "25", "30", "50"], "answer": "25"},
        {"question": "What is 5 to the power of 3?", "options": ["15", "25", "125", "75"], "answer": "125"},
        {"question": "Which of these is a prime number?", "options": ["4", "9", "13", "15"], "answer": "13"}
    ],
    "Computer Science": [
        {"question": "What is a 'bool'?", "options": ["Number", "Text", "Logical value", "List"], "answer": "Logical value"},
        {"question": "Who created Python?", "options": ["Steve Jobs", "Guido van Rossum", "Bill Gates", "Mark Zuckerberg"], "answer": "Guido van Rossum"},
        {"question": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Tech Multi Language", "Home Tool Markup Language", "Hyperlink Text Mode"], "answer": "Hyper Text Markup Language"},
        {"question": "What is the standard port for HTTP?", "options": ["21", "80", "443", "22"], "answer": "80"},
        {"question": "RAM memory is considered:", "options": ["Permanent", "Volatile", "External", "Optical"], "answer": "Volatile"},
        {"question": "What is the file extension for Python files?", "options": [".py", ".exe", ".txt", ".js"], "answer": ".py"},
        {"question": "What is an algorithm?", "options": ["A secret code", "A series of steps", "A hardware part", "A virus"], "answer": "A series of steps"},
        {"question": "What is the basic unit of information?", "options": ["Byte", "Bit", "Pixel", "Hertz"], "answer": "Bit"},
        {"question": "What does 'print()' do in Python?", "options": ["Deletes", "Creates file", "Displays text", "Closes program"], "answer": "Displays text"},
        {"question": "Which of these is a famous database?", "options": ["MySQL", "Photoshop", "Excel", "Windows"], "answer": "MySQL"}
    ]
}

class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Master Pro")
        self.geometry("650x650")

        # Logic Variables
        self.questions = []
        self.question_index = 0
        self.score = 0
        self.timer_count = 100 
        self.timer_id = None

        # --- UI - Main Container ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        # --- START SCREEN ---
        self.start_screen = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.start_screen.pack(expand=True)
        self.label_welcome = ctk.CTkLabel(self.start_screen, text="Select a Category", font=("Roboto", 28, "bold"))
        self.label_welcome.pack(pady=20)

        for cat in quiz_data.keys():
            btn = ctk.CTkButton(self.start_screen, text=cat, font=("Roboto", 16), width=240, height=50,
                                command=lambda c=cat: self.start_quiz(c))
            btn.pack(pady=10)

        # --- GAME SCREEN ---
        self.game_screen = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        self.question_info_label = ctk.CTkLabel(self.game_screen, text="", font=("Roboto", 14, "italic"))
        self.question_info_label.pack(pady=(10, 0))

        self.question_label = ctk.CTkLabel(self.game_screen, text="", font=("Roboto", 22, "bold"), wraplength=500)
        self.question_label.pack(pady=20)

        # Progress Bar for Timer
        self.progress_bar = ctk.CTkProgressBar(self.game_screen, width=400, height=12)
        self.progress_bar.set(1.0)
        self.progress_bar.pack(pady=10)

        # Answer Grid (2x2)
        self.ans_container = ctk.CTkFrame(self.game_screen, fg_color="transparent")
        self.ans_container.pack(pady=20)
        
        self.option_buttons = []
        for i in range(4):
            btn = ctk.CTkButton(self.ans_container, text="", width=220, height=60, font=("Roboto", 16),
                                command=lambda idx=i: self.check_answer(idx))
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
            self.option_buttons.append(btn)

        self.score_label = ctk.CTkLabel(self.game_screen, text="Score: 0", font=("Roboto", 18))
        self.score_label.pack(pady=10)

    def start_quiz(self, category):
        # Load and shuffle questions
        self.questions = list(quiz_data[category])
        random.shuffle(self.questions)
        self.question_index = 0
        self.score = 0
        
        self.start_screen.pack_forget()
        self.game_screen.pack(expand=True, fill="both")
        self.show_question()

    def show_question(self):
        if self.timer_id: self.after_cancel(self.timer_id)

        if self.question_index < len(self.questions):
            q = self.questions[self.question_index]
            self.question_info_label.configure(text=f"Question {self.question_index + 1} of 10")
            self.question_label.configure(text=q["question"])
            
            # Shuffle options for variety
            opts = list(q["options"])
            random.shuffle(opts)
            
            for i, option in enumerate(opts):
                self.option_buttons[i].configure(text=option, fg_color=["#3B8ED0", "#1F6AA5"], state="normal")
            
            self.timer_count = 100 
            self.update_timer()
        else:
            self.end_quiz()

    def update_timer(self):
        if self.timer_count > 0:
            self.timer_count -= 1
            self.progress_bar.set(self.timer_count / 100)
            
            # Change color to red if time is running out
            if self.timer_count < 30: self.progress_bar.configure(progress_color="red")
            else: self.progress_bar.configure(progress_color="#3B8ED0")
            
            self.timer_id = self.after(100, self.update_timer) 
        else:
            # Time's up! Move to next question
            self.question_index += 1
            self.show_question()

    def check_answer(self, idx):
        if self.timer_id: self.after_cancel(self.timer_id)
        
        # Disable buttons to prevent multiple clicks
        for btn in self.option_buttons: btn.configure(state="disabled")

        selected = self.option_buttons[idx].cget("text")
        correct = self.questions[self.question_index]["answer"]
        
        if selected == correct:
            self.score += 1
            self.option_buttons[idx].configure(fg_color="green", hover_color="green")
        else:
            self.option_buttons[idx].configure(fg_color="red", hover_color="red")
            # Highlight the correct one
            for btn in self.option_buttons:
                if btn.cget("text") == correct: btn.configure(fg_color="green")
        
        self.score_label.configure(text=f"Score: {self.score}")
        self.question_index += 1
        
        # Pause for 1.2s so user can see the result
        self.after(1200, self.show_question)

    def end_quiz(self):
        messagebox.showinfo("Quiz Finished", f"Congratulations!\nFinal Score: {self.score}/10")
        self.game_screen.pack_forget()
        self.start_screen.pack(expand=True)

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()