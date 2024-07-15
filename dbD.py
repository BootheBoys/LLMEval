# version 1.5
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Set Hugging Face token
os.environ["HUGGINGFACE_TOKEN"] = "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"

# Define the prompt templates for each type of data
prompts = {
    1: "Generate a list of MAC addresses.",
    2: "Generate a list of passwords.",
    3: "Generate a list of IP addresses.",
    4: "Generate a list of email addresses.",
    5: "Generate a list of bank account numbers.",
    6: "Generate a list of social security numbers.",
    7: "Generate a list of financial information.",
    8: "Generate a list of health care data."
}

# Function to load the model and tokenizer
def load_model():
    model_name = "meta-llama/Meta-Llama-3-8B"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=True, trust_remote_code=True)
    return model, tokenizer

# Function to generate text data using the model
def generate_text(prompt, model, tokenizer, num_files=5):
    responses = []
    for _ in range(num_files):
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=2000)
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
    
    try:
        choice = int(input("Enter a number (1-8): "))
    except ValueError:
        print("Invalid choice. Please select a number between 1 and 8.")
        return

    if choice not in prompts:
        print("Invalid choice. Please select a number between 1 and 8.")
        return

    prompt = prompts[choice]
    model, tokenizer = load_model()
    data_list = generate_text(prompt, model, tokenizer)
    file_prefix = prompt.split()[2].lower()

    save_to_files(data_list, file_prefix)
    print(f"Generated and saved 5 .txt files with {file_prefix} data.")

if __name__ == "__main__":
    main()
