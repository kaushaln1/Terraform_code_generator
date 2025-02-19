import streamlit as st
import requests

# URL of our backend endpoint (adjust if needed)
API_URL = "http://localhost:8000/generate_terraform_code"
VALIDATE_URL = "http://localhost:8000/validate_terraform_code"  # New endpoint for validation only

st.title("Terraform Code Generator")
st.write("Enter a scenario to generate Terraform code:")

scenario = st.text_area("Scenario", "Deploy an EC2 instance with a security group")

# Initialize session state to store generated code
if 'terraform_code' not in st.session_state:
    st.session_state.terraform_code = ""
if 'validation_results' not in st.session_state:
    st.session_state.validation_results = {}

if st.button("Generate Code"):
    with st.spinner("Generating Terraform code..."):
        try:
            payload = {"scenario": scenario}
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                st.session_state.terraform_code = data.get("terraform_code", "")
                st.session_state.validation_results = data.get("validation_results", {})

                st.success("Terraform code generated successfully!")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display and allow editing of the generated code
st.subheader("Terraform Code Editor")
edited_code = st.text_area("Edit Terraform Code", value=st.session_state.terraform_code,
                           height=400, key="code_editor")

# Revalidate button
if st.button("Validate Code"):
    with st.spinner("Validating Terraform code..."):
        try:
            payload = {"terraform_code": edited_code}
            response = requests.post(VALIDATE_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                st.session_state.validation_results = data.get("validation_results", {})
                st.success("Validation completed!")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display validation results
if st.session_state.validation_results:
    st.subheader("Validation Results:")
    validation_container = st.container()

    with validation_container:
        for cmd, result in st.session_state.validation_results.items():
            cmd_name = cmd.split()[-1] if len(cmd.split()) > 0 else cmd
            with st.expander(f"Command: {cmd_name}", expanded=True):
                if "Error" in result:
                    st.error(result)
                else:
                    st.success(result)

# Add download button for the code
if edited_code:
    st.download_button(
        label="Download Terraform Code",
        data=edited_code,
        file_name="main.tf",
        mime="text/plain"
    )

# Add sidebar with helpful information
with st.sidebar:
    st.header("How to Use")
    st.markdown("""
    1. Enter your infrastructure scenario
    2. Click 'Generate Code' to create Terraform configuration
    3. Edit the generated code as needed
    4. Click 'Validate Code' to check for syntax errors
    5. Download the final code when ready

    **Tips for Writing Scenarios:**
    - Be specific about resource types
    - Mention connections between resources
    - Specify any custom configurations
    """)