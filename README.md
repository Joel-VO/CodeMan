# CodeMan

CodeMan is an agentic AI code generation system that writes, executes, tests, and self-corrects code inside a controlled local runtime environment. It integrates model flexibility in ollama with containerized execution to create an iterative development loop that ensures generated code works.

## Introduction

This was created to tackle a problem faced by me. I use the terminal extensively, and naturally use LLM's fairly often for boilerplate code. However, I usually find the quality lacking with error after error. To tackle this, CodeMan was born.

## Features
* LLM-driven code generation
* Automatic code extraction
* Docker-based runtime isolation
* Iterative self-correction loop
* Test case validation
* Multi-language support
* Optional GPU framework support (PyTorch, TensorFlow)


## Requirements
- Python 3.10+
- Docker Engine (Follow this link to download [Docker](https://docs.docker.com/get-started/get-docker/))
- Ollama (Follow this link to download [Ollama](https://ollama.com/))

## Installation
To start off, clone the repo to a folder and then open the folder. To setup CodeMan, run the following command:
```bash
bash install.sh
```
This will create a venv for running the script in and sets up all necessary dependencies.

---
### Notes

- Designed for local development environments
- Execution is container-isolated
- Resource limits and security controls are recommended
