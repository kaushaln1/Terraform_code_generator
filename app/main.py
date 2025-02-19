from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.llm import terraform_generator
from app.sandbox import terraform_sandbox
from app.logger import logger

app = FastAPI()

class TerraformRequest(BaseModel):
    scenario: str

class TerraformResponse(BaseModel):
    terraform_code: str
    # validation_results: dict

class ValidationRequest(BaseModel):
    terraform_code: str

@app.post("/generate_terraform_code", response_model=TerraformResponse)
async def generate_terraform_code(request: TerraformRequest):
    try:
        logger.info(f"Received request for scenario: {request.scenario}")
        terraform_code = terraform_generator.generate_code(request.scenario)
        # validation_results = terraform_sandbox.execute_terraform(terraform_code)
        logger.info("Terraform code generated and validated successfully.")
        return TerraformResponse(terraform_code=terraform_code)
    except Exception as e:
        logger.error("Error in /generate_terraform_code endpoint", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/validate_terraform_code")
def validate_terraform_code(request: ValidationRequest):
    try:
        validation_results = terraform_sandbox.execute_terraform(request.terraform_code)
        return {"validation_results": validation_results}
    except Exception as e:
        logger.error("Error in /validate_terraform_code endpoint", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))