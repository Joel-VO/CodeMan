import ollama

class LlmResponse:
    def __init__(self, sys_prompt, usr_prompt, model=""):
        self.SYS_PROMPT = sys_prompt
        self.USER_PROMPT = usr_prompt
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

    def response():
        response = ollama.chat(
            self.model_name,
            messages=[
                {'role': 'system', 'content': self.SYS_PROMPT},
                {'role': 'user', 'content': self.USER_PROMPT}
            ]
        )

        print(response['message']['content']) # comment this out when testing, this is for debugging only
        
        return response['message']['content'] 
