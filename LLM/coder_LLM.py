import ollama
import re

class LLMResponse:
    def __init__(self, sys_prompt, rag_chunks, model="qwen2.5-coder:7b"):

        self.SYS_PROMPT = f"""You are a professional coding agent. 
        Below is relevant documentation that you may or may not use:
        {rag_chunks}
        """
        
        """Rag chunks have to be in format given below:
        chunk1: [docs]
        chunk2: [docs] etc
        """

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
        response = ollama.chat(
            model = self.model_name,
            messages=[
                {'role': 'system', 'content': self.SYS_PROMPT},
                {'role': 'user', 'content': usr_prompt}
            ]
        )

        return response['message']['content'] 

    def get_code(self, response):
        pattern = r"```(\w+)?\s*(.*?)```"
        matches = re.findall(pattern, response, re.DOTALL)

        # print(list(lang for lang, code in matches))
        # print(list(code.strip() for lang, code in matches)[0])

        return [{"language": lang or None, "code": code.strip()} for lang, code in matches]


# user_prompt_out = "write the code for generating fibonacci series.user recursion"

# model = LLMResponse(sys_prompt)
# out = model.response(user_prompt_out)
# model_response_dict = model.get_code(out)

# print(model_response_dict[0]['code']) ## this is the code to use when accessing just the code