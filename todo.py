from task import Task
from datetime import datetime
import json

# Global list to store tasks
tasks = []

# add tasks
def add_task(description):
    priority = input("Enter task priority (Low, Medium, High, default is Medium): ").strip().capitalize()
    
    if priority not in ["Low", "Medium", "High"]:
        print("Invalid priority, setting to default (Medium).")
        priority = "Medium"
    
    # Ask for deadline input
    deadline_input = input("Enter deadline (YYYY-MM-DD) or press Enter to skip: ").strip()

    if deadline_input:
        try:
            # Parse the input date into a datetime object
            deadline = datetime.strptime(deadline_input, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Setting deadline to None.")
            deadline = None
    else:
        deadline = None

    task = Task(description, priority=priority, deadline=deadline)
    tasks.append(task)
    save_tasks_to_file()  # Save the tasks after adding a new one
    return f'Task "{description}" added with priority {priority} and deadline {deadline_input if deadline else "None"}.'



def list_tasks():
    if not tasks:
        return "No tasks available."
    else:
        task_list = ""
        today = datetime.now()  # Get the current date and time

        for index, task in enumerate(tasks, start=1):
            status = "[✓]" if task.completed else "[✗]"
            deadline_str = task.deadline.strftime('%Y-%m-%d') if task.deadline else "No deadline"
            overdue_warning = ""

            # Check if the task is overdue
            if task.deadline and task.deadline < today and not task.completed:
                overdue_warning = " (OVERDUE!)"
            
            task_list += f"{index}. {task.description} {status} (Priority: {task.priority}) Deadline: {deadline_str}{overdue_warning}\n"

        return task_list.strip()  # Strip the last newline


#delete
def delete_task(task_number):
    try:
        task = tasks.pop(task_number - 1)
        return f'Task "{task.description}" deleted.'
    except IndexError:
        return "Invalid task number."
    
#Mark Complete
def mark_task_complete(task_number):
    try:
        task = tasks[task_number - 1]
        if task.completed:
            return f'Task "{task.description}" is already completed.'
        task.mark_complete()
        return f'Task "{task.description}" marked as complete.'
    except IndexError:
        return "Invalid task number."


def save_tasks_to_file(file_name='tasks.json'):
    with open(file_name, 'w') as file:
        task_data = [
            {
                'description': task.description, 
                'completed': task.completed, 
                'priority': task.priority,
                'deadline': task.deadline.strftime('%Y-%m-%d') if task.deadline else None
            } for task in tasks
        ]
        json.dump(task_data, file)


def load_tasks_from_file(file_name='tasks.json'):
    try:
        with open(file_name, 'r') as file:
            task_data = json.load(file)
            for task in task_data:
                # Handle cases where the 'deadline' key might be missing in older files
                deadline_str = task.get('deadline')  
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d') if deadline_str else None
                
                # Initialize Task object with loaded data
                loaded_task = Task(
                    task['description'],
                    priority=task.get('priority', 'Medium'),  # Default to 'Medium' if missing
                    deadline=deadline
                )
                loaded_task.completed = task.get('completed', False)  
                tasks.append(loaded_task)  
    except FileNotFoundError:
        # If the file doesn't exist, we start with an empty task list
        pass




# CLI logic moved to a separate function for manual usage
def run_cli():
    while True:
        print("\nCommands: add, list, complete, delete, quit")
        command = input("Enter command: ").strip().lower()

        if command == "add":
            task_desc = input("Enter task description: ").strip()
            print(add_task(task_desc))
        elif command == "list":
            print(list_tasks())
        elif command == "complete":
            task_number = int(input("Enter task number to mark complete: ").strip())
            print(mark_task_complete(task_number))
        elif command == "delete":
            task_number = int(input("Enter task number to delete: ").strip())
            print(delete_task(task_number))
        elif command == "quit":
            break
        else:
            print("Invalid command.")
            
if __name__ == "__main__":
    load_tasks_from_file()
    run_cli()
