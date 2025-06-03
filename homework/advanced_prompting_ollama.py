import subprocess
import time
import requests

model_name = "gemma3"
# Pull the desired model. WARNING: this implementation does not check your disk space, so be careful when running this
print("Pulling %s model from Ollama..." % model_name)
subprocess.run(["ollama", "pull", model_name], check=True)

# I wait here for a bit just in case
time.sleep(2)

initial_prompt = "Nuo šiol atsakyk tik lietuvių kalba."

# prompting
print("Running %s model..." % model_name)
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": model_name,
        "prompt": initial_prompt,
        "stream": False
    }
)

if response.ok:
    print("Atsakymas:")
    print(response.json()["response"])
else:
    print("Klaida:", response.status_code)
