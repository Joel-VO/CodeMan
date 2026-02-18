from LLM.coder_LLM import LLMResponse
import os


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
    "h": "h",
    "hpp": "hpp",

    # Java / JVM
    "java": "java",
    "kotlin": "kt",
    "kt": "kt",
    "scala": "scala",
    "groovy": "groovy",

    # JavaScript ecosystem
    "javascript": "js",
    "js": "js",
    "typescript": "ts",
    "ts": "ts",
    "node": "js",

    # Web
    "html": "html",
    "css": "css",
    "scss": "scss",
    "sass": "sass",
    "json": "json",
    "xml": "xml",

    # Systems / modern
    "rust": "rs",
    "go": "go",
    "golang": "go",
    "zig": "zig",
    "nim": "nim",

    # Scripting
    "bash": "sh",
    "sh": "sh",
    "zsh": "sh",
    "powershell": "ps1",
    "ps": "ps1",

    # Backend / scripting
    "php": "php",
    "ruby": "rb",
    "rb": "rb",
    "perl": "pl",

    # Functional
    "haskell": "hs",
    "hs": "hs",
    "clojure": "clj",
    "elixir": "ex",
    "erlang": "erl",

    # SQL
    "sql": "sql",

    # Shell config / infra
    "dockerfile": "dockerfile",
    "yaml": "yaml",
    "yml": "yml",
    "toml": "toml",
    "ini": "ini",

    # Assembly
    "asm": "asm",
    "assembly": "asm",

    # C#
    "csharp": "cs",
    "c#": "cs"
}



class CodeMan:
    def __init__(self):
        self.code_gen_counter = 0
        self.user_prompt = ""
        self.model = None
        self.lang = ""
        self.dir = "Snippets"

    def initialize_model(self, model_name = "qwen2.5-coder:7b"):
        self.model = LLMResponse(model=model_name)

    def model_release(self):
        self.model = None
        
    def user_prompt_init(self, user_prompt_out):
        self.user_prompt = user_prompt_out

    def _rag_orchestration(self):
        # logic for how rag will have certain logic given here and use that for the next sections
        pass
    
    def _docker_orchestration(self):
        # run docker cyclically to give an o/p and then if errors are there, clean o/p and pass back to model.
        pass

    def generate_code(self):
        if self.model == None:
            self.initialize_model()

        out = self.model.response(self.user_prompt)
        language, code = self.model.get_code(out) # make this return both lang and code.
        self.lang = LANG_MAP.get(language.lower(), "txt") if language else "txt"

        os.makedirs(self.dir, exist_ok=True)
        filename = f"script_{self.code_gen_counter}.{self.lang.lstrip('.')}"
        path = os.path.join(self.dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        self.code_gen_counter += 1

def main():
    text = "Give code for finding the fibonacci series using recursion. Code in javascript"
    
    codeman = CodeMan()
    codeman.initialize_model()
    codeman.user_prompt_init(user_prompt_out=text)
    codeman.generate_code()

if __name__ == "__main__":
    main()