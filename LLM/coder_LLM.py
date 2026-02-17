import ollama
import re

class LLMResponse:
    def __init__(self, sys_prompt, model="qwen2.5-coder:7b"):
        self.SYS_PROMPT = sys_prompt
        self.model_name = model

        try:
            ollama.chat(self.model_name)
            print("Loaded model")
        except ollama.ResponseError as e:
            print('Error:', e.error)
            if e.status_code == 404:
                try:
                    ollama.pull(self.model_name)
                except:
                    print("Model pull failed, model doesn't exist in the ollama registery.")

    def response(self, usr_prompt):
        response = ollama.chat(
            model = self.model_name,
            messages=[
                {'role': 'system', 'content': self.SYS_PROMPT},
                {'role': 'user', 'content': usr_prompt}
            ]
        )

        # print(response['message']['content']) # comment this out when testing, this is for debugging only
        return response['message']['content'] 

    def get_code(self, response):
        pattern = r"```(\w+)?\s*(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)

        # print(list(lang for lang, code in matches))
        # print(list(code.strip() for lang, code in matches)[0])

        return [{"language": lang or None, "code": code.strip()} for lang, code in matches]


# sys_prompt = "You are a profession coder"
# user_prompt_out = "write the code for generating fibonacci series.user recursion"

# model = LLMResponse(sys_prompt)
# out = model.response(user_prompt_out)
# model.get_code(out)