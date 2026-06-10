import os
import argparse
from call_function import available_functions, call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

load_dotenv()
model_name = 'gemini-2.5-flash'
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--dir", type=str, default="./calculator")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

for _ in range(20):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    
    # Bước 2: thêm candidates vào messages
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    # Bước 4: không có function call → LLM đã có final response
    if not response.function_calls:
        print("Final response:")
        if response.text:
            print(response.text)
        elif response.candidates:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.text:
                            print(part.text)
        break

    # Bước 3: gọi từng function, collect results
    function_responses = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, args.verbose, args.dir)

        if not function_call_result.parts:
            raise Exception("No parts in function call result")
        if function_call_result.parts[0].function_response is None:
            raise Exception("No function response in parts")
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("No response in function response")

        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        function_responses.append(function_call_result.parts[0])

    # Append tool responses vào messages
    messages.append(types.Content(role="user", parts=function_responses))

else:
    # Bước 5: hết 20 vòng vẫn chưa xong
    print("Agent reached maximum iterations without a final response")
    exit(1)