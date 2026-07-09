from datetime import datetime
import json
import dateparser
from rich.console import Console
from rich.table import Table

console = Console()

def normalized_parser(value, mode):

    parsed = dateparser.parse(value)

    if parsed is None:
        return value

    if mode == "date":
        return parsed.strftime("%Y-%m-%d")

    elif mode == "time":
        return parsed.strftime("%I:%M %p")

def create_task(Title, Date, Time):

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
        "Date": normalized_parser(Date,"date"),
        "Time": normalized_parser(Time, "time"),
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

    data["tasks"] = [
        task for task in data["tasks"]
        if task["id"] != task_id
    ]

    with open("Knowledge.json", "w") as f:
        json.dump(data, f, indent=4)

    return f"{title_query} deleted successfully!"


# print(delete_task(1))


def update_task(new_title, new_time, new_date,  title_query):

    task_id = get_task_id(title_query)

    if task_id is None:
        return f"Task {title_query} not found!!"

    with open("Knowledge.json", "r") as f:
        data = json.load(f)

    
    
    for task in data["tasks"]:
        if task["id"] == task_id:
            if new_title:
                task["Title"] = new_title
            if new_time:
                task["Time"] = normalized_parser(new_time,"time")

            if new_date:
                task["Date"] = normalized_parser(new_date,"date")
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
        table.add_column("Title" , style="cyan")
        table.add_column("Date" , style="Green")
        table.add_column("Time" , style="Yellow")


        for i, task in enumerate(tasks , start=1):
            table.add_row(
                str(i),
                task["Title"],
                task["Date"],
                task["Time"]
            )

        console.print(table)
        return "Tasks displayed successfully."

# print(display_All_task())


def get_task_id(title_query):
    tasks = display_All_task()
    for task in tasks:
        if title_query.lower() in task["Title"].lower():
            return task["id"]
        
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
                "properties": {"title_query": {"type": "integer"}},
                "required": ["title_query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Use this tool to update a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "new_title": {"type": "string"},
                    "new_time": {"type": "string"},
                    "new_date": {"type": "string"},
                    "title_query": {"type": "integer"},
                },
                "required": ["new_title", "new_date", "new_time", "title_query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "display_All_task",
            "description": "Use this tool to display all the task in the list",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_task_id",
            "description": "Use this to find the ID of a task by its name.",
            "parameters": {
                "type": "object",
                "properties": {"title_query": {"type": "string"}},
                "required": ["title_query"],
            },
        },
    },
]


Tool_Map = {
    "create_task": create_task,
    "update_task": update_task,
    "delete_task": delete_task,
    "display_All_task": display_All_task,
    "get_task_id": get_task_id,
}
