 
import openai 
from openai import OpenAI
import os
import json
endpoint = "https://cdong1--azure-proxy-web-app.modal.run"
api_key = "supersecretkey"
deployment_name = "gpt-4o"
client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

f = open("data/raw.txt", "r")
data = f.read()
print(data)
response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "developer",
            "content": "your task it to create a pretty json from text data i give you"
        },
        {
            "role": "user",
            "content": "work with this raw/dirty data and then give me a json file similar to a table structure" + data
        }
    ]
)

file_path = "data/clean_data.json"

try:
    with open(file_path, "w") as json_file:
        json.dump(response.choices[0].message.content, json_file)
    print(f"Data successfully saved to {file_path}")
except Exception as e:
    print(f"An error occurred while saving the JSON file: {e}")
# print(response.choices[0].message.content)