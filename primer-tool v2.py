import tkinter as tk
from tkinter import messagebox, scrolledtext

def calculate_gc_content(seq):
    gc_count = seq.count("G") + seq.count("C")
    return (gc_count / len(seq)) * 100 if seq else 0

def calculate_tm(seq):
    return 4 * (seq.count("G") + seq.count("C")) + 2 * (seq.count("A") + seq.count("T"))

def design_primers():
    seq = sequence_entry.get("1.0", tk.END).strip().upper()

    if not seq:
        messagebox.showwarning("Input Required", "Please enter a DNA sequence.")
        return

    if not all(base in "ATGC" for base in seq):
        messagebox.showerror("Invalid Sequence", "DNA sequence must contain only A, T, G, or C.")
        return

    if len(seq) < 40:
        messagebox.showerror("Sequence Too Short", "Enter a sequence at least 40 bases long.")
        return

    forward_primer = seq[:20]
    reverse_primer = seq[-20:][::-1].translate(str.maketrans("ATGC", "TACG"))

    forward_gc = calculate_gc_content(forward_primer)
    reverse_gc = calculate_gc_content(reverse_primer)
    forward_tm = calculate_tm(forward_primer)
    reverse_tm = calculate_tm(reverse_primer)

    output_text = (
        f"✔ Forward Primer:\n"
        f"Sequence: {forward_primer}\n"
        f"GC Content: {forward_gc:.2f}%\n"
        f"Tm: {forward_tm:.2f}°C\n\n"
        f"✔ Reverse Primer:\n"
        f"Sequence: {reverse_primer}\n"
        f"GC Content: {reverse_gc:.2f}%\n"
        f"Tm: {reverse_tm:.2f}°C"
    )

    result_output.config(state="normal")
    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, output_text)
    result_output.config(state="disabled")

def reset_fields():
    sequence_entry.delete("1.0", tk.END)
    result_output.config(state="normal")
    result_output.delete("1.0", tk.END)
    result_output.config(state="disabled")

def export_results():
    result_output.config(state="normal")
    content = result_output.get("1.0", tk.END).strip()
    result_output.config(state="disabled")

    if not content:
        messagebox.showwarning("Nothing to Export", "Please design primers first before exporting.")
        return

    try:
        with open("primer_results.txt", "w", encoding="utf-8") as file:
            file.write(content)
        messagebox.showinfo("Exported", "Results saved to 'primer_results.txt'")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export file:\n{e}")

# GUI setup
root = tk.Tk()
root.title("Primer Design Tool")
root.geometry("800x500")
root.minsize(700, 450)
root.configure(bg="white")

# Fonts
title_font = ("Helvetica", 16, "bold")
label_font = ("Segoe UI", 11)
btn_font = ("Segoe UI", 10, "bold")

# Title
title_label = tk.Label(root, text="Primer Design Tool", font=title_font, fg="#333", bg="white")
title_label.pack(pady=10)

# Input frame
input_frame = tk.LabelFrame(root, text="Input DNA Sequence", font=label_font, padx=10, pady=5, bg="white")
input_frame.pack(fill="x", padx=20)

sequence_entry = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=4, font=("Consolas", 11))
sequence_entry.pack(fill="x", expand=True)

# Button frame
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

design_btn = tk.Button(button_frame, text="Design Primers", bg="#4CAF50", fg="white", font=btn_font, command=design_primers, width=15)
design_btn.grid(row=0, column=0, padx=10)

reset_btn = tk.Button(button_frame, text="Reset", bg="#f44336", fg="white", font=btn_font, command=reset_fields, width=10)
reset_btn.grid(row=0, column=1, padx=10)

export_btn = tk.Button(button_frame, text="Export Results", bg="#2196F3", fg="white", font=btn_font, command=export_results, width=15)
export_btn.grid(row=0, column=2, padx=10)

# Output frame
output_frame = tk.LabelFrame(root, text="Suggested Primer Pair", font=label_font, padx=10, pady=5, bg="white")
output_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

result_output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Consolas", 11), state="disabled")
result_output.pack(fill="both", expand=True)

root.mainloop()
