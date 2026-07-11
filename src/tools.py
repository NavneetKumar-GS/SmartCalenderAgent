from datetime import datetime, timedelta
import json
import dateparser
from rich.console import Console
from rich.table import Table

console = Console()


def resolved_datetime(str_date, str_time=None):

    if str_time:
        text = f"{str_date} {str_time}"
    else:
        text = str_date

    dt = dateparser.parse(text, settings={"PREFER_DATES_FROM": "future"})

    if dt is None:
        return None, None
    return (dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M"))


def create_task(Title, Date, Time):

    resolved_date, resolved_time = resolved_datetime(Date, Time)

    try:
        with open("Knowledge.json", "r") as f:
            data = json.load(f)
            print(
                f"DEBUG: File load hui, abhi {len(data['tasks'])} tasks hain."
            )  # Ye line zaroori hai
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"tasks": []}
        print("DEBUG: Nayi file bani.")

    new_task = {
        "id": len(data["tasks"]) + 1,
        "Title": Title,
        "Date": resolved_date,
        "Time": resolved_time,
        "Created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    data["tasks"].append(new_task)

    with open("Knowledge.json", "w") as f:
        json.dump(data, f, indent=4)

        return f"Task {Title} created successfully!"


# print(create_Task("haa", "2026-10-02", "11:00 AM"))


def delete_task(title_query):

    task_id = get_task_id(title_query)

    if task_id is None:
        return f"{title_query} not found!"

    with open("Knowledge.json", "r") as f:
        data = json.load(f)

    data["tasks"] = [task for task in data["tasks"] if task["id"] != task_id]

    with open("Knowledge.json", "w") as f:
        json.dump(data, f, indent=4)

    return f"{title_query} deleted successfully!"


# print(delete_task(1))


def delete_all_task():

    with open("Knowledge.json", "r") as f:
        data = json.load(f)

        data["tasks"] = []

        with open("Knowledge.json", "w") as f:
            json.dump(data, f, indent=4)

    return "All task has been deleted!"


def update_task(new_title, new_time, new_date, title_query):

    task_id = get_task_id(title_query)

    if task_id is None:
        return f"Task {title_query} not found!!"

    with open("Knowledge.json", "r") as f:
        data = json.load(f)

    resolved_date, resolved_time = resolved_datetime(new_date, new_time)

    for task in data["tasks"]:
        if task["id"] == task_id:
            if new_title:
                task["Title"] = new_title
            if new_time:
                task["Time"] = resolved_time

            if new_date:
                task["Date"] = resolved_date
            break

    with open("Knowledge.json", "w") as f:
        json.dump(data, f, indent=4)

    return "Task updated successfully!!"


# print(update_task("gym session", 2, 28 , 2 ))


def display_All_task():
    with open("Knowledge.json", "r") as f:
        data = json.load(f)

        tasks = data["tasks"]

        table = Table(title="📋 Your Tasks")

        table.add_column("ID", style="magenta")
        table.add_column("Title", style="cyan")
        table.add_column("Date", style="Green")
        table.add_column("Time", style="Yellow")

        for i, task in enumerate(tasks, start=1):
            table.add_row(str(i), task["Title"], task["Date"], task["Time"])

        console.print(table)
        return "Tasks displayed successfully."


# print(display_All_task())


def get_task_id(title_query):

    print("Searching:", repr(title_query))

    with open("Knowledge.json", "r") as f:
        data = json.load(f)

    for task in data["tasks"]:
        print(task["Title"])

        if title_query.lower() in task["Title"].lower():
            print("Matched")
            return task["id"]

    print("No Match")
    return None


tools = [
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Use this tool to create a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "Title": {"type": "string"},
                    "Date": {"type": "string"},
                    "Time": {"type": "string"},
                },
                "required": ["Title", "Date", "Time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Use this tool to delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "title_query": {
                        "type": "string",
                        "description": "Existing task title or part of the title.",
                    },
                },
                "required": ["title_query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task by searching its title. Do NOT provide task IDs. Pass the task title exactly as mentioned by the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "new_title": {"type": "string"},
                    "new_time": {"type": "string"},
                    "new_date": {"type": "string"},
                    "title_query": {
                        "type": "string",
                        "description": "Title or part of the task title to identify which task should be updated.",
                    },
                },
                "required": ["title_query", "new_title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "display_All_task",
            "description": "Use this tool to display all the task in the list",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_all_task",
            "description": "Use this tool to delete all the task in the list",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
]


Tool_Map = {
    "create_task": create_task,
    "update_task": update_task,
    "delete_task": delete_task,
    "display_All_task": display_All_task,
    "delete_all_task": delete_all_task,
}
