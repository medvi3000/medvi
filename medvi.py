import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import sqlite3
import os
import io
import google.generativeai as genai
from datetime import datetime
from gpiozero import Button
import threading
from signal import pause

# === CONFIGURE GEMINI API KEY ===
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-2.5-flash")

# === DATABASE SETUP ===
conn = sqlite3.connect("medvi_local.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    phone_number TEXT,
    timestamp TEXT,
    image_path TEXT,
    extracted_text TEXT
)''')
conn.commit()

# === GLOBAL VARIABLES ===
captured_image_path = None
patient_id = ""
phone_number = ""

# === GEMINI OCR FUNCTION ===
def extract_text_from_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()
        response = model.generate_content(
            [
                "Extract only the handwritten text in this image with no explanation or preamble.",
                {"mime_type": "image/jpeg", "data": image_data},
            ]
        )
        return response.text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# === GUI LOGIC ===
def login_user():
    global patient_id, phone_number
    patient_id = entry_id.get()
    phone_number = entry_phone.get()
    if not patient_id or not phone_number:
        messagebox.showwarning("Login Failed", "Please enter both ID and phone number.")
        return
    login_frame.pack_forget()
    show_dashboard()

def show_dashboard():
    root.geometry("900x500")
    dashboard_frame.pack()

def capture_image():
    global captured_image_path
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            captured_image_path = "captured_image.jpg"
            cv2.imwrite(captured_image_path, frame)
            update_preview(captured_image_path)
        else:
            messagebox.showerror("Error", "Image capture failed.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def button_pressed():
    capture_image()

def start_button_listener():
    try:
        button = Button(17)
        button.when_pressed = button_pressed
        pause()
    except Exception as e:
        print(f"Button error: {e}")

def update_preview(img_path):
    img = Image.open(img_path)
    img.thumbnail((250, 250))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk

def upload_image():
    global captured_image_path
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if path:
        captured_image_path = path
        update_preview(path)

def generate_report():
    if not captured_image_path:
        messagebox.showwarning("No Image", "Upload or capture an image first.")
        return
    text = extract_text_from_image(captured_image_path)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)

def save_to_db():
    if not captured_image_path or output_box.get("1.0", tk.END).strip() == "":
        messagebox.showwarning("Empty Fields", "Ensure an image is captured and report generated.")
        return
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO reports (patient_id, phone_number, timestamp, image_path, extracted_text) VALUES (?, ?, ?, ?, ?)",
                   (patient_id, phone_number, now, captured_image_path, output_box.get("1.0", tk.END)))
    conn.commit()
    messagebox.showinfo("Saved", "Report saved successfully.")

def download_report():
    if output_box.get("1.0", tk.END).strip() == "":
      messagebox.showwarning("No Report", "Generate a report first.")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
    if save_path:
        with open(save_path, "w") as f:
            f.write(f"Patient ID: {patient_id}\nPhone: {phone_number}\n\n")
            f.write(output_box.get("1.0", tk.END))
        messagebox.showinfo("Downloaded", "Report downloaded successfully.")

# === UI SETUP ===
root = tk.Tk()
root.title("MedVi OCR Interface")
root.configure(bg="#f0f4f7")
root.geometry("400x300")

# === LOGIN FRAME ===
login_frame = tk.Frame(root, bg="#e0e0e0")
login_frame.pack(expand=True)

tk.Label(login_frame, text="MedVi Login", font=("Helvetica", 16, "bold"), bg="#e0e0e0").pack(pady=10)
tk.Label(login_frame, text="Patient ID", bg="#e0e0e0").pack()
entry_id = tk.Entry(login_frame)
entry_id.pack()
tk.Label(login_frame, text="Phone Number", bg="#e0e0e0").pack()
entry_phone = tk.Entry(login_frame)
entry_phone.pack()
tk.Button(login_frame, text="Login", command=login_user, bg="#4caf50", fg="white").pack(pady=10)

# === DASHBOARD FRAME ===
dashboard_frame = tk.Frame(root, bg="#f0f4f7")

tk.Label(dashboard_frame, text="MedVi Patient Report Generator", font=("Helvetica", 14, "bold"), bg="#f0f4f7").pack(pady=10)

btns = tk.Frame(dashboard_frame, bg="#f0f4f7")
btns.pack(pady=5)
tk.Button(btns, text="📸 Capture Image", command=capture_image, bg="#2196f3", fg="white").grid(row=0, column=0, padx=5)
tk.Button(btns, text="🗂 Upload Image", command=upload_image, bg="#03a9f4", fg="white").grid(row=0, column=1, padx=5)
tk.Button(btns, text="📄 Generate Report", command=generate_report, bg="#009688", fg="white").grid(row=0, column=2, padx=5)

main_area = tk.Frame(dashboard_frame, bg="#f0f4f7")
main_area.pack(pady=10, fill="both", expand=True)

image_label = tk.Label(main_area, bg="#cccccc", width=250, height=250)
image_label.pack(side="left", padx=20)

output_box = tk.Text(main_area, height=15, width=50, wrap="word")
output_box.pack(side="right", padx=20)

bottom_btns = tk.Frame(dashboard_frame, bg="#f0f4f7")
bottom_btns.pack(pady=10)

tk.Button(bottom_btns, text="💾 Save to DB", command=save_to_db, bg="#4caf50", fg="white").grid(row=0, column=0, padx=10)
tk.Button(bottom_btns, text="⬇️ Download Report", command=download_report, bg="#ff9800", fg="white").grid(row=0, column=1, padx=10)

# === GPIO Thread ===
threading.Thread(target=start_button_listener, daemon=True).start()

root.mainloop()
