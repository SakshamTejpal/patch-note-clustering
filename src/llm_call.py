from pathlib import Path
from google import genai
from google.genai.types import GenerateContentConfig
import time
from dotenv import load_dotenv
import os
from src.telemetry import log_call

load_dotenv()

def call_gemini(system_prompt: str, user_prompt: str, batch: int) -> str:

    print("Calling Gemini API...")
    full_prompt = system_prompt + "\n" + user_prompt

    # print(os.getenv("API_KEY"))
    start_time = time.time()
    client = genai.Client(api_key=os.getenv("API_KEY"))
    response = client.models.generate_content(
        model ="gemini-2.5-flash",
        contents = user_prompt,
        config = GenerateContentConfig(
            system_instruction= system_prompt
        ),
    )
    latency = time.time() - start_time

    log_call(batch=batch, input_len=len(full_prompt), latency=latency)
    #print(response.text)
    return response.text 

