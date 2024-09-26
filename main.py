import tkinter as tk
from tkinter import filedialog, Text, messagebox, ttk
import eval
import os
from pathlib import Path

os.environ['PATH'] += os.pathsep + os.path.join(Path(__file__).parent.resolve(), 'dependencies', 'poppler', 'Library', 'bin')
os.environ['TESSDATA_PREFIX'] = os.path.join(Path(__file__).parent.resolve(), 'tesseract-5.3.4', 'tessdata').replace("\\", "/")

def choose_folder(entry):
    folder_path = filedialog.askdirectory(initialdir=Path.home())
    folder_path = os.path.normpath(folder_path)
    if folder_path:
        entry.delete(0, tk.END)
        entry.insert(0, folder_path)


def process_folders():
    excel_folder = excel_folder_entry.get()
    pdf_folder = pdf_folder_entry.get()

    if not excel_folder or not pdf_folder:
        messagebox.showwarning("Errore", "Devi selezionare entrambe le cartelle.")
        return

    process_gen = eval.eval(excel_folder, pdf_folder)
    update_progress(process_gen)
        

def update_progress(process_gen):
    try:
        progress, text = next(process_gen)
        output_text.insert(tk.END, text)
        output_text.see(tk.END)
        progress_bar["value"] = progress
        root.after(100, update_progress, process_gen)
    except StopIteration:
        progress_bar["value"] = 100

# GUI Layout
root = tk.Tk()
root.title("PergaTess")

# Excel folder
excel_folder_frame = tk.Frame(root)
excel_folder_frame.grid(row=0, column=0, padx=5, pady=5)

excel_folder_label = tk.Label(excel_folder_frame, text="Seleziona cartella contenente i file Excel:")
excel_folder_label.grid(row=0, column=0, sticky="w")

excel_folder_entry = tk.Entry(excel_folder_frame, width=50)
excel_folder_entry.grid(row=1, column=0, padx=5, pady=5)

choose_excel_folder_btn = tk.Button(excel_folder_frame, text="Seleziona...", command=lambda: choose_folder(excel_folder_entry))
choose_excel_folder_btn.grid(row=1, column=1, padx=5, pady=5)

# PDF folder
pdf_folder_frame = tk.Frame(root)
pdf_folder_frame.grid(row=1, column=0, padx=5, pady=5)

pdf_folder_label = tk.Label(pdf_folder_frame, text="Seleziona cartella contenente i file PDF:")
pdf_folder_label.grid(row=0, column=0, sticky="w")

pdf_folder_entry = tk.Entry(pdf_folder_frame, width=50)
pdf_folder_entry.grid(row=1, column=0, padx=5, pady=5)

choose_pdf_folder_btn = tk.Button(pdf_folder_frame, text="Seleziona...", command=lambda: choose_folder(pdf_folder_entry))
choose_pdf_folder_btn.grid(row=1, column=1, padx=5, pady=5)

# Output
output_label = tk.Label(root, text="Risultati del processo:")
output_label.grid(row=2, column=0, padx=5, pady=(10, 0), sticky="w")

output_text = Text(root, height=20, width=70)
output_text.grid(row=3, column=0, padx=5, pady=5)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=420, mode="determinate")
progress_bar.grid(row=4, column=0, padx=5, pady=5)

# Process button
process_btn = tk.Button(root, text="Rileva errori", command=process_folders)
process_btn.grid(row=5, column=0, pady=10)

root.mainloop()
