
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient

load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")


class Model:
    def __init__(self, model_name=['openai/gpt-oss-20b','meta-llama/llama-4-maverick-17b-128e-instruct' ]):
        self.model_name = model_name
        self.provider = "groq"
        self.client = InferenceClient(provider=self.provider, api_key=os.environ["HF_TOKEN"])
        
    def generate_structured(self, prompt, input_data: str, schema: Optional[BaseModel]):
        messages = [
            {
                "role": "system", 
                "content": prompt
            },
            {
                "role": "user", 
                "content": input_data
            }
        ]

        if schema: 
            response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "ResponseSchema",
                "schema": schema.model_json_schema()
            }}
            
            response = self.client.chat_completion(
                messages=messages,
                response_format=response_format,
                model=self.model_name,
            )
        else:
            response = self.client.chat_completion(
                messages=messages,
                model=self.model_name,
            )


        structured_data = response.choices[0].message.content
        return structured_data


