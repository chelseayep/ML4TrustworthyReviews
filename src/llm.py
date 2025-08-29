
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
import os
import re
import json
import ast
from huggingface_hub import InferenceClient

from transformers import pipeline
from pydantic import BaseModel
from typing import Optional
import json

import torch

load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")


class InferenceModel:
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


        data = response.choices[0].message.content
        structured_data = json.loads(data)  # Validate JSON format
        return structured_data


device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
class Model:
    def __init__(self, model_name=["Qwen/Qwen2.5-VL-3B-Instruct", "mistralai/Mistral-7B-Instruct-v0.2", "google/gemma-3-1b-it"]):
        """
        model_name: Hugging Face model ID to load locally
        device: -1 for CPU, 0 for GPU
        """
        self.model_name = model_name
        self.generator = pipeline("text-generation", model=self.model_name, device=-1)

    def generate_structured(self, prompt: str, input_data: str, schema: Optional[BaseModel] = None):
        # Compose prompt (since pipeline doesn't use "messages" format natively)
        full_prompt = f"System: {prompt}\nUser: {input_data}\nAssistant:"

        response = self.generator(
            full_prompt,
            max_new_tokens=512,
            temperature=0.0,
            do_sample=False,
            truncation=True,
        )

        # Extract generated text
        raw=response[0]['generated_text']
        output_text = response[0]['generated_text'].split("Assistant:")[-1].strip()
        # print("Processed output text:", output_text)

        if schema:
            structured_data = self.extract_json(output_text.strip())
            if structured_data is None:
                print("No JSON object found in output, response: ", raw)
                return {} # Return empty schema instance if no JSON found
            return structured_data
        
           
        else:
            return output_text
    



    @staticmethod
    def extract_json(text: str) -> dict:
        """
        Extract JSON object from text, handling fenced code blocks if present.
        """
        
        # # If no fences or fenced content failed, try to find a {...} JSON block
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            candidate = json_match.group(0)
            # print("Extracted candidate JSON:", candidate)
            return ast.literal_eval(candidate)
            # except json.JSONDecodeError:
            #     pass
        
        # If both methods fail, raise an error with both original and extracted text for debugging
        else:
            return None

