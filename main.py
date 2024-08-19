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
    print("6. Search Tasks")
    print("7. Sort Tasks")
    print("8. Filter Tasks")
    print("9. Save and Exit")

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

def search_tasks(tasks):
    keyword = input("Enter a keyword to search for: ").lower()
    matching_tasks = [task for task in tasks if keyword in task['description'].lower()]
    if matching_tasks:
        print("\nSearch Results:")
        view_tasks(matching_tasks)
    else:
        print("\nNo tasks found matching the keyword.")

def sort_tasks(tasks):
    print("\nSort Tasks:")
    print("1. By Priority")
    print("2. By Completion Status")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        tasks.sort(key=lambda x: x['priority'])
        print("\nTasks sorted by priority.")
    elif choice == '2':
        tasks.sort(key=lambda x: x['completed'])
        print("\nTasks sorted by completion status.")
    else:
        print("Invalid choice. Please enter 1 or 2.")

def filter_tasks(tasks):
    print("\nFilter Tasks:")
    print("1. View Completed Tasks")
    print("2. View Incomplete Tasks")
    print("3. View Tasks by Priority")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        filtered_tasks = [task for task in tasks if task['completed']]
        view_tasks(filtered_tasks)
    elif choice == '2':
        filtered_tasks = [task for task in tasks if not task['completed']]
        view_tasks(filtered_tasks)
    elif choice == '3':
        priority = input("Enter priority to filter by (High, Medium, Low): ").capitalize()
        filtered_tasks = [task for task in tasks if task['priority'] == priority]
        view_tasks(filtered_tasks)
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

def main():
    tasks = load_tasks()
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-9): ")
        
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
            search_tasks(tasks)
        elif choice == '7':
            sort_tasks(tasks)
        elif choice == '8':
            filter_tasks(tasks)
        elif choice == '9':
            save_tasks(tasks)
            print("Tasks saved. Exiting the to-do list app. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()
