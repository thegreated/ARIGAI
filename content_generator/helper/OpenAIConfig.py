import os
from openai import OpenAI

import json
import time
class OpenAIConfig:


    @staticmethod
    def  generateContent(prompt,article_body):
        token = os.getenv("API_KEY")
        endpoint = "https://models.github.ai/inference"
        model_name = "openai/gpt-4o"

        client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant the revised the document and return as JSON",
                },
                {
                    "role": "user",
                    "content": prompt + article_body,
                }
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )

        openai_revised_body = response.choices[0].message.content

        # Clean the string to remove code block formatting if present
        cleaned_body = openai_revised_body.strip()

        if cleaned_body.startswith("```"):
            # Remove ```json or ``` if present
            cleaned_body = cleaned_body.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        # Now safely load the JSON
        try:
            data = json.loads(cleaned_body)
            return data  # or return json.dumps(data, indent=2) if needed as a string
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print("Raw content:", repr(openai_revised_body))
            raise

