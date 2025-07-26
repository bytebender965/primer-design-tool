import tkinter as tk 

 

# Helper functions 

def calculate_gc_content(sequence): 

    """Calculate the GC content of a DNA sequence as a percentage.""" 

    count_G = sequence.count('G') 

    count_C = sequence.count('C') 

    length = len(sequence) 

    return ((count_G + count_C) / length) * 100 

 

def calculate_tm(sequence): 

    """Calculate the melting temperature (Tm) of a DNA sequence.""" 

    count_A = sequence.count('A') 

    count_T = sequence.count('T') 

    count_G = sequence.count('G') 

    count_C = sequence.count('C') 

    return (count_A + count_T) * 2 + (count_G + count_C) * 4 

 

def reverse_complement(sequence): 

    """Generate the reverse complement of a DNA sequence.""" 

    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'} 

    return ''.join(complement[base] for base in reversed(sequence)) 

 

def find_best_primers(dna_sequence): 

    """Find the best forward and reverse primers based on criteria.""" 

    best_pair = None 

    best_gc_diff = float('inf')  # To prioritize primers with GC content closest to 50% 

 

    for length in range(20, 26):  # Primer length: 20-25 bp 

        for start in range(0, len(dna_sequence) - length + 1): 

            forward_primer = dna_sequence[start:start + length] 

            gc_content = calculate_gc_content(forward_primer) 

            tm = calculate_tm(forward_primer) 

 

            if 40 <= gc_content <= 60 and 50 <= tm <= 62: 

                reverse_primer = reverse_complement(forward_primer) 

                reverse_gc = calculate_gc_content(reverse_primer) 

                reverse_tm = calculate_tm(reverse_primer) 

 

                if 40 <= reverse_gc <= 60 and 50 <= reverse_tm <= 62: 

                    # Select the best primer pair based on GC content closest to 50% 

                    gc_diff = abs(gc_content - 50) 

                    if gc_diff < best_gc_diff: 

                        best_pair = (forward_primer, gc_content, tm, reverse_primer, reverse_gc, reverse_tm) 

                        best_gc_diff = gc_diff 

 

    return best_pair 

 

# Function triggered by the GUI button 

def process_sequence(): 

    """Process the DNA sequence entered by the user.""" 

    dna_sequence = input_field.get().upper() 

    if not set(dna_sequence).issubset({'A', 'T', 'G', 'C'}): 

        output_label.config(fg="red")  # Set text color to red for error messages 

        result_text.set("Invalid Input: Please enter a valid DNA sequence (A, T, G, C only).") 

        return 

 

    primer_pair = find_best_primers(dna_sequence) 

    if primer_pair: 

        forward, forward_gc, forward_tm, reverse, reverse_gc, reverse_tm = primer_pair 

        output_label.config(fg="green")  # Set text color to green for valid outputs 

        result_text.set( 

            f"Forward Primer:\n" 

            f"  Sequence: {forward}\n" 

            f"  GC Content: {forward_gc:.2f}%\n" 

            f"  Tm: {forward_tm:.2f}°C\n\n" 

            f"Reverse Primer:\n" 

            f"  Sequence: {reverse}\n" 

            f"  GC Content: {reverse_gc:.2f}%\n" 

            f"  Tm: {reverse_tm:.2f}°C" 

        ) 

    else: 

        output_label.config(fg="red")  # Set text color to red for error messages 

        result_text.set("No suitable primer pairs found.") 

 

# Function to reset the GUI 

def reset_gui(): 

    """Clear the input and output fields.""" 

    input_field.delete(0, tk.END)  # Clear the input field 

    result_text.set("")  # Clear the output text 

    output_label.config(fg="black")  # Reset text color to default 

 

# Create the GUI window 

root = tk.Tk() 

root.title("Primer Design Tool") 

 

# Input field and label 

tk.Label(root, text="Enter DNA Sequence:", font=("Arial", 12)).pack(pady=5) 

input_field = tk.Entry(root, width=50, font=("Arial", 12)) 

input_field.pack(pady=5) 

 

# Buttons for processing and resetting 

button_frame = tk.Frame(root) 

button_frame.pack(pady=10) 

 

process_button = tk.Button(button_frame, text="Design Primers", command=process_sequence, font=("Arial", 12), bg="lightblue") 

process_button.grid(row=0, column=0, padx=5) 

 

reset_button = tk.Button(button_frame, text="Reset", command=reset_gui, font=("Arial", 12), bg="lightcoral") 

reset_button.grid(row=0, column=1, padx=5) 

 

# Output area 

tk.Label(root, text="Suggested Primer Pair:", font=("Arial", 12, "bold")).pack(pady=5) 

result_text = tk.StringVar() 

output_label = tk.Label(root, textvariable=result_text, justify="left", wraplength=400, font=("Courier", 11)) 

output_label.pack(pady=5) 

 

# Run the GUI 

root.mainloop() 