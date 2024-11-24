import google.generativeai as genai
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import os
class GeminiChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini Chatbot")
        self.root.geometry("800x600")
        
        # Add style configuration
        self.style = ttk.Style()
        self.style.configure('Modern.TFrame', background='#f0f0f0')
        self.style.configure('Modern.TButton', 
                            padding=10, 
                            font=('Helvetica', 10),
                            background='#2196F3')
        
        # Configure root window
        self.root.configure(bg='#f0f0f0')
        
        # Configure API
        GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Generation configuration
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        
        # Safety settings
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
        
        # Initialize model and chat
        self.model = genai.GenerativeModel("gemini-pro",
                                         generation_config=self.generation_config,
                                         safety_settings=self.safety_settings)
        self.convo = self.model.start_chat()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configure grid weights for main window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create main frame with modern style
        main_frame = ttk.Frame(self.root, padding="10", style='Modern.TFrame')
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure main frame grid weights
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Chat display area with custom styling
        self.chat_display = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            height=20,
            font=('Helvetica', 11),
            bg='white',
            fg='#333333',
            padx=10,
            pady=10
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 10))
        
        # Bottom frame for input and buttons
        bottom_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        bottom_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))
        
        # Configure bottom frame grid weights
        bottom_frame.grid_columnconfigure(0, weight=1)  # Make input field expandable
        
        # Input field with modern styling
        self.user_input = tk.Text(
            bottom_frame, 
            font=('Helvetica', 11),
            height=2,  # Adjust this value to control height (in number of lines)
            wrap=tk.WORD,
            padx=5,
            pady=5
        )
        self.user_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        # Button frame for consistent button sizing
        button_frame = ttk.Frame(bottom_frame, style='Modern.TFrame')
        button_frame.grid(row=0, column=1, sticky="e")
        
        # Configure button style
        self.style.configure('Modern.TButton',
                            font=('Helvetica', 10),
                            padding=(10, 5))
        
        # Modern send button
        send_button = ttk.Button(
            button_frame, 
            text="Send", 
            command=self.send_message,
            style='Modern.TButton'
        )
        send_button.grid(row=0, column=0, padx=(0, 5))
        
        # Modern exit button
        exit_button = ttk.Button(
            button_frame, 
            text="Exit", 
            command=self.root.destroy,
            style='Modern.TButton'
        )
        exit_button.grid(row=0, column=1)
        
        # Bind Enter key to send message
        self.user_input.bind('<Return>', self.send_message)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Initial system message
        self.display_message("System: Chat started. Type your message and press Enter or click Send.\n")
        
    def display_message(self, message):
        self.chat_display.config(state='normal')
        
        # Add different colors for different message types
        if message.startswith("You: "):
            self.chat_display.tag_configure("user", foreground="#2196F3", font=('Helvetica', 11, 'bold'))
            self.chat_display.insert(tk.END, message + "\n", "user")
        elif message.startswith("Bot: "):
            self.chat_display.tag_configure("bot", foreground="#4CAF50", font=('Helvetica', 11, 'bold'))
            self.chat_display.insert(tk.END, message + "\n", "bot")
        else:
            self.chat_display.tag_configure("system", foreground="#9E9E9E", font=('Helvetica', 10, 'italic'))
            self.chat_display.insert(tk.END, message + "\n", "system")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state='disabled')
        
    def send_message(self, event=None):
        user_message = self.user_input.get("1.0", tk.END).strip()
        if user_message.lower() in ['quit', 'exit']:
            self.root.destroy()
            return
            
        if user_message:
            # Display user message
            self.display_message(f"You: {user_message}")
            self.user_input.delete("1.0", tk.END)
            
            # Process in separate thread to prevent UI freezing
            threading.Thread(target=self.process_message, args=(user_message,), daemon=True).start()
    
    def process_message(self, user_message):
        try:
            # Get response from Gemini
            response = self.convo.send_message(user_message)
            
            # Display bot response
            self.root.after(0, self.display_message, f"Bot: {response.text}")
            
        except Exception as e:
            self.root.after(0, self.display_message, f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = GeminiChatbot(root)
    root.mainloop()

if __name__ == "__main__":
    main()