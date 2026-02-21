from LLM.coder_LLM import LLMResponse
from Docker.docker_runtime import DockerRuntime
import os
import ollama


LANG_MAP = {
    # Python family
    "python": "py",
    "py": "py",

    # C family
    "c": "c",
    "cpp": "cpp",
    "c++": "cpp",
    "cc": "cpp",
    "cxx": "cpp",
    # "h": "h",
    # "hpp": "hpp",

    # # Java / JVM
    # "java": "java",
    # "kotlin": "kt",
    # "kt": "kt",
    # "scala": "scala",
    # "groovy": "groovy",

    # # JavaScript ecosystem
    # "javascript": "js",
    # "js": "js",
    # "typescript": "ts",
    # "ts": "ts",
    # "node": "js",

    # # Web
    # "html": "html",
    # "css": "css",
    # "scss": "scss",
    # "sass": "sass",
    # "json": "json",
    # "xml": "xml",

    # # Systems / modern
    "rust": "rs",
    # "go": "go",
    # "golang": "go",
    # "zig": "zig",
    # "nim": "nim",

    # # Scripting
    # "bash": "sh",
    # "sh": "sh",
    # "zsh": "sh",
    # "powershell": "ps1",
    # "ps": "ps1",

    # # Backend / scripting
    # "php": "php",
    # "ruby": "rb",
    # "rb": "rb",
    # "perl": "pl",

    # # Functional
    # "haskell": "hs",
    # "hs": "hs",
    # "clojure": "clj",
    # "elixir": "ex",
    # "erlang": "erl",

    # # SQL
    # "sql": "sql",

    # # Shell config / infra
    # "dockerfile": "dockerfile",
    # "yaml": "yaml",
    # "yml": "yml",
    # "toml": "toml",
    # "ini": "ini",

    # # Assembly
    # "asm": "asm",
    # "assembly": "asm",

    # # C#
    # "csharp": "cs",
    # "c#": "cs"
}

class CodeMan:
    def __init__(self):
        self.code_gen_counter = 0
        self.user_prompt = ""
        self.model = None
        self.lang = ""
        self.dir = "Snippets"
        self._initialize_model()

    def _initialize_model(self, model_name = "qwen2.5-coder:7b"):
        self.model = LLMResponse(model=model_name)

    def _model_release(self):
        self.model = None

    def _rag_orchestration(self):
        # logic for how rag will have certain logic given here and use that for the next sections
        pass
    
    def _docker_orchestration(self):
        # run docker cyclically to give an o/p and then if errors are there, clean o/p and pass back to model.
        pass

    def user_prompt_init(self, user_prompt_out):
        self.user_prompt = user_prompt_out

    def change_model(self):
        self._model_release()
        models_available = ollama.list()
        print(f"Available models are {models_available}")
        model_name = input("Enter Model name: ")
        try:
            self.model = LLMResponse(model=model_name)
        except:
            print("Improper model chosen, kindly select a model that exists")
            self.change_model()

    def generate_code(self):
        if self.model == None:
            self._initialize_model()

        out = self.model.response(self.user_prompt)
        language, code = self.model.get_code(out)
        self.lang = LANG_MAP.get(language.lower(), "txt") if language else "txt"

        os.makedirs(self.dir, exist_ok=True)
        filename = f"script_{self.code_gen_counter}.{self.lang.lstrip('.')}"
        path = os.path.join(self.dir, filename)
        # print(f"Code is {code}")

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        self.code_gen_counter += 1

        return path
    def error_prompt(self, stderror):
        error_prompt = f"""
        The previous code failed with the following error:
        {result['stderr']}
        Fix the code. Return only corrected code."""

    def shutdown(self):
        # if self.model:
        #     self.model.get_chat_history()
        self._model_release()
        return False

def main():
    text = "Create a simple mad libs game where users are prompted for different cases. Dont ask user prompts now, have predefined answers. Generate a large story. Code python"
    max_iter = 5
    codeman = CodeMan()
    codeman.user_prompt_init(text)
    history = []

    with DockerRuntime() as runtime:
        for i in range(max_iter):
            try:
                print(f"Iteration {i+1}/{max_iter}")

                file_path = codeman.generate_code()
                runtime.copy_file_to_container(host_path=file_path)
                result = runtime.run_code(filename=file_path, language="python")

                history.append({"Iteration":i, "result":result})

                # print(f"Exit code : {result['exit_code']}")
                # print(f"Stdout    : {result['stdout']}")
                # print(f"Stderr    : {result['stderr']}")

                if result["success"]:
                        print(f"\nSucceeded on iteration {i+1}")
                        return {"success": True, "iterations": i, "output": result["stdout"], "history": history}
                else:
                    print(f"\nFailed current iteration.\n")
                    print(f"\nError: {result['stderr']}")
                    continue
            finally:
                codeman.shutdown()

if __name__ == "__main__":
    main()