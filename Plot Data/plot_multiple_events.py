# import os
# import re
# import glob
# import pandas as pd
# import matplotlib.pyplot as plt

# def load_sensor_data(file_path):
#     try:
#         df = pd.read_csv(file_path, delimiter=",", header=None)
#     except Exception as e:
#         print(f"Error reading {file_path}: {e}")
#         return None
#     if df.shape[1] >= 4:
#         df = df.iloc[:, :4]
#         df.columns = ['timestamp', 'x', 'y', 'z']
#     else:
#         df.columns = ['x', 'y', 'z']
#     return df

# def plot_comparison_graph(files, path):
#     plt.figure(figsize=(12, 7))
#     for f_path in files:
#         df = load_sensor_data(f_path)
#         if df is not None:
#             plt.plot(df['x'].values, label=f"{f_path[-40:]}")
    
#     plt.title(f"Comparison for Sensor: Magnetometer\nActivity: slow_walk")
#     plt.xlabel("Time (samples)")
#     plt.ylabel("X Value")
#     plt.legend(loc="best")
#     plt.grid(True)
#     # plt.show()
#     plt.savefig(path)
#     plt.close()
#     print(f"Saved comparison graph: {path}")

# def main():
#     # Get the source dataset folder and destination folder for plots.
#     path = input("Enter the path to save plots: ").strip()
#     files = [
#         r"C:\Users\Malik Haider\Documents\HUMCARE\DataSet\March23\Sync_Data_Correct\BITF21M541\slow_walk\glass_accelerometer_e3.csv",
#         r"C:\Users\Malik Haider\Documents\HUMCARE\DataSet\March23\Sync_Data_Correct\bitf21m542\slow_walk\glass_accelerometer_e3.csv",
#         r"C:\Users\Malik Haider\Documents\HUMCARE\DataSet\March23\Sync_Data_Correct\BITF21M549\slow_walk\glass_accelerometer_e3.csv",
#         r"C:\Users\Malik Haider\Documents\HUMCARE\DataSet\March23\Sync_Data_Correct\sub\slow_walk\glass_accelerometer_e3.csv",
#     ]
#     path+="\plot.png"
#     plot_comparison_graph(files,path)
    
# if __name__ == "__main__":
#     main()

import os
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox, Listbox, Scrollbar

def load_sensor_data(file_path):
    """Load sensor data from CSV file."""
    try:
        df = pd.read_csv(file_path, delimiter=",", header=None)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    if df.shape[1] >= 4:
        df = df.iloc[:, :4]
        df.columns = ['timestamp', 'x', 'y', 'z']
    else:
        df.columns = ['x', 'y', 'z']
    
    return df

def plot_comparison_graph(files, save_path):
    """Plot data from multiple files in a single graph."""
    plt.figure(figsize=(12, 7))
    
    for f_path in files:
        df = load_sensor_data(f_path)
        if df is not None:
            plt.plot(df['x'].values, label=os.path.basename(f_path))  # Label with filename
    
    plt.title("Comparison Graph")
    plt.xlabel("Time (samples)")
    plt.ylabel("X Value")
    plt.legend(loc="best")
    plt.grid(True)
    
    plt.savefig(save_path)
    plt.close()
    messagebox.showinfo("Success", f"Saved plot: {save_path}")

def add_files(event):
    """Handle drag-and-drop files."""
    files = root.tk.splitlist(event.data)  # Get dropped files
    for file in files:
        if file.endswith(".csv") and file not in file_list:
            file_list.append(file)
            listbox.insert(tk.END, file)  # Add file to listbox

def remove_selected():
    """Remove selected file from the list."""
    selected = listbox.curselection()
    for index in reversed(selected):
        del file_list[index]
        listbox.delete(index)

def browse_files():
    """Manually add files via file dialog."""
    files = filedialog.askopenfilenames(filetypes=[("CSV Files", "*.csv")])
    for file in files:
        if file.endswith(".csv") and file not in file_list:
            file_list.append(file)
            listbox.insert(tk.END, file)

def generate_plot():
    """Generate plot from selected files."""
    if not file_list:
        messagebox.showwarning("Warning", "No files selected!")
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png", filetypes=[("PNG files", "*.png")]
    )
    
    if not save_path:
        return

    plot_comparison_graph(file_list, save_path)

# Create main window
root = TkinterDnD.Tk()
root.title("Drag & Drop CSV Plotter")
root.geometry("600x400")

# Instructions
label = tk.Label(root, text="Drag & Drop CSV Files Below or Click 'Add Files'", font=("Arial", 12))
label.pack(pady=5)

# Listbox with scrollbars to show files
frame = tk.Frame(root)
frame.pack(pady=5, expand=True, fill=tk.BOTH)

listbox = Listbox(frame, selectmode=tk.MULTIPLE, width=80, height=10)
scrollbar = Scrollbar(frame, orient="vertical", command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Drag-and-drop support
listbox.drop_target_register(DND_FILES)
listbox.dnd_bind("<<Drop>>", add_files)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

btn_add = tk.Button(btn_frame, text="Add Files", command=browse_files)
btn_add.grid(row=0, column=0, padx=5)

btn_remove = tk.Button(btn_frame, text="Remove Selected", command=remove_selected)
btn_remove.grid(row=0, column=1, padx=5)

btn_plot = tk.Button(root, text="Generate Plot", command=generate_plot, font=("Arial", 12, "bold"))
btn_plot.pack(pady=10)

# File list to store added files
file_list = []

# Run the GUI
root.mainloop()
