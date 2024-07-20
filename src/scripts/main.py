import tkinter as tk
import json
import os

# Define global variables for frames and task file
frame1_content = None
frame2_content = None
frame3_content = None
frame4_content = None
TASKS_FILE = 'src/support_files/tasks.json'

# Function to add a task to a specific frame
def add_task(frame, task, quadrant):
    task_frame = tk.Frame(frame)
    task_frame.pack(fill=tk.X, pady=2)  # Add padding between tasks

    task_label = tk.Label(task_frame, text=task, bg="lightgrey", relief="raised", padx=5, pady=5)
    task_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    delete_button = tk.Button(task_frame, text="Delete", command=lambda: remove_task(task_frame))
    delete_button.pack(side=tk.RIGHT, padx=5)

    save_tasks()

# Function to remove a task from a specific frame
def remove_task(task_frame):
    task_frame.destroy()
    save_tasks()

# Function to save tasks to a file
def save_tasks():
    tasks = {1: [], 2: [], 3: [], 4: []}
    for frame, quadrant in zip((frame1_content, frame2_content, frame3_content, frame4_content), range(1, 5)):
        for task_frame in frame.winfo_children():
            if isinstance(task_frame, tk.Frame):
                task_label = task_frame.winfo_children()[0]
                tasks[quadrant].append(task_label.cget("text"))

    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

# Function to load tasks from a file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            tasks = json.load(file)

        for quadrant, tasks_list in tasks.items():
            quadrant = int(quadrant)
            frame = [frame1_content, frame2_content, frame3_content, frame4_content][quadrant - 1]
            for task in tasks_list:
                add_task(frame, task, quadrant)

# Function to handle adding a task from user input
def add_task_from_input():
    task = task_entry.get()
    if not task:
        return

    selected_quadrant = quadrant_var.get()
    frame = [frame1_content, frame2_content, frame3_content, frame4_content][selected_quadrant - 1]

    add_task(frame, task, selected_quadrant)

    # Clear the task entry field
    task_entry.delete(0, tk.END)

def main():
    global frame1_content, frame2_content, frame3_content, frame4_content
    global task_entry, quadrant_var

    root = tk.Tk()
    root.title("Eisenhower Matrix")

    # Set the window size (width x height)
    root.geometry("800x600")  # Adjust as needed

    # Create a container frame for the quadrants and the input area
    container = tk.Frame(root)
    container.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create frames for each quadrant
    frame1_content = tk.Frame(container, bg='#ffcccb', width=200, height=300)
    frame1_content.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    frame2_content = tk.Frame(container, bg='#aec6cf', width=200, height=300)
    frame2_content.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    frame3_content = tk.Frame(container, bg='#77dd77', width=200, height=300)
    frame3_content.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    frame4_content = tk.Frame(container, bg='#fdfd96', width=200, height=300)
    frame4_content.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # Configure grid weights for responsive layout
    container.grid_rowconfigure(0, weight=1)
    container.grid_rowconfigure(1, weight=1)
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    # Add titles to the frames
    tk.Label(frame1_content, text="Urgent & Important", bg='#ffcccb', font=('Arial', 12, 'bold')).pack()
    tk.Label(frame2_content, text="Not Urgent & Important", bg='#aec6cf', font=('Arial', 12, 'bold')).pack()
    tk.Label(frame3_content, text="Urgent & Not Important", bg='#77dd77', font=('Arial', 12, 'bold')).pack()
    tk.Label(frame4_content, text="Not Urgent & Not Important", bg='#fdfd96', font=('Arial', 12, 'bold')).pack()

    # Add task input area at the bottom of the container
    input_frame = tk.Frame(root)
    input_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)

    task_entry = tk.Entry(input_frame, width=40)
    task_entry.pack(side=tk.LEFT, padx=5)

    quadrant_var = tk.IntVar(value=1)
    for i, text in enumerate([
        "Urgent & Important",
        "Not Urgent & Important",
        "Urgent & Not Important",
        "Not Urgent & Not Important"
    ], start=1):
        tk.Radiobutton(input_frame, text=text, variable=quadrant_var, value=i).pack(side=tk.LEFT, padx=5)

    add_task_button = tk.Button(input_frame, text="Add Task", command=add_task_from_input)
    add_task_button.pack(side=tk.LEFT, padx=5)

    # Load existing tasks
    load_tasks()

    root.mainloop()

if __name__ == "__main__":
    main()
