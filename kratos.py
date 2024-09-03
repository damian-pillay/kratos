import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

class Kratos:
    def __init__(self) -> None:
        self._openai_api_key = OPENAI_API_KEY
        self.kratos_model = """
            You are my personal mentor
            You have the overall tone of Kratos from the playstation game god of war: ragnarok.
            You are happy provide me with mentorship and guidance.
            You may address me as Boy when needed.
            Speak concisely and with purpose. Do not say more than that is needed.
            Do not exceed 220 characters with your replies
        """
        openai.api_key = self._openai_api_key

    def get_response(self, prompt):
        '''Gets an ai generated response for user inputed prompt'''   
    
        messages = [
            {"role": "system", "content": self.kratos_model},
            {"role": "user", "content": prompt}
        ]
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # or another model you prefer
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        message = response.choices[0].message.content
        
        return message.strip()