import os

from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


class TerraformCodeGenerator:
    def generate_code(self, scenario):
        try:
            response = client.chat.completions.create(
                model="gpt-4",  # Ensure correct model usage
                messages=[
                    {"role": "system", "content": "You are a Terraform expert. only give the terraform code and nothing else"},
                    {"role": "user", "content": scenario}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating Terraform code: {e}")
            raise e


terraform_generator = TerraformCodeGenerator()
