from datetime import datetime, timedelta
import json
import csv
import argparse
from plyer import notification

# File to store tasks
TASKS_FILE = "tasks.json"
CSV_FILE = "tasks.csv"

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
    print("9. Export Tasks to CSV")
    print("10. Import Tasks from CSV")
    print("11. Save and Exit")

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

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

def add_task(tasks, args=None):
    if args:
        task_description = args.description
        task_priority = args.priority.capitalize()
        task_due_date = args.due_date
        task_due_time = args.due_time
        task_recurrence = args.recurrence.capitalize()
        task_category = args.category.capitalize()
        task_notes = args.notes
    else:
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
    send_notification("Task Added", f"Task '{task_description}' has been added to your to-do list.")

def remove_task(tasks, args=None):
    if args:
        task_number = args.task_number
    else:
        view_tasks(tasks)
        if tasks:
            task_number = int(input("Enter the task number to remove: "))
    
    if 1 <= task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        print(f"Task '{removed_task['description']}' removed.")
        send_notification("Task Removed", f"Task '{removed_task['description']}' has been removed from your to-do list.")
    else:
        print("Invalid task number.")

def mark_task_complete(tasks, args=None):
    if args:
        task_number = args.task_number
    else:
        view_tasks(tasks)
        if tasks:
            task_number = int(input("Enter the task number to mark as complete: "))
    
    if 1 <= task_number <= len(tasks):
        task = tasks[task_number - 1]
        task['completed'] = True
        print(f"Task '{task['description']}' marked as complete.")
        send_notification("Task Completed", f"Task '{task['description']}' has been marked as complete.")
        
        # Handle recurrence
        if task['recurrence'] != "None":
            new_due_date = None
            if task['due_date']:
                try:
                    if task['recurrence'] == "Daily":
                        new_due_date = (datetime.strptime(task['due_date'], "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
                    elif task['recurrence'] == "Weekly":
                        new_due_date = (datetime.strptime(task['due_date'], "%Y-%m-%d") + timedelta(weeks=1)).strftime("%Y-%m-%d")
                    elif task['recurrence'] == "Monthly":
                        new_due_date = (datetime.strptime(task['due_date'], "%Y-%m-%d") + timedelta(days=30)).strftime("%Y-%m-%d")
                except ValueError as e:
                    print(f"Error calculating new due date: {e}")
            
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
            send_notification("Recurring Task Added", f"Recurring task '{task['description']}' has been added with new due date {new_due_date}.")
    else:
        print("Invalid task number.")

def edit_task(tasks, args=None):
    if args:
        task_number = args.task_number
        new_description = args.description
        new_priority = args.priority.capitalize()
        new_due_date = args.due_date
        new_due_time = args.due_time
        new_recurrence = args.recurrence.capitalize()
        new_category = args.category.capitalize()
        new_notes = args.notes
    else:
        view_tasks(tasks)
        if tasks:
            task_number = int(input("Enter the task number to edit: "))
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
    send_notification("Task Updated", f"Task '{tasks[task_number - 1]['description']}' has been updated.")

def search_tasks(tasks, args=None):
    if args:
        keyword = args.keyword.lower()
    else:
        keyword = input("Enter a keyword to search for: ").lower()
    
    matching_tasks = [task for task in tasks if keyword in task['description'].lower()]
    if matching_tasks:
        print("\nSearch Results:")
        view_tasks(matching_tasks)
    else:
        print("\nNo tasks found matching the keyword.")

def sort_tasks(tasks, args=None):
    if args:
        choice = args.choice
    else:
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

def filter_tasks(tasks, args=None):
    if args:
        choice = args.choice
    else:
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

def export_tasks_to_csv(tasks):
    with open(CSV_FILE, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Description", "Priority", "Completed", "Due Date", "Due Time", "Recurrence", "Category", "Notes"])
        for task in tasks:
            writer.writerow([
                task['description'],
                task['priority'],
                task['completed'],
                task['due_date'],
                task['due_time'],
                task['recurrence'],
                task['category'],
                task['notes']
            ])
    print(f"Tasks exported to {CSV_FILE}.")
    send_notification("Tasks Exported", f"Tasks have been exported to {CSV_FILE}.")

def import_tasks_from_csv(tasks):
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks.append({
                    'description': row['Description'],
                    'priority': row['Priority'],
                    'completed': row['Completed'] == 'True',
                    'due_date': row['Due Date'] if row['Due Date'] else None,
                    'due_time': row['Due Time'] if row['Due Time'] else None,
                    'recurrence': row['Recurrence'],
                    'category': row['Category'],
                    'notes': row['Notes']
                })
        print(f"Tasks imported from {CSV_FILE}.")
        send_notification("Tasks Imported", f"Tasks have been imported from {CSV_FILE}.")
    except FileNotFoundError:
        print(f"{CSV_FILE} not found.")

def main():
    parser = argparse.ArgumentParser(description="Simple To-Do List CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a task")
    parser_add.add_argument("description", type=str, help="Task description")
    parser_add.add_argument("priority", type=str, choices=["High", "Medium", "Low"], help="Task priority")
    parser_add.add_argument("--due_date", type=str, help="Task due date (YYYY-MM-DD)", default=None)
    parser_add.add_argument("--due_time", type=str, help="Task due time (HH:MM)", default=None)
    parser_add.add_argument("--recurrence", type=str, choices=["None", "Daily", "Weekly", "Monthly"], help="Task recurrence", default="None")
    parser_add.add_argument("--category", type=str, help="Task category", default="No category")
    parser_add.add_argument("--notes", type=str, help="Additional notes", default="No notes")

    # Remove command
    parser_remove = subparsers.add_parser("remove", help="Remove a task")
    parser_remove.add_argument("task_number", type=int, help="Task number to remove")

    # Complete command
    parser_complete = subparsers.add_parser("complete", help="Mark a task as complete")
    parser_complete.add_argument("task_number", type=int, help="Task number to mark as complete")

    # Edit command
    parser_edit = subparsers.add_parser("edit", help="Edit a task")
    parser_edit.add_argument("task_number", type=int, help="Task number to edit")
    parser_edit.add_argument("description", type=str, help="New task description")
    parser_edit.add_argument("priority", type=str, choices=["High", "Medium", "Low"], help="New task priority")
    parser_edit.add_argument("--due_date", type=str, help="New task due date (YYYY-MM-DD)", default=None)
    parser_edit.add_argument("--due_time", type=str, help="New task due time (HH:MM)", default=None)
    parser_edit.add_argument("--recurrence", type=str, choices=["None", "Daily", "Weekly", "Monthly"], help="New task recurrence", default="None")
    parser_edit.add_argument("--category", type=str, help="New task category", default="No category")
    parser_edit.add_argument("--notes", type=str, help="New additional notes", default="No notes")

    # Search command
    parser_search = subparsers.add_parser("search", help="Search tasks")
    parser_search.add_argument("keyword", type=str, help="Keyword to search for")

    # Sort command
    parser_sort = subparsers.add_parser("sort", help="Sort tasks")
    parser_sort.add_argument("choice", type=str, choices=["priority", "completion", "due_date"], help="Sort choice")

    # Filter command
    parser_filter = subparsers.add_parser("filter", help="Filter tasks")
    parser_filter.add_argument("choice", type=str, choices=["completed", "incomplete", "priority", "overdue"], help="Filter choice")

    # Export command
    parser_export = subparsers.add_parser("export", help="Export tasks to CSV")

    # Import command
    parser_import = subparsers.add_parser("import", help="Import tasks from CSV")

    # View command
    parser_view = subparsers.add_parser("view", help="View tasks")

    args = parser.parse_args()

    tasks = load_tasks()

    if args.command == "add":
        add_task(tasks, args)
    elif args.command == "remove":
        remove_task(tasks, args)
    elif args.command == "complete":
        mark_task_complete(tasks, args)
    elif args.command == "edit":
        edit_task(tasks, args)
    elif args.command == "search":
        search_tasks(tasks, args)
    elif args.command == "sort":
        sort_tasks(tasks, args)
    elif args.command == "filter":
        filter_tasks(tasks, args)
    elif args.command == "export":
        export_tasks_to_csv(tasks)
    elif args.command == "import":
        import_tasks_from_csv(tasks)
    elif args.command == "view":
        view_tasks(tasks)
    else:
        while True:
            display_menu()
            choice = input("\nEnter your choice (1-11): ")
            
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
                export_tasks_to_csv(tasks)
            elif choice == '10':
                import_tasks_from_csv(tasks)
            elif choice == '11':
                save_tasks(tasks)
                print("Tasks saved. Exiting the to-do list app. Goodbye!")
                send_notification("Tasks Saved", "Tasks have been saved. Exiting the to-do list app. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 11.")

if __name__ == "__main__":
    main()