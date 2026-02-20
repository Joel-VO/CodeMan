import ollama
import re

class LLMResponse:
    def __init__(self, model):

        self.SYS_PROMPT = f"""You are a professional coding agent. Default to coding in python unless language is specified.
        Below is relevant documentation that you may or may not use to solve the problem
        
        """
        
        """Rag chunks have to be in format given below:
        chunk1: [docs]
        chunk2: [docs] etc
        """

        self.messages = [{'role': 'system', 'content': self.SYS_PROMPT}]

        self.model_name = model

        try:

            ollama.chat(self.model_name)

        except ollama.ResponseError as e:
            
            print('Error:', e.error)
            if e.status_code == 404:
                try:
                    ollama.pull(self.model_name)
                except:
                    print("Model pull failed, model doesn't exist in the ollama registery.")


    def response(self, usr_prompt):
        
        self.messages.append({'role': 'user', 'content': usr_prompt})
        response = ollama.chat(
            model = self.model_name,
            messages=self.messages
        )

        return response['message']['content'] 

    def get_code(self, response):
        pattern = r"```(\w+)?\s*(.*?)```"
        matches = re.search(pattern, response, re.DOTALL)

        if not matches:
            return None, None

        lang = matches.group(1) or None
        code = matches.group(2).strip()

        return lang, code

# user_prompt = "generate a code for fibonacci series using recurison in python"
# model = LLMResponse(model="qwen2.5-coder:7b")
# out = model.response(user_prompt)
# language, code = model.get_code(out)
# print(code)