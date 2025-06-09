import tkinter as tk
from tkinter import scrolledtext, messagebox
import webbrowser
import re
import random

class LearningBotApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🤖 Code Mentor Bot")
        self.master.geometry("700x550")
        self.master.configure(bg="#f0f8ff")
        
       
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
       
        self.create_header_frame()
        self.create_chat_frame()
        self.create_input_frame()
        
       
        self.awaiting_example_response = False
        self.awaiting_new_concept = False
        self.last_topic = ""
        self.user_name = ""
        
       
        greetings = ["Hello there!", "Hi coder!", "Greetings!", "Welcome!", "Ready to learn?"]
        self.insert_bot_message(random.choice(greetings) 
                               + " I'm your Code Mentor Bot. What's your name?")
    
    def create_header_frame(self):
        """Create the header frame with app title"""
        header = tk.Frame(self.master, bg="#4682b4", height=60)
        header.grid(row=0, column=0, sticky="ew", columnspan=2)
        
        title = tk.Label(header, text="💻 Code Mentor Bot", 
                        font=("Arial", 16, "bold"), 
                        bg="#4682b4", fg="white")
        title.pack(pady=15)
    
    def create_chat_frame(self):
        """Create the chat display area"""
        self.chat_frame = tk.Frame(self.master, bg="#f0f8ff")
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
       
        self.text_widget = scrolledtext.ScrolledText(
            self.chat_frame, 
            height=20, 
            wrap=tk.WORD, 
            state=tk.DISABLED, 
            bg="white", 
            fg="#333333", 
            font=("Consolas", 12),
            padx=10,
            pady=10
        )
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        
       
        self.text_widget.tag_configure("user", foreground="#006400", font=("Arial", 12, "bold"))
        self.text_widget.tag_configure("bot", foreground="#8b008b", font=("Arial", 12))
        self.text_widget.tag_configure("code", background="#f0f0f0", font=("Consolas", 11))
        self.text_widget.tag_configure("warning", foreground="red")
        self.text_widget.tag_configure("link", foreground="blue", underline=1)
        
       
        self.text_widget.tag_bind("link", "<Button-1>", self.open_link)
    
    def create_input_frame(self):
        """Create the user input area"""
        input_frame = tk.Frame(self.master, bg="#f0f8ff")
        input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
       
        self.entry = tk.Entry(
            input_frame, 
            font=("Arial", 12), 
            width=50,
            relief=tk.GROOVE,
            bd=2
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda event: self.process_input())
        
        
        button_frame = tk.Frame(input_frame, bg="#f0f8ff")
        button_frame.pack(side=tk.RIGHT, padx=5)
        
        self.submit_button = tk.Button(
            button_frame, 
            text="➤ Ask", 
            command=self.process_input, 
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            width=8,
            relief=tk.RAISED
        )
        self.submit_button.grid(row=0, column=0, padx=2)
        
        self.clear_button = tk.Button(
            button_frame, 
            text="🗑️ Clear", 
            command=self.clear_chat, 
            bg="#ff9800", 
            fg="white", 
            font=("Arial", 10), 
            width=8
        )
        self.clear_button.grid(row=0, column=1, padx=2)
        
        self.exit_button = tk.Button(
            button_frame, 
            text="🚪 Exit", 
            command=self.exit_app, 
            bg="#f44336", 
            fg="white", 
            font=("Arial", 10), 
            width=8
        )
        self.exit_button.grid(row=0, column=2, padx=2)
    
    def insert_bot_message(self, text, code_block=None, link=None):
        """Insert a message from the bot with optional code block"""
        self.text_widget.config(state=tk.NORMAL)
        
        
        self.text_widget.insert(tk.END, "Bot: ", "bot")
        self.text_widget.insert(tk.END, text + "\n", "bot")
        
      
        if code_block:
            self.text_widget.insert(tk.END, code_block + "\n", "code")
        
      
        if link:
            self.text_widget.insert(tk.END, "Learn more: ", "bot")
            self.text_widget.insert(tk.END, link + "\n", "link")
            self.text_widget.insert(tk.END, "\n")
        
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.yview(tk.END)
    
    def insert_user_message(self, text):
        """Insert a message from the user"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, "You: ", "user")
        self.text_widget.insert(tk.END, text + "\n", "user")
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.yview(tk.END)
    
    def process_input(self):
        """Process user input and generate appropriate response"""
        user_input = self.entry.get().strip()
        if not user_input:
            return
        
        self.insert_user_message(user_input)
        self.entry.delete(0, tk.END)
        
      
        if not self.user_name:
            self.user_name = user_input
            welcome = f"Nice to meet you, {self.user_name}! What programming concept would you like to learn about today?"
            self.insert_bot_message(welcome)
            self.insert_bot_message("Try asking about: variables, loops, functions, or conditions")
            return
        
       
        if self.handle_special_commands(user_input):
            return
            
        
        if self.awaiting_example_response:
            self.handle_example_response(user_input)
        elif self.awaiting_new_concept:
            self.handle_new_concept(user_input)
        else:
            self.identify_and_explain_topic(user_input)
    
    def handle_special_commands(self, user_input):
        """Handle special commands like help, about, etc."""
        user_input = user_input.lower()
        
        if user_input in ["help", "?"]:
            help_text = """Available commands:
            - help: Show this help message
            - about: About this application
            - clear: Clear the chat
            - exit: Close the application
            Or ask about programming concepts!"""
            self.insert_bot_message(help_text)
            return True
        
        elif user_input == "about":
            about_text = """Code Mentor Bot v1.0\n
            An interactive learning assistant for Python programming concepts.\n
            Created with Python and Tkinter."""
            self.insert_bot_message(about_text)
            return True
        
        elif user_input == "joke":
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
                "Why do Python programmers need glasses? Because they can't C!"
            ]
            self.insert_bot_message(random.choice(jokes))
            return True
        
        return False
    
    def identify_and_explain_topic(self, user_input):
        """Identify the programming topic and provide explanation"""
        topic_keywords = {
            "variables": {
                "keywords": ["variable", "variables", "define variable", "what is a variable"],
                "explanation": "Variables are containers for storing data values in memory.",
                "example": "x = 5\nprint(x)\n# Output: 5",
                "link": "https://www.w3schools.com/python/python_variables.asp"
            },
            "loops": {
                "keywords": ["loop", "loops", "what is a loop", "explain loops", "for loop", "while loop"],
                "explanation": "Loops allow you to execute a block of code repeatedly until a condition is met.",
                "example": "for i in range(3):\n    print(i)\n# Output:\n# 0\n# 1\n# 2",
                "link": "https://www.w3schools.com/python/python_for_loops.asp"
            },
            "functions": {
                "keywords": ["function", "functions", "define function", "what is a function", "method"],
                "explanation": "Functions are reusable blocks of code that perform a specific task.",
                "example": "def greet():\n    print('Hello!')\n\ngreet()\n# Output: Hello!",
                "link": "https://www.w3schools.com/python/python_functions.asp"
            },
            "conditions": {
                "keywords": ["condition", "if statement", "what is an if statement", "explain conditions", "else"],
                "explanation": "Conditional statements allow your program to make decisions based on certain conditions.",
                "example": "age = 18\nif age >= 18:\n    print('Adult')\nelse:\n    print('Minor')\n# Output: Adult",
                "link": "https://www.w3schools.com/python/python_conditions.asp"
            }
        }
        
        matched_topic = None
        for topic, data in topic_keywords.items():
            if any(re.search(rf"\b{kw}\b", user_input.lower()) for kw in data["keywords"]):
                matched_topic = topic
                break
        
        if matched_topic:
            self.explain_concept(matched_topic, topic_keywords[matched_topic])
        else:
            self.insert_bot_message("I'm not sure I understand. Try asking about:", "variables, loops, functions, or conditions")
            self.insert_bot_message("Or type 'help' for available commands.")
    
    def explain_concept(self, concept, concept_data):
        """Explain a programming concept with examples"""
      
        self.insert_bot_message(concept_data["explanation"])
        
       
        self.insert_bot_message("Here's an example:", concept_data["example"])
        
       
        self.insert_bot_message("", link=concept_data["link"])
        
       
        self.insert_bot_message("Would you like another example? (yes/no)")
        self.awaiting_example_response = True
        self.last_topic = concept
    
    def handle_example_response(self, user_input):
        """Handle user response to example request"""
        if user_input.lower() in ["yes", "y"]:
            self.provide_additional_example()
        else:
            self.insert_bot_message("Would you like to explore another concept? Type a topic name.")
            self.awaiting_example_response = False
            self.awaiting_new_concept = True
    
    def provide_additional_example(self):
        """Provide an additional example for the current topic"""
        examples = {
            "variables": {
                "text": "Here's another variables example:",
                "example": "name = 'Alice'\nage = 25\nprint(f\"{name} is {age} years old\")\n# Output: Alice is 25 years old"
            },
            "loops": {
                "text": "Here's a more complex loop example:",
                "example": "fruits = ['apple', 'banana', 'cherry']\nfor i, fruit in enumerate(fruits, 1):\n    print(f\"{i}. {fruit}\")\n# Output:\n# 1. apple\n# 2. banana\n# 3. cherry"
            },
            "functions": {
                "text": "Here's a function with parameters:",
                "example": "def add_numbers(a, b):\n    return a + b\n\nresult = add_numbers(5, 7)\nprint(result)  # Output: 12"
            },
            "conditions": {
                "text": "Here's an example with multiple conditions:",
                "example": "score = 85\nif score >= 90:\n    grade = 'A'\nelif score >= 80:\n    grade = 'B'\nelse:\n    grade = 'C'\nprint(f\"Grade: {grade}\")  # Output: Grade: B"
            }
        }
        
        if self.last_topic in examples:
            example_data = examples[self.last_topic]
            self.insert_bot_message(example_data["text"], example_data["example"])
        else:
            self.insert_bot_message("I don't have another example for that topic.")
        
        self.insert_bot_message("Would you like to learn about another concept? Type a topic name!")
        self.awaiting_example_response = False
        self.awaiting_new_concept = True
    
    def handle_new_concept(self, user_input):
        """Handle user request for a new concept"""
        self.explain_concept(user_input, self.get_concept_data(user_input))
        self.awaiting_new_concept = False
    
    def get_concept_data(self, concept):
        """Get concept data based on user input"""
        
        concept = concept.lower()
        
        if "variable" in concept:
            return {
                "explanation": "Variables are named containers that store data values.",
                "example": "counter = 0\ncounter += 1\nprint(counter)  # Output: 1",
                "link": "https://www.w3schools.com/python/python_variables.asp"
            }
        elif "loop" in concept:
            return {
                "explanation": "Loops repeat code until a condition is met. Python has 'for' and 'while' loops.",
                "example": "i = 0\nwhile i < 3:\n    print(i)\n    i += 1\n# Output:\n# 0\n# 1\n# 2",
                "link": "https://www.w3schools.com/python/python_while_loops.asp"
            }
        else:
            return {
                "explanation": f"I'm not sure about {concept}, but here's a general tip: Always break problems into smaller parts!",
                "example": "# Pseudocode example:\n# 1. Define the problem\n# 2. Plan the solution\n# 3. Write code step by step",
                "link": "https://www.w3schools.com/python/"
            }
    
    def open_link(self, event):
        """Open web browser when user clicks on a link"""
        widget = event.widget
        index = widget.index(f"@{event.x},{event.y}")
        tag_names = widget.tag_names(index)
        
        if "link" in tag_names:
           
            start = widget.tag_ranges("link")[0]
            end = widget.tag_ranges("link")[1]
            url = widget.get(start, end)
            
           
            webbrowser.open_new(url)
    
    def clear_chat(self):
        """Clear the chat window"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.config(state=tk.DISABLED)
        self.insert_bot_message("Chat cleared. What would you like to learn about?")
    
    def exit_app(self):
        """Exit the application with confirmation"""
        if messagebox.askyesno("Exit", "Are you sure you want to quit?"):
            farewells = [
                "Happy coding!",
                "Keep learning!",
                "See you next time!",
                "May your code always compile!",
                "Remember: The best way to learn is by doing!"
            ]
            self.insert_bot_message(random.choice(farewells))
            self.master.after(1000, self.master.quit)

def run_gui():
    """Run the application"""
    root = tk.Tk()
    app = LearningBotApp(root)
    
    
    try:
        root.iconbitmap("bot_icon.ico")
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    run_gui()