import tkinter as tk
from tkinter import messagebox
import json
import os

# Define the directory and file path
SUPPORT_DIR = os.path.join("src", "support_files")
TASKS_FILE = os.path.join(SUPPORT_DIR, "tasks.json")

# Ensure the support_files directory exists
if not os.path.exists(SUPPORT_DIR):
    os.makedirs(SUPPORT_DIR)

class DraggableTask(tk.Frame):
    def __init__(self, parent, task, quadrant, bg_color, *args, **kwargs):
        super().__init__(parent, bg=bg_color, pady=5, *args, **kwargs)
        self.parent = parent
        self.task = task
        self.quadrant = quadrant
        self.bg_color = bg_color

        self.task_label = tk.Label(self, text=task, bg=bg_color, anchor='w')
        self.task_label.pack(side='left', fill='x', expand=True)

        self.delete_button = tk.Button(self, text="Delete", command=self.delete_task)
        self.delete_button.pack(side='right')

        self.task_label.bind("<Button-1>", self.on_start)
        self.task_label.bind("<B1-Motion>", self.on_drag)
        self.task_label.bind("<ButtonRelease-1>", self.on_drop)

    def on_start(self, event):
        self._drag_data = {"x": event.x, "y": event.y}

    def on_drag(self, event):
        x = self.winfo_x() - self._drag_data["x"] + event.x
        y = self.winfo_y() - self._drag_data["y"] + event.y
        self.place(x=x, y=y)

    def on_drop(self, event):
        self.place_forget()
        self.pack(fill='x', pady=5)

    def delete_task(self):
        self.destroy()
        remove_task(self.quadrant, self.task)

def add_task(quadrant, task, save=True):
    if quadrant == 1:
        frame = frame1_content
        bg_color = '#ffcccb'  # Pastel Red
    elif quadrant == 2:
        frame = frame2_content
        bg_color = '#aec6cf'  # Pastel Blue
    elif quadrant == 3:
        frame = frame3_content
        bg_color = '#77dd77'  # Pastel Green
    elif quadrant == 4:
        frame = frame4_content
        bg_color = '#fdfd96'  # Pastel Yellow
    else:
        print(f"Warning: Invalid quadrant {quadrant}. Task not added.")
        return
    
    task_frame = DraggableTask(frame, task, quadrant, bg_color)
    task_frame.pack(fill='x', pady=5)

    if save:
        save_tasks()

def get_task():
    task = task_entry.get()
    try:
        quadrant = int(quadrant_entry.get())
        if quadrant in [1, 2, 3, 4]:
            add_task(quadrant, task)
        else:
            messagebox.showerror("Invalid Input", "Please enter a number between 1 and 4.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
    task_entry.delete(0, tk.END)

def save_tasks():
    tasks = {1: [], 2: [], 3: [], 4: []}
    for task_frame in frame1_content.winfo_children():
        if isinstance(task_frame, DraggableTask):
            tasks[1].append(task_frame.task)
    for task_frame in frame2_content.winfo_children():
        if isinstance(task_frame, DraggableTask):
            tasks[2].append(task_frame.task)
    for task_frame in frame3_content.winfo_children():
        if isinstance(task_frame, DraggableTask):
            tasks[3].append(task_frame.task)
    for task_frame in frame4_content.winfo_children():
        if isinstance(task_frame, DraggableTask):
            tasks[4].append(task_frame.task)

    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            tasks = json.load(file)
            for quadrant, task_list in tasks.items():
                for task in task_list:
                    try:
                        quadrant = int(quadrant)
                        if quadrant in [1, 2, 3, 4]:
                            add_task(quadrant, task, save=False)
                        else:
                            print(f"Warning: Invalid quadrant {quadrant} in file. Task not loaded.")
                    except ValueError:
                        print(f"Warning: Invalid task data for quadrant {quadrant}.")

def remove_task(quadrant, task):
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            tasks = json.load(file)
            if task in tasks[quadrant]:
                tasks[quadrant].remove(task)
                with open(TASKS_FILE, 'w') as file:
                    json.dump(tasks, file)

def on_closing():
    save_tasks()
    root.destroy()

root = tk.Tk()
root.title("Eisenhower Matrix")
root.geometry("600x600")

def create_scrollable_frame(root, bg_color, relx, rely):
    container = tk.Frame(root)
    canvas = tk.Canvas(container, bg=bg_color, bd=0, highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=bg_color)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    container.place(relx=relx, rely=rely, relwidth=0.5, relheight=0.5)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame

frame1_content = create_scrollable_frame(root, '#ffcccb', 0, 0)  # Pastel Red
frame2_content = create_scrollable_frame(root, '#aec6cf', 0.5, 0)  # Pastel Blue
frame3_content = create_scrollable_frame(root, '#77dd77', 0, 0.5)  # Pastel Green
frame4_content = create_scrollable_frame(root, '#fdfd96', 0.5, 0.5)  # Pastel Yellow

label1 = tk.Label(frame1_content, text="Urgent & Important", bg='#ffcccb')
label1.pack()

label2 = tk.Label(frame2_content, text="Not Urgent & Important", bg='#aec6cf')
label2.pack()

label3 = tk.Label(frame3_content, text="Urgent & Not Important", bg='#77dd77')
label3.pack()

label4 = tk.Label(frame4_content, text="Not Urgent & Not Important", bg='#fdfd96')
label4.pack()

task_entry = tk.Entry(root)
task_entry.place(relx=0.3, rely=0.95, relwidth=0.4, relheight=0.05)

quadrant_entry = tk.Entry(root)
quadrant_entry.place(relx=0.1, rely=0.95, relwidth=0.1, relheight=0.05)

add_button = tk.Button(root, text="Add Task", command=get_task)
add_button.place(relx=0.75, rely=0.95, relwidth=0.2, relheight=0.05)

# Load tasks when the application starts
load_tasks()

# Bind the close event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
