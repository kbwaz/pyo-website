import tkinter as tk
from tkinter import messagebox

# Functions for genetic trait validation and offspring prediction

def validate_color_genotype(genotype):
    valid_colors = ['BB', 'Bb', 'bb']
    if genotype not in valid_colors:
        raise ValueError(f"Invalid color genotype: {genotype}. Must be one of {valid_colors}")

def validate_dilution_genotype(genotype):
    valid_dilutions = ['DD', 'Dd', 'dd']
    if genotype not in valid_dilutions:
        raise ValueError(f"Invalid dilution genotype: {genotype}. Must be one of {valid_dilutions}")

def validate_pattern_genotype(pattern):
    valid_patterns = ['colorpoint', 'mitted', 'bicolor']
    if pattern not in valid_patterns:
        raise ValueError(f"Invalid pattern: {pattern}. Must be one of {valid_patterns}")

def validate_red_genotype(genotype, sex):
    if sex == 'female':
        valid_female_red_genes = ['XOXO', 'XOXo', 'XoXo']
        if genotype not in valid_female_red_genes:
            raise ValueError(f"Invalid female red genotype: {genotype}. Must be one of {valid_female_red_genes}")
    elif sex == 'male':
        valid_male_red_genes = ['XOY', 'XoY']
        if genotype not in valid_male_red_genes:
            raise ValueError(f"Invalid male red genotype: {genotype}. Must be one of {valid_male_red_genes}")
    else:
        raise ValueError(f"Invalid sex: {sex}. Must be 'male' or 'female'")

def validate_parent_input(parent):
    try:
        validate_color_genotype(parent['color'])
        validate_dilution_genotype(parent['dilution'])
        validate_pattern_genotype(parent['pattern'])

        # Validate red gene only if it's present
        if 'red' in parent:
            validate_red_genotype(parent['red'], parent['sex'])

    except ValueError as ve:
        return str(ve)
    return "All inputs are valid!"

def calculate_offspring_traits(parent1, parent2):
    """
    Function to calculate offspring color, dilution, and pattern traits.
    Based on Mendelian inheritance for coat color and pattern.
    """
    try:
        # Validate parent inputs first
        valid1 = validate_parent_input(parent1)
        valid2 = validate_parent_input(parent2)

        if "Invalid" in valid1:
            return valid1
        if "Invalid" in valid2:
            return valid2

        # Example: Let's calculate coat colors and dilution
        color_outcome = {}
        dilution_outcome = {}

        # Color calculation (simple BB, Bb, bb)
        if parent1['color'] == 'BB' and parent2['color'] == 'BB':
            color_outcome['offspring_color'] = 'Seal (100%)'
        elif 'Bb' in [parent1['color'], parent2['color']]:
            color_outcome['offspring_color'] = '75% Seal, 25% Chocolate'
        elif 'bb' in [parent1['color'], parent2['color']]:
            color_outcome['offspring_color'] = '50% Chocolate, 50% Seal carrier'

        # Dilution calculation (simple DD, Dd, dd)
        if parent1['dilution'] == 'dd' or parent2['dilution'] == 'dd':
            dilution_outcome['offspring_dilution'] = '50% Dilute'
        else:
            dilution_outcome['offspring_dilution'] = '75% Dense, 25% Dilute carrier'

        # Pattern prediction (Colorpoint, mitted, bicolor)
        pattern_outcome = f"Possible pattern outcomes: {parent1['pattern']} × {parent2['pattern']}"

        return {
            **color_outcome,
            **dilution_outcome,
            'pattern_outcome': pattern_outcome
        }

    except Exception as e:
        return str(e)

# GUI Interface

def submit_traits():
    parent1 = {
        'color': color1_entry.get(),
        'dilution': dilution1_entry.get(),
        'pattern': pattern1_entry.get(),
        'sex': sex1_entry.get(),
        'red': red1_entry.get() if red1_entry.get() != '' else None
    }
    parent2 = {
        'color': color2_entry.get(),
        'dilution': dilution2_entry.get(),
        'pattern': pattern2_entry.get(),
        'sex': sex2_entry.get(),
        'red': red2_entry.get() if red2_entry.get() != '' else None
    }

    result = calculate_offspring_traits(parent1, parent2)

    if isinstance(result, dict):
        result_message = f"Color Outcome: {result['offspring_color']}\nDilution Outcome: {result['offspring_dilution']}\n{result['pattern_outcome']}"
    else:
        result_message = result  # If there was an error, show the message

    messagebox.showinfo("Prediction Result", result_message)

# Main app window using Tkinter

root = tk.Tk()
root.title("Ragdoll Genetic Trait Predictor")

# Parent 1 input
tk.Label(root, text="Parent 1").grid(row=0, column=0)
tk.Label(root, text="Color:").grid(row=1, column=0)
color1_entry = tk.Entry(root)
color1_entry.grid(row=1, column=1)

tk.Label(root, text="Dilution:").grid(row=2, column=0)
dilution1_entry = tk.Entry(root)
dilution1_entry.grid(row=2, column=1)

tk.Label(root, text="Pattern:").grid(row=3, column=0)
pattern1_entry = tk.Entry(root)
pattern1_entry.grid(row=3, column=1)

tk.Label(root, text="Sex:").grid(row=4, column=0)
sex1_entry = tk.Entry(root)
sex1_entry.grid(row=4, column=1)

tk.Label(root, text="Red (Optional):").grid(row=5, column=0)
red1_entry = tk.Entry(root)
red1_entry.grid(row=5, column=1)

# Parent 2 input
tk.Label(root, text="Parent 2").grid(row=0, column=2)
tk.Label(root, text="Color:").grid(row=1, column=2)
color2_entry = tk.Entry(root)
color2_entry.grid(row=1, column=3)

tk.Label(root, text="Dilution:").grid(row=2, column=2)
dilution2_entry = tk.Entry(root)
dilution2_entry.grid(row=2, column=3)

tk.Label(root, text="Pattern:").grid(row=3, column=2)
pattern2_entry = tk.Entry(root)
pattern2_entry.grid(row=3, column=3)

tk.Label(root, text="Sex:").grid(row=4, column=2)
sex2_entry = tk.Entry(root)
sex2_entry.grid(row=4, column=3)

tk.Label(root, text="Red (Optional):").grid(row=5, column=2)
red2_entry = tk.Entry(root)
red2_entry.grid(row=5, column=3)

# Submit button
submit_button = tk.Button(root, text="Predict Offspring", command=submit_traits)
submit_button.grid(row=6, column=1, columnspan=2)

root.mainloop()
