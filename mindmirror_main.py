import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

try:
    import openai
except ImportError:
    raise ImportError("Please install the openai package: pip install openai")

# Optional: For .env support uncomment the next two lines and install python-dotenv
# from dotenv import load_dotenv
# load_dotenv()

# ===== SETUP: Add your OpenAI API Key to your environment =====
# On your command line or in a .env file, set OPENAI_API_KEY=sk-...
# NEVER hardcode secrets in your source files!
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise EnvironmentError(
        "No OpenAI API key found. Set OPENAI_API_KEY as an environment variable."
    )
openai.api_key = openai_api_key

class MindMirrorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MindMirror - Emotional AI Journal 💖")
        self.root.geometry("600x500")
        self.root.config(bg="#fff0f5")

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="How are you feeling today?",
                 font=("Arial", 16), bg="#fff0f5").pack(pady=10)

        self.entry = scrolledtext.ScrolledText(self.root, height=10, width=70,
                                               font=("Arial", 12))
        self.entry.pack(pady=10)

        self.analyze_button = tk.Button(self.root, text="Analyze 💬",
                                        command=self.on_analyze,
                                        font=("Arial", 12), bg="#ffb6c1")
        self.analyze_button.pack(pady=10)

        self.output_text = tk.StringVar()
        self.output_label = tk.Label(self.root, textvariable=self.output_text,
                                     wraplength=500, justify="left",
                                     font=("Arial", 12), bg="#fff0f5")
        self.output_label.pack(padx=20, pady=20)

    def on_analyze(self):
        user_input = self.entry.get("1.0", tk.END).strip()
        if not user_input:
            self.output_text.set("Please write something first!")
            return

        # UX: Disable button, clear output, show loading
        self.analyze_button.config(state=tk.DISABLED)
        self.output_text.set("Analyzing...")

        # Run API call in a separate thread (to keep GUI responsive)
        threading.Thread(target=self.analyze_text, args=(user_input,), daemon=True).start()

    def analyze_text(self, user_input):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": (
                        "אתה יועץ רגשי רגיש. כשהמשתמש כותב יומן אישי, תגיב כך:\n"
                        "- זיהוי רגשות עיקריים\n"
                        "- המלצת שיר שמתאים לרגש\n"
                        "- משפט עידוד קצר ומעורר השראה\n"
                        "כתוב בצורה חמה, נעימה ולא רובוטית."
                    )},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response["choices"][0]["message"]["content"]
            # Update UI from main thread
            self.root.after(0, lambda: self.output_text.set(reply))
        except openai.error.OpenAIError as api_err:
            self.root.after(0, lambda: self.output_text.set(f"OpenAI error: {api_err}"))
        except Exception as e:
            self.root.after(0, lambda: self.output_text.set(f"An error occurred: {e}"))
        finally:
            # Re-enable button
            self.root.after(0, lambda: self.analyze_button.config(state=tk.NORMAL))

if __name__ == "__main__":
    root = tk.Tk()
    app = MindMirrorApp(root)
    root.mainloop()
