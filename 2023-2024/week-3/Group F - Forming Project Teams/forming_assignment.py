import tkinter as tk

# Function to calculate binomial coefficient using dynamic programming algorithm
def calculate_binomial_coefficient(n, k):
    C = [[0] * (k + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(min(i, k) + 1):
            if j == 0 or j == i:
                C[i][j] = 1
            else:
                C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
    return C[n][k], C

# Function to handle button click event
def calculate_teams():
    total_developers = int(entry_total.get())
    developers_per_team = int(entry_per_team.get())
    if developers_per_team> total_developers:
        result_label.config(text="Invalid input: Team size cannot be larger than the total number of developers.", fg='red')
        return
    num_teams, binomial_table = calculate_binomial_coefficient(total_developers, developers_per_team)
    result_label.config(text=f"Number of sub-teams: {num_teams}")
    display_table(binomial_table,total_developers,developers_per_team)

def display_table(table, total_developers, developers_per_team):
    table_window = tk.Toplevel(root)
    table_window.title("Binomial Coefficient Table")
    table_text = tk.Text(table_window, height=len(table) + 1, width=len(table[0]) * 10)  # Adjust the width here
    table_text.pack()
    
    # Display column numbers
    for colHead in range(developers_per_team+1):
        table_text.insert(tk.END, f"  {colHead:<2}","header")  # Adjust the width and alignment
    table_text.insert(tk.END, "\n")
    
    for i in range(len(table)):
        # Display row number
        table_text.insert(tk.END, f"{i:<2}","header")  # Adjust the width and alignment
        for j in range(len(table[i])):
            table_text.insert(tk.END, f"{table[i][j]:<3} ","special" if (i, j) == (total_developers, developers_per_team) else "normal")
        table_text.insert(tk.END, '\n')
        #Tag configuration
    table_text.tag_configure("header", foreground="red")
    table_text.tag_configure("special",foreground="blue")

# Create main window
root = tk.Tk()
root.title("Team Formation Calculator")

# UI components
label_total = tk.Label(root, text="Enter total number of developers:")
label_total.pack()
entry_total = tk.Entry(root)
entry_total.pack()

label_per_team = tk.Label(root, text="Enter number of developers per team:")
label_per_team.pack()
entry_per_team = tk.Entry(root)
entry_per_team.pack()

calculate_button = tk.Button(root, text="Calculate", command=calculate_teams)
calculate_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()

