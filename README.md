# To-Do List CLI

This is a simple command-line To-Do List application written in Python. The app allows you to manage tasks, set due dates, track task completion, and even export/import tasks using a CSV file.

## Features

- Add, edit, and remove tasks
- Mark tasks as complete and handle recurring tasks
- Search, sort, and filter tasks
- Export tasks to CSV and import tasks from CSV
- Notifications using `plyer`
- Command-line interface using `argparse`
- JSON-based task persistence

## Requirements

To run this application, you need to have Python installed on your system. The required dependencies are listed in the `requirements.txt` file.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/PawiX25/SimpleTodoCLI
   cd SimpleTodoCLI
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

You can run the To-Do List app using the command line:

```bash
python main.py
```

### Example Commands

- Add a task:

  ```bash
  python main.py add "Task description" Medium --due_date 2023-12-31 --category "Work"
  ```

- View tasks:

  ```bash
  python main.py view
  ```

- Complete a task:

  ```bash
  python main.py complete 1
  ```
