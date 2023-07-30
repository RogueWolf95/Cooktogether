import openai

class OpenAIManager:
    def __init__(self):
        self.language_models = ["gpt-3.5-turbo", "gpt-4"]
        self.max_tokens = 1000


    def generate_response(self, messages:list[dict], token_limit:int, model:int=0) -> str:
        response = openai.ChatCompletion.create(
            model=self.language_models[model],  # Using GPT-3.5-turbo by default
            messages=messages,
            max_tokens=token_limit + (token_limit * model)  # Maximum length of the output
        )
        return response