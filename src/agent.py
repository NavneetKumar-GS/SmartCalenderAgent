from openai import OpenAI
from dotenv import load_dotenv
from tools import Tool_Map, tools
import json
import os
from datetime import datetime


load_dotenv()
client = OpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL"), api_key=os.getenv("OLLAMA_API_KEY")
)


def execute_tool_calls(tools_calls):
    results = []
    for tool_call in tools_calls:
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        if func_name in Tool_Map:
            print(f"{func_name} with {args}")
            output = Tool_Map[func_name](**args)
            # print(func_name)
            # print(Tool_Map.keys())
            results.append(output)
        else:
            results.append(f"{func_name} not found!")
    return results



def chat_with_agent(prompt):

    # today = datetime.now().strftime("%Y-%m-%d")
    response = client.chat.completions.create(
        model="llama3.1",
        messages=[
            {
                "role": "system",
                "content": """You are a Calendar Agent.

Always use tools.

If the user asks to create multiple tasks,
return multiple tool calls.

Never explain your reasoning.

Never output JSON manually.

Only use the provided tools.
                            """
                            },
                            {
                                "role": "user", "content": prompt
                                },
        ],
        tools=tools,
        # tool_choice="auto",
    )

    message = response.choices[0].message

    if message.tool_calls:
        result = execute_tool_calls(message.tool_calls)
        return f"Tool Execution Result: {result}"
    print("Tool Calls:", message.tool_calls)
    print("Finish Reason:", response.choices[0].finish_reason)
    print("Content:", message.content)

    return message.content