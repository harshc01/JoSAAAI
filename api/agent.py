import os
import json
from groq import Groq
from dotenv import load_dotenv
from api.tools import search_allotments, TOOL_DEFINITION

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a JoSAA rank predictor assistant.
Help users find opening and closing ranks for college programs.
Use the search_allotments tool to query the database.
Present results in a clean, round-wise format.


IMPORTANT RULES:
- Use short partial search terms, NOT full names or abbreviations.
  Example: user says "IIT Bombay" → search institute="Bombay"
  Example: user says "NIT Trichy" → search institute="Tiruchirappalli"
  Example: user says "IIT Delhi" → search institute="Delhi"
- For programs use partial terms too:
  "CSE" → program="Computer Science"
  "ECE" → program="Electronics"
  "ME" → program="Mechanical"
- If no results found, try even shorter search terms.
- Data is from JoSAA 2025. No need to ask for year.
- Always present results round-wise with opening and closing ranks.
- If the user query is ambiguous, ask for clarification."""


async def run_agent(user_message: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=[{"type": "function", "function": TOOL_DEFINITION}],
        tool_choice="required",
    )

    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        tool_result = search_allotments(**args)

        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result),
        })

        final = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
        )
        return final.choices[0].message.content

    return message.content