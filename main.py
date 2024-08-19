import json
from datetime import datetime, timedelta

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
            due_date = task['due_date'] if task['due_date'] else "No due date"
            due_time = task['due_time'] if task['due_time'] else "No due time"
            recurrence = task['recurrence'] if task['recurrence'] else "No recurrence"
            category = task['category'] if task['category'] else "No category"
            notes = task['notes'] if task['notes'] else "No notes"
            print(f"{index}. [{status}] {task['description']} (Priority: {task['priority']}, Due: {due_date} {due_time}, Recurrence: {recurrence}, Category: {category}, Notes: {notes})")

def add_task(tasks):
    task_description = input("Enter the task description: ")
    task_priority = input("Enter the task priority (High, Medium, Low): ").capitalize()
    task_due_date = input("Enter the task due date (YYYY-MM-DD) or press Enter to skip: ")
    task_due_time = input("Enter the task due time (HH:MM) or press Enter to skip: ")
    task_recurrence = input("Enter the task recurrence (None, Daily, Weekly, Monthly): ").capitalize()
    task_category = input("Enter the task category (e.g., Work, Personal, Shopping): ").capitalize()
    task_notes = input("Enter any additional notes for the task: ")
    
    # Validate date format
    if task_due_date:
        try:
            datetime.strptime(task_due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Task added without due date.")
            task_due_date = None
    else:
        task_due_date = None
    
    # Validate time format
    if task_due_time:
        try:
            datetime.strptime(task_due_time, "%H:%M")
        except ValueError:
            print("Invalid time format. Task added without due time.")
            task_due_time = None
    else:
        task_due_time = None
    
    tasks.append({
        'description': task_description,
        'priority': task_priority,
        'completed': False,
        'due_date': task_due_date,
        'due_time': task_due_time,
        'recurrence': task_recurrence,
        'category': task_category,
        'notes': task_notes
    })
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
                task = tasks[task_number - 1]
                task['completed'] = True
                print(f"Task '{task['description']}' marked as complete.")
                
                # Handle recurrence
                if task['recurrence'] != "None":
                    new_due_date = None
                    if task['recurrence'] == "Daily":
                        new_due_date = (datetime.strptime(task['due_date'], "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
                    elif task['recurrence'] == "Weekly":
                        new_due_date = (datetime.strptime(task['due_date'], "%Y-%m-%d") + timedelta(weeks=1)).strftime("%Y-%m-%d")
                    elif task['recurrence'] == "Monthly":
                        new_due_date = (datetime.strptime(task['due_date'], "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d")
                    
                    tasks.append({
                        'description': task['description'],
                        'priority': task['priority'],
                        'completed': False,
                        'due_date': new_due_date,
                        'due_time': task['due_time'],
                        'recurrence': task['recurrence'],
                        'category': task['category'],
                        'notes': task['notes']
                    })
                    print(f"Recurring task '{task['description']}' added with new due date {new_due_date}.")
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
                new_due_date = input("Enter the new task due date (YYYY-MM-DD) or press Enter to keep the current due date: ")
                new_due_time = input("Enter the new task due time (HH:MM) or press Enter to keep the current due time: ")
                new_recurrence = input("Enter the new task recurrence (None, Daily, Weekly, Monthly): ").capitalize()
                new_category = input("Enter the new task category (e.g., Work, Personal, Shopping): ").capitalize()
                new_notes = input("Enter the new task notes: ")
                
                # Validate date format
                if new_due_date:
                    try:
                        datetime.strptime(new_due_date, "%Y-%m-%d")
                    except ValueError:
                        print("Invalid date format. Keeping the current due date.")
                        new_due_date = tasks[task_number - 1]['due_date']
                
                # Validate time format
                if new_due_time:
                    try:
                        datetime.strptime(new_due_time, "%H:%M")
                    except ValueError:
                        print("Invalid time format. Keeping the current due time.")
                        new_due_time = tasks[task_number - 1]['due_time']
                
                tasks[task_number - 1]['description'] = new_description
                tasks[task_number - 1]['priority'] = new_priority
                tasks[task_number - 1]['due_date'] = new_due_date
                tasks[task_number - 1]['due_time'] = new_due_time
                tasks[task_number - 1]['recurrence'] = new_recurrence
                tasks[task_number - 1]['category'] = new_category
                tasks[task_number - 1]['notes'] = new_notes
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
    print("3. By Due Date")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        tasks.sort(key=lambda x: x['priority'])
        print("\nTasks sorted by priority.")
    elif choice == '2':
        tasks.sort(key=lambda x: x['completed'])
        print("\nTasks sorted by completion status.")
    elif choice == '3':
        tasks.sort(key=lambda x: x['due_date'] if x['due_date'] else '')
        print("\nTasks sorted by due date.")
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

def filter_tasks(tasks):
    print("\nFilter Tasks:")
    print("1. View Completed Tasks")
    print("2. View Incomplete Tasks")
    print("3. View Tasks by Priority")
    print("4. View Overdue Tasks")
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
    elif choice == '4':
        today = datetime.now().strftime("%Y-%m-%d")
        filtered_tasks = [task for task in tasks if task['due_date'] and task['due_date'] < today]
        view_tasks(filtered_tasks)
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

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
