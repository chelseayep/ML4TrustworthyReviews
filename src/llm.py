
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from pydantic import BaseModel
from typing import List
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
        
    def generate_structured(self, prompt, input_data: str, schema: BaseModel):
        response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "ResponseSchema",
            "schema": schema.model_json_schema()
        }
    }

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
        
        response = self.client.chat_completion(
            messages=messages,
            response_format=response_format,
            model=self.model_name,
        )


        structured_data = response.choices[0].message.content
        return structured_data


paper_text = """
Title: Attention Is All You Need

Abstract: The dominant sequence transduction models are based on complex recurrent 
or convolutional neural networks that include an encoder and a decoder. The best 
performing models also connect the encoder and decoder through an attention mechanism. 
We propose a new simple network architecture, the Transformer, based solely on 
attention mechanisms, dispensing with recurrence and convolutions entirely...
"""

# Define the response format
class PaperAnalysis(BaseModel):
    title: str
    abstract_summary: str


model=Model("meta-llama/llama-4-maverick-17b-128e-instruct")
prompt="You are a helpful assistant that extracts and summarizes key information from academic papers."
result=model.generate_structured(prompt, paper_text, PaperAnalysis)
print(result)