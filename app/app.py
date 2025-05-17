import tkinter as tk
from tkinter import messagebox
import random 
from boyer_moore import boyer_moore

FONT = "Segoe UI"

# Generates a random DNA
def generate_dna(size=1050):
    bases = ["A", "C", "G", "T"]
    dna = "".join(random.choices(bases, k=size)).upper()
    return dna

# Formats the DNA
def format_dna(dna, columns=70):
    rows = []
    for i in range(0, len(dna), columns):
        prefix = f"{i:04d}:"
        row = dna[i:i+columns]
        rows.append(f"{prefix} {row}")
    return '\n'.join(rows)

# Updates the TextBox with a new DNA
def update_dna():
    global gen_dna
    gen_dna = generate_dna()
    formated_dna = format_dna(gen_dna)

    box_dna.config(state=tk.NORMAL)
    box_dna.delete("1.0", tk.END)
    box_dna.insert(tk.END, formated_dna)
    box_dna.config(state=tk.DISABLED)

    result.set("")
    input_pattern.delete(0, tk.END)

def highlight_matches(positions, pattern):
    box_dna.config(state=tk.NORMAL)
    box_dna.tag_remove("highlight", "1.0", tk.END)

    text = box_dna.get("1.0", tk.END)
    index_map = []
    dna_index = 0

    # Mapeia posições de DNA real → índices no Text
    for i, char in enumerate(text):
        if char in "ACGT":
            index_map.append(i)
            dna_index += 1
            if dna_index >= 1050:  # parar no final do DNA
                break

    for pos in positions:
        if pos + len(pattern) <= len(index_map):
            start_idx = index_map[pos]
            end_idx = index_map[pos + len(pattern) - 1] + 1

            start = f"1.0 + {start_idx} chars"
            end = f"1.0 + {end_idx} chars"
            box_dna.tag_add("highlight", start, end)

    box_dna.config(state=tk.DISABLED)


def find_matches():
    global gen_dna
    pattern = input_pattern.get().strip().upper()

    if not pattern:
        messagebox.showwarning("Error", "Please, enter a pattern")
        return
    
    positions, _ = boyer_moore(gen_dna, pattern)

    if positions:
        result.set(f"✅ {len(positions)} Matches found at positions: {positions}")
        label_result.config(fg="green")
        highlight_matches(positions, pattern)
    else:
        result.set("❌ No match found!")
        label_result.config(fg="red")
        box_dna.config(state=tk.NORMAL)
        box_dna.tag_remove("highlight", "1.0", tk.END)
        box_dna.config(state=tk.DISABLED)

# Interface
# Main Window
wdw = tk.Tk()
wdw.title("DNA Search - Boyer-Moore")
wdw.geometry("700x600")
wdw.configure(bg="#f2f2f2")

# Fonts
fonte_titulo = (FONT, 14, "bold")
fonte_normal = (FONT, 12)
fonte_resultado = (FONT, 11, "italic")

# First DNA
gen_dna = generate_dna()

# Widgets
tk.Label(wdw, text="🧬 Auto Generated DNA", font=fonte_titulo, bg="#f2f2f2").pack(pady=(10, 5))

box_dna = tk.Text(wdw, height=15, width=80, font=("Courier New", 10), wrap="word")
box_dna.insert(tk.END, gen_dna)
box_dna.config(state=tk.DISABLED, bg="#ffffff", relief=tk.GROOVE, bd=2)
box_dna.tag_configure("highlight", background="lightgreen", foreground="black")
box_dna.pack()

frame_entrada = tk.Frame(wdw, bg="#f2f2f2")
frame_entrada.pack(pady=20)

tk.Label(frame_entrada, text="🔎 Pattern:", font=fonte_normal, bg="#f2f2f2").grid(row=0, column=0, padx=10)
input_pattern = tk.Entry(frame_entrada, width=30, font=fonte_normal)
input_pattern.grid(row=0, column=1, padx=10)

search_button = tk.Button(frame_entrada, text="🔍 Search", font=fonte_normal, bg="#4CAF50", fg="white", width=12, command=find_matches)
search_button.grid(row=0, column=2, padx=10)

update_dna_button = tk.Button(wdw, text="♻️ New DNA", font=fonte_normal, bg="#2196F3", fg="white", width=20, command=update_dna)
update_dna_button.pack(pady=10)

result = tk.StringVar()
label_result = tk.Label(wdw, textvariable=result, font=fonte_resultado, fg="green", bg="#f2f2f2", wraplength=650, justify="center")
label_result.pack(pady=20)

update_dna()
wdw.mainloop()