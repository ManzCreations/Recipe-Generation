import tkinter as tk
from tkinter import ttk
import pandas as pd
import webbrowser

def print_value(val):
    print(val)

# Create the main window
root = tk.Tk()
root.title("Recipe Generator")

# Create left panel
left_frame = ttk.Frame(root, padding=20)
left_frame.grid(row=0, column=0, sticky="ns")

# Create drop down menus
ingredients = pd.read_csv("ingredients.csv")
ingredients = ingredients.sort_values(by=['Ingredient'])
ingredient1_label = ttk.Label(left_frame, text="Choose Ingredient 1:")
ingredient1_label.grid(row=0, column=0, sticky="w")
ingredient1 = ttk.Combobox(left_frame, values=pd.Series(ingredients["Ingredient"].unique()).to_list(), state="readonly")
ingredient1.grid(row=0, column=1, padx=5, pady=5)

ingredient2_label = ttk.Label(left_frame, text="Choose Ingredient 2:")
ingredient2_label.grid(row=1, column=0, sticky="w")
ingredient2 = ttk.Combobox(left_frame, values=pd.Series(ingredients["Ingredient"].unique()).to_list(), state="readonly")
ingredient2.grid(row=1, column=1, padx=5, pady=5)

ingredient3_label = ttk.Label(left_frame, text="Choose Ingredient 3:")
ingredient3_label.grid(row=2, column=0, sticky="w")
ingredient3 = ttk.Combobox(left_frame, values=pd.Series(ingredients["Ingredient"].unique()).to_list(), state="readonly")
ingredient3.grid(row=2, column=1, padx=5, pady=5)

# Create slider bar
cook_time_label = ttk.Label(left_frame, text="Choose total cook time:")
cook_time_label.grid(row=3, column=0, sticky="w")
cook_time_var = tk.StringVar()
cook_time_var.set(0)
def update_cook_time_var(value):
    cook_time_var.set(f'{value:.6} minutes')
cook_time_slider = ttk.Scale(left_frame, from_=0, to=180, length=200, orient="horizontal", command=update_cook_time_var)
cook_time_slider.grid(row=3, column=1, padx=5, pady=5)
cook_time_slider.set(120)
cook_time_text = ttk.Label(left_frame, textvariable=cook_time_var)
cook_time_text.grid(row=3, column=2, padx=5, pady=5)

# Create generate button
def generate_recipes():
    selected_ingredients = [ingredient1.get(), ingredient2.get(), ingredient3.get()]
    max_cook_time = cook_time_slider.get()
    recipes = ingredients.loc[(ingredients["Ingredient"].isin(selected_ingredients)) & (ingredients["Cook Time (minutes)"] <= max_cook_time)]
    recipe_list.delete(0, tk.END)
    recipe_list.insert(tk.END, *pd.Series(recipes["Recipe"].unique()).tolist())

generate_button = ttk.Button(left_frame, text="Generate recipes", command=generate_recipes)
generate_button.grid(row=4, column=0, columnspan=2, pady=10)

# Create right panel
right_frame = ttk.Frame(root, padding=20)
right_frame.grid(row=0, column=1, sticky="ns")

# Create list box
recipe_list_label = ttk.Label(right_frame, text="Recipe List:")
recipe_list_label.grid(row=0, column=0, sticky="w")
recipe_list = tk.Listbox(right_frame, selectmode="multiple", width=50, height=20)
recipe_list.grid(row=1, column=0, padx=5, pady=5)
recipe_list.delete(0, tk.END)
recipe_list.insert(tk.END, *pd.Series(ingredients["Recipe"].unique()).tolist())

# Create open recipe button
def open_recipes():
    for i in recipe_list.curselection():
        website = ingredients.loc[ingredients["Recipe"] == recipe_list.get(i)]["Website"].values[0]
        webbrowser.open_new_tab(website)

open_recipe_button = ttk.Button(right_frame, text="Open recipes", command=open_recipes)
open_recipe_button.grid(row=4, column=0, columnspan=2, pady=10)

# Start the main loop
root.mainloop()
