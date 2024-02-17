import os
import yaml

print("Welcome to TikTok Helper setup!")
print("I will now install the required packages for you.")
print("This may take a few minutes.")

input("Press Enter to continue...")

# Install the required packages
os.system("pip install -r requirements.txt")
os.system("clear") if os.name == "posix" else os.system("cls")

print("All required packages have been installed.")
openai_api_key = input("Please enter your OpenAI API key: ")
ms_token = input("Please enter your TikTok token: ")
secrets = {
    "api": openai_api_key,
    "ms-token": ms_token}

with open('secrets.yaml', 'w') as file:
    yaml.dump(secrets, file)

os.system("clear") if os.name == "posix" else os.system("cls")
print("Setup is complete!\n")
print("You can now run the app by executing the following command:")
print("`python app.py`")
