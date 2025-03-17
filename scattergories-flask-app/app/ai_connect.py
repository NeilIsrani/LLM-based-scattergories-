from flask import json
import openai
from app.config import Config

class AIValidator:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY

    def provide_round_prompts(self):
        """Generate creative and varied Scattergories prompts."""
        prompt = """
        Generate 12 creative and interesting Scattergories prompts. Think outside the box and make them fun and challenging.
        Return the response in this exact JSON format:
        {
            "prompts": [
                {
                    "category": "prompt text",
                    "examples": ["example1", "example2"]
                }
            ]
        }
        
        Be creative with categories - they can be phrases or specific scenarios like:
        - Things you'd find in a superhero's pocket
        - Reasons to be late
        - Things that make you nostalgic
        - What you'd see in a time machine
        
        Make the prompts engaging and entertaining. Each should be clear enough to understand but open to creative answers.
        Respond only with the JSON, no additional text.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": prompt
            }],
            temperature=0.9,
            response_format={ "type": "json_object" }
        )
        
        prompts_data = json.loads(response.choices[0].message.content)
        return prompts_data['prompts']
    
    def validate_answer(self, category, answer, letter):
        """Validate a Scattergories answer."""
        if not answer or not category or not letter:
            return {
                "valid": False,
                "score": 0,
                "reason": "Missing input parameters"
            }

        prompt = f"""
        Validate this Scattergories answer:
        - Category: {category}
        - Answer: {answer}
        - Must start with letter: {letter}

        Return response in this exact JSON format:
        {{
            "valid": boolean,
            "score": number (0 or 1),
            "reason": "explanation string"
        }}

        Rules:
        1. Answer must start with the letter '{letter}' (case insensitive)
        2. Answer must be a real and logical fit for the category
        3. Answer must be specific (no generic terms)
        4. No proper names unless the category specifically asks for them
        
        Respond only with the JSON, no additional text.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": prompt
            }],
            temperature=0.7,
            response_format={ "type": "json_object" }
        )

        # Parse the response to ensure valid JSON
        validation_result = json.loads(response.choices[0].message.content)
        
        # Ensure the response has all required fields
        return {
            "valid": validation_result.get("valid", False),
            "score": validation_result.get("score", 0),
            "reason": validation_result.get("reason", "Invalid response format")
        }