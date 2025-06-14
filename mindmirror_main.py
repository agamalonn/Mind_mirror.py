import tkinter as tk
from tkinter import scrolledtext
import openai

# 🔑 הכניסי כאן את ה-API Key שלך
openai.api_key = "YOUR_API_KEY_HERE"

# 🔍 פונקציה ששולחת את הטקסט לצ'אט GPT ומחזירה תשובה
def analyze_text():
    user_input = entry.get("1.0", tk.END).strip()
    if not user_input:
        output_text.set("Please write something first!")
        return

    output_text.set("Analyzing...")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # אפשר גם "gpt-3.5-turbo"
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
        output_text.set(reply)

    except Exception as e:
        output_text.set(f"Error: {str(e)}")


# 🪟 ממשק משתמש
root = tk.Tk()
root.title("MindMirror - Emotional AI Journal 💖")
root.geometry("600x500")
root.config(bg="#fff0f5")

title = tk.Label(root, text="How are you feeling today?", font=("Arial", 16), bg="#fff0f5")
title.pack(pady=10)

entry = scrolledtext.ScrolledText(root, height=10, width=70, font=("Arial", 12))
entry.pack(pady=10)

analyze_button = tk.Button(root, text="Analyze 💬", command=analyze_text, font=("Arial", 12), bg="#ffb6c1")
analyze_button.pack(pady=10)

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, wraplength=500, justify="left", font=("Arial", 12), bg="#fff0f5")
output_label.pack(padx=20, pady=20)

root.mainloop()
