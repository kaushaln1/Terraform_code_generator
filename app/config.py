import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "db/chroma")
    SANDBOX_DIR = os.getenv("SANDBOX_DIR", "/tmp/terraform_sandbox")
    DOCKER_IMAGE = os.getenv("DOCKER_IMAGE", "hashicorp/terraform:latest")
