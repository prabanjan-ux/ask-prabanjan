from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr

load_dotenv()

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

def push(message):
    print(f"Push: {message}")
    payload = {
        "user": pushover_user,
        "token": pushover_token,
        "message": message
    }
    try:
        requests.post(pushover_url, data=payload)
    except Exception as e:
        print("Push error:", e)

def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return {"recorded": "ok"}

tools = [
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": "Store user email for follow-up",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "name": {"type": "string"},
                    "notes": {"type": "string"}
                },
                "required": ["email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_unknown_question",
            "description": "Store unanswered question",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"}
                },
                "required": ["question"]
            }
        }
    }
]

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        func = globals().get(name)
        result = func(**args) if func else {}
        results.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": tool_call.id
        })
    return results

reader = PdfReader("me/linkedin.pdf")
linkedin = "".join([p.extract_text() or "" for p in reader.pages])

with open("me/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()

name = "Prabanjan R"

system_prompt = f"""
You are acting as {name}.

STRICT RULES:
- Only use provided data
- Do NOT hallucinate
- If unknown → say you don't know and call record_unknown_question
- If user shows interest → ask for email and call record_user_details

Summary:
{summary}

LinkedIn:
{linkedin}
"""

MODEL_NAME = "gemini-2.5-flash-lite"

gemini = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY"),
)

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    for _ in range(5):
        response = gemini.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools
        )
        msg = response.choices[0].message
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in msg.tool_calls
                ]
            })
            results = handle_tool_calls(msg.tool_calls)
            messages.extend(results)
            continue
        return msg.content or "I'm here to help with my background and experience."
    return "Something went wrong. Please try again."

with gr.Blocks(title="Prabanjan AI") as demo:

    gr.Markdown(f"""
    # 🤖 {name}
    AI assistant — ask about my projects, skills, and experience.
    """)

    chatbot = gr.Chatbot(height=500)

    msg = gr.Textbox(
        placeholder="Ask something...",
        lines=1
    )

    clear = gr.Button("Clear Chat")

    def respond(message, history):
        if not message.strip():
            return "", history
        reply = chat(message, history)
        history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": reply},
        ]
        return "", history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: ([], ""), outputs=[chatbot, msg])

demo.launch()