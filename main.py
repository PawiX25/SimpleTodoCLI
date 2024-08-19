import json

# File to store tasks
TASKS_FILE = "tasks.json"

def display_menu():
    print("\nTo-Do List Menu:")
    print("1. View To-Do List")
    print("2. Add Task")
    print("3. Remove Task")
    print("4. Mark Task as Complete")
    print("5. Edit Task")
    print("6. Save and Exit")

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def view_tasks(tasks):
    if not tasks:
        print("\nYour to-do list is empty.")
    else:
        print("\nTo-Do List:")
        for index, task in enumerate(tasks, start=1):
            status = "✔" if task['completed'] else "✖"
            print(f"{index}. [{status}] {task['description']} (Priority: {task['priority']})")

def add_task(tasks):
    task_description = input("Enter the task description: ")
    task_priority = input("Enter the task priority (High, Medium, Low): ").capitalize()
    tasks.append({'description': task_description, 'priority': task_priority, 'completed': False})
    print(f"Task '{task_description}' added.")

def remove_task(tasks):
    view_tasks(tasks)
    if tasks:
        try:
            task_number = int(input("Enter the task number to remove: "))
            if 1 <= task_number <= len(tasks):
                removed_task = tasks.pop(task_number - 1)
                print(f"Task '{removed_task['description']}' removed.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")

def mark_task_complete(tasks):
    view_tasks(tasks)
    if tasks:
        try:
            task_number = int(input("Enter the task number to mark as complete: "))
            if 1 <= task_number <= len(tasks):
                tasks[task_number - 1]['completed'] = True
                print(f"Task '{tasks[task_number - 1]['description']}' marked as complete.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")

def edit_task(tasks):
    view_tasks(tasks)
    if tasks:
        try:
            task_number = int(input("Enter the task number to edit: "))
            if 1 <= task_number <= len(tasks):
                new_description = input("Enter the new task description: ")
                new_priority = input("Enter the new task priority (High, Medium, Low): ").capitalize()
                tasks[task_number - 1]['description'] = new_description
                tasks[task_number - 1]['priority'] = new_priority
                print(f"Task '{tasks[task_number - 1]['description']}' updated.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    tasks = load_tasks()
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            remove_task(tasks)
        elif choice == '4':
            mark_task_complete(tasks)
        elif choice == '5':
            edit_task(tasks)
        elif choice == '6':
            save_tasks(tasks)
            print("Tasks saved. Exiting the to-do list app. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
