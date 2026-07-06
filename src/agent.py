from openai import OpenAI
from dotenv import load_dotenv
from tools import Tool_Map, tools
import json
import os


load_dotenv()
client = OpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    api_key=os.getenv("OLLAMA_API_KEY")
)


def execute_tool_calls(tools_calls):
    result = []
    for tool_call in tools_calls:
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

    if func_name in Tool_Map:
        print(f"{func_name} with {args}")
        result = Tool_Map[func_name](**args)
        # print(func_name)
        # print(Tool_Map.keys())
        return result
    else:
        return f"Error:Tool {func_name} not found!"


def chat_with_agent(prompt):

    response = client.chat.completions.create(
        model="llama3.1",
        messages=[
            {
                "role": "system",
                "content": "You are a Calendar Agent. You have access to these tools: create_Task, update_task, delete_task, display_All_task, get_task_id. When the user asks to perform an action, you MUST use the correct tool name from this list. Do not respond without a tool name if an action is required.If the user says today, tomorrow or yesterday, pass exactly:today,tomorrow,yesterday, Do not pass phrases like Today (current date"
            },
            {"role": "user", "content": prompt},
        ],
        tools=tools,
        tool_choice="auto",
    )

    message = response.choices[0].message

    if message.tool_calls:
        
        result = execute_tool_calls(message.tool_calls)
        # print(message)
        # print(message.tool_calls)
        return f"Tool Execution Result: {result}"
        
        
    return message.content


