from ast import keyword
from multiprocessing.sharedctypes import Value
import os
from typing import List
import openai
from decouple import config
import argparse
import re

API_KEY = config('OPENAI_API_KEY')
MAX_INPUT_LENGTH = 32

def main():
    print('Running Copy Kitt!')

    parser = argparse.ArgumentParser()
    parser.add_argument("--input","-i",type=str, required=True)
    args = parser.parse_args()
    user_input = args.input

    print(f"User input: {user_input}")
    if validate_length(user_input):
        generate_branding_snippet(user_input)
        generate_keywords(user_input)

    else:
        raise ValueError(f"Input length is too long. Must be under {MAX_INPUT_LENGTH}. Submitted input is {user_input}")

def validate_length(prompt: str) -> bool:
    return len(prompt) <= MAX_INPUT_LENGTH

def generate_keywords(prompt: str) -> List[str]:

    # Load API from the environment variable
    openai.api_key = API_KEY

    enriched_prompt= f"Generate related branding keywords for {prompt} "
    print(enriched_prompt)

    response = openai.Completion.create(engine='davinci-instruct-beta-v3',prompt=enriched_prompt, max_tokens=32)

    # Extract Output Text
    Keywords_text: str = response["choices"][0]["text"]

    # Strip whitespace
    Keywords_text = Keywords_text.strip()
    Keywords_array = re.split(",|\n|;|-", Keywords_text)
    Keywords_array = [k.lower().strip() for k in Keywords_array]
    Keywords_array = [k for k in Keywords_array if len(k) > 0]
    
    print(f"Keywords: {Keywords_array}")
    return Keywords_array


def generate_branding_snippet(prompt: str) -> str:
    
    # Load API from the environment variable
    openai.api_key = API_KEY
    enriched_prompt= f"Generate upbeat branding snippet for {prompt} "
    print(enriched_prompt)


    response = openai.Completion.create(engine='davinci-instruct-beta-v3',prompt=enriched_prompt, max_tokens=32)

    # Extract Output Text
    branding_text: str = response["choices"][0]["text"]

    # Strip whitespace
    branding_text = branding_text.strip()
    last_char = branding_text[-1]

    #  Add ... to truncated statements
    if last_char not in {".","!","?"}:
        branding_text += "..."

    print(f"Snippet: {branding_text}")
    return branding_text


if __name__ == "__main__":
    main()