import docker
import tarfile
import io
import os
import subprocess

class DockerRuntime:
    def __init__(self, image_name: str = "agent-runtime"):
        self.client = docker.from_env()
        self.image_name = image_name
        self.container = None

    def start(self):
        """Start a persistent container."""
        self.container = self.client.containers.run(
            self.image_name,
            detach=True,
            tty=True,
            mem_limit="512m",
            nano_cpus=1_000_000_000,
            network_mode="none",
            remove=True,
        )

    def stop(self):
        if self.container:
            self.container.stop(timeout=2)
            self.container = None

    def copy_file_to_container(self, host_path: str, container_dest: str = "/Snippets"):
        subprocess.run(
            ["docker", "cp", host_path, f"{self.container.id}:{container_dest}"],
            check=True
        )

    def run_code(self, filename: str, language: str, timeout: int = 30) -> dict:
        """Execute a file and return stdout, stderr, exit_code."""
        print(f"file name is {filename}")
        commands = {
            "python": f"python3 {filename}",
            "rust":   f"cd /Snippets && rustc {filename} -o out && ./out",
            "cpp":    f"cd /Snippets && g++ {filename} -o out && ./out",
        }
        cmd = commands.get(language)
        if not cmd:
            raise ValueError(f"Unsupported language: {language}")

        result = self.container.exec_run(
            cmd=["bash", "-c", cmd],
            workdir="/",
            demux=True,
        )
        stdout, stderr = result.output
        return {
            "exit_code": result.exit_code,
            "stdout": stdout.decode() if stdout else "",
            "stderr": stderr.decode() if stderr else "",
            "success": result.exit_code == 0,
        }

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()