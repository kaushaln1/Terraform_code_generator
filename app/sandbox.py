import subprocess
import os
import uuid
from app.config import Config
from app.logger import logger


class TerraformSandbox:
    def __init__(self):
        self.sandbox_dir = Config.SANDBOX_DIR
        if not os.path.exists(self.sandbox_dir):
            os.makedirs(self.sandbox_dir, exist_ok=True)
            logger.info(f"Created sandbox directory at {self.sandbox_dir}")

    def execute_terraform(self, terraform_code: str):
        session_id = str(uuid.uuid4())
        session_path = os.path.join(self.sandbox_dir, session_id)
        os.makedirs(session_path, exist_ok=True)
        tf_file_path = os.path.join(session_path, "main.tf")

        try:
            with open(tf_file_path, "w") as f:
                f.write(terraform_code)
            logger.info(f"Terraform code written to {tf_file_path}")

            # Convert Windows path to Docker-compatible format
            # 1. Get absolute path
            abs_session_path = os.path.abspath(session_path)
            # 2. Convert backslashes to forward slashes
            docker_path = abs_session_path.replace('\\', '/')
            # 3. For Windows, convert C:/ format to /c/ format
            if os.name == 'nt' and ':' in docker_path:
                drive, path = docker_path.split(':', 1)
                docker_path = f"/{drive.lower()}{path}"

            commands = [
                f"docker run --rm -v \"{docker_path}:/terraform\" -w /terraform {Config.DOCKER_IMAGE} init",
                f"docker run --rm -v \"{docker_path}:/terraform\" -w /terraform {Config.DOCKER_IMAGE} validate"
            ]

            results = {}
            for cmd in commands:
                logger.info(f"Executing command: {cmd}")
                process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                output = process.stdout + process.stderr
                results[cmd] = output
                if process.returncode != 0:
                    logger.error(f"Command failed: {cmd}\nOutput: {output}")
            return results
        except Exception as e:
            logger.error("Error executing Terraform in sandbox", exc_info=True)
            raise e


terraform_sandbox = TerraformSandbox()
