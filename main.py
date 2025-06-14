import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from prompts import system_prompt
from schemas import available_functions



functions = {"get_file_content": get_file_content,
             "get_files_info": get_files_info,
             "run_python_file": run_python_file,
             "write_file": write_file}

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")


    client = genai.Client(api_key=api_key)
    
    args = sys.argv[1:]

    if not args:
        print("Prompt not given. Exiting program")
        print("\nPlease provide a prompt: python3 main.py 'your prompt'")
        sys.exit(1)
    
    prompt = sys.argv[1]
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    
    verbose = False
    
    if len(args) > 1:
        if args[1] == "--verbose":
            verbose = True

    final_result = generate_content(client, messages, prompt, verbose)
    print("Final response:")
    print(final_result)


def generate_content(client, messages, prompt, verbose):
    for i in range(20):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],
                                               system_instruction=system_prompt)
            )
        for candidate in response.candidates:
            messages.append(candidate.content)
            
        if verbose:
            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls is not None and len(response.function_calls) != 0:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                if not function_call_result.parts[0].function_response.response:
                    raise Exception(f"Error running function {function_call_part.name}")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(function_call_result)

        else:
            break
   
    return response.candidates[0].content.parts[0].text
        
        


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    name = function_call_part.name
    args = function_call_part.args
    args["working_directory"] = "./calculator"
    if name in functions:
        function_result = functions[name](**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )

    
if __name__ == "__main__":
    main()