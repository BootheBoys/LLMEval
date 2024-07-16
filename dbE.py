import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Set Hugging Face token
os.environ["HUGGINGFACE_TOKEN"] = "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"

# Define the prompt templates for each type of data
prompts = {
    1: [
        "Generate a list of 50 MAC addresses in the format XX:XX:XX:XX:XX:XX.",
        "Create a list of valid MAC addresses for network devices.",
        "Provide 50 sample MAC addresses used in Wi-Fi networks.",
        "List 50 random MAC addresses in standard notation.",
        "Generate unique MAC addresses for virtual machines.",
        "Create a list of 50 MAC addresses for use in a local area network (LAN).",
        "Provide 50 MAC addresses that could be used in a corporate network.",
        "Generate 50 random MAC addresses with mixed upper and lower case letters.",
        "List 50 MAC addresses commonly used in IoT devices.",
        "Create a list of 50 MAC addresses for Ethernet connections."
    ],
    2: [
        "Generate a list of 50 strong passwords.",
        "Create 50 random passwords with a mix of letters, numbers, and symbols.",
        "Provide 50 example passwords for online accounts.",
        "List 50 secure passwords for use in a corporate environment.",
        "Generate 50 passwords that are at least 12 characters long.",
        "Create 50 passwords that follow best security practices.",
        "Provide 50 sample passwords with at least one uppercase letter, one lowercase letter, one number, and one symbol.",
        "Generate 50 unique passwords for personal use.",
        "List 50 passwords that are easy to remember but hard to guess.",
        "Create 50 complex passwords for securing sensitive data."
    ],
    3: [
        "Generate a list of 50 IPv4 addresses.",
        "Create a list of valid IP addresses for network configuration.",
        "Provide 50 sample IP addresses for a home network.",
        "List 50 random IP addresses in the format XXX.XXX.XXX.XXX.",
        "Generate 50 IP addresses for use in a virtual private network (VPN).",
        "Create a list of 50 IP addresses for a corporate network.",
        "Provide 50 public IP addresses used in web servers.",
        "Generate 50 private IP addresses for local network use.",
        "List IP addresses that follow the IPv4 standard.",
        "Create a list of 50 IP addresses for internet-facing devices."
    ],
    4: [
        "Generate a list of 50 email addresses.",
        "Create a list of sample email addresses for testing purposes.",
        "Provide 50 example email addresses for a corporate environment.",
        "List 50 random email addresses with various domains.",
        "Generate 50 email addresses for personal use.",
        "Create a list of 50 email addresses for use in a marketing campaign.",
        "Provide email addresses that include numbers and special characters.",
        "Generate 50 professional email addresses for business use.",
        "List 50 email addresses with different top-level domains (TLDs).",
        "Create a list of 50 email addresses for online accounts."
    ],
    5: [
        "Generate a list of 50 bank account numbers.",
        "Create a list of sample bank account numbers for testing purposes.",
        "Provide 50 example bank account numbers for a financial application.",
        "List 50 random bank account numbers in standard format.",
        "Generate 50 bank account numbers for use in a payment system.",
        "Create a list of 50 bank account numbers for a corporate environment.",
        "Provide 50 bank account numbers that follow banking standards.",
        "Generate 50 unique bank account numbers for personal use.",
        "List 50 bank account numbers for various financial institutions.",
        "Create a list of 50 bank account numbers for secure transactions."
    ],
    6: [
        "Generate a list of 50 social security numbers.",
        "Create a list of valid social security numbers for testing purposes.",
        "Provide 50 example social security numbers for a government application.",
        "List 50 random social security numbers in standard format.",
        "Generate 50 social security numbers for use in a secure database.",
        "Create a list of 50 social security numbers for identity verification.",
        "Provide 50 social security numbers that follow government standards.",
        "Generate 50 unique social security numbers for personal use.",
        "List 50 social security numbers for various demographics.",
        "Create a list of social security numbers for data masking."
    ],
    7: [
        "Generate a list of 50 financial information records.",
        "Create a list of sample financial records for testing purposes.",
        "Provide 50 example financial records for a financial application.",
        "List 50 random financial records including account balances.",
        "Generate financial records for use in an accounting system.",
        "Create a list of 50 financial records for a corporate environment.",
        "Provide 50 financial records that include transaction details.",
        "Generate 50 unique financial records for personal use.",
        "List 50 financial records for various financial institutions.",
        "Create a list of 50 financial records for secure transactions."
    ],
    8: [
        "Generate a list of 50 health care data records.",
        "Create a list of sample health care records for testing purposes.",
        "Provide 50 example health care records for a medical application.",
        "List 50 random health care records including patient information.",
        "Generate 50 health care records for use in a medical database.",
        "Create a list of 50 health care records for a hospital environment.",
        "Provide 50 health care records that include medical history.",
        "Generate 50 unique health care records for personal use.",
        "List 50 health care records for various medical institutions.",
        "Create a list of health care records for secure storage."
    ]
}

# Function to load the model and tokenizer
def load_model():
    model_name = "meta-llama/Meta-Llama-3-8B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=True, trust_remote_code=True)
    return model, tokenizer

# Function to generate text data using the model
def generate_text(prompt, model, tokenizer, num_files=10):
    responses = []
    for _ in range(num_files):
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=200)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        responses.append(response.strip())
    return responses

# Function to save text data to .txt files
def save_to_files(data_list, file_prefix):
    os.makedirs('data_corpus', exist_ok=True)
    for i, data in enumerate(data_list):
        with open(f'data_corpus/{file_prefix}_{i+1}.txt', 'w') as f:
            f.write(data)

# Main function to handle user selection and generate files
def main():
    print("Select a type of vulnerability to generate data corpuses:")
    print("1. MAC Address")
    print("2. Passwords")
    print("3. IP Address")
    print("4. Email Address")
    print("5. Bank Account Numbers")
    print("6. Social Security Numbers")
    print("7. Financial Information")
    print("8. Health Care Data")
    
    choice = int(input("Enter a number (1-8): "))
    
    if choice not in prompts:
        print("Invalid choice. Please select a number between 1 and 8.")
        return

    prompt_list = prompts[choice]
    model, tokenizer = load_model()

    for idx, prompt in enumerate(prompt_list):
        data_list = generate_text(prompt, model, tokenizer)
        file_prefix = f"{prompt.split(' ')[2].lower()}_{idx+1}"
        save_to_files(data_list, file_prefix)
        print(f"Generated and saved 10 .txt files with {file_prefix} data.")

if __name__ == "__main__":
    main()
