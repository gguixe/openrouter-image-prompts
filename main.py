import os
import requests
import json
import time

SHARED_FOLDER = 'shared'
OPENROUTER_API_KEY = ''
MODEL = 'microsoft/phi-3-medium-128k-instruct:free'
PROMPT = 'A cute random animal in a random artistic style. Repeat this previous prompt but changing the random words'
INTERVAL = 8 * 60 * 60  # Interval in seconds (8 hours)

def fetch_and_store_message():
	try:
		print("Request to " + MODEL)
		print("Prompt: " + PROMPT)
		response = requests.post(
		  url="https://openrouter.ai/api/v1/chat/completions",
		  headers={
			"Authorization": f"Bearer {OPENROUTER_API_KEY}",
		  },
		  data=json.dumps({
			"model": f"{MODEL}", 
			"messages": [
			  { "role": "user", "content": f"{PROMPT}" }
			]
		  })
		)
		
		if response.status_code == 200:
			data = response.json()
			message = data['choices'][0]['message']['content']
			print("Response:")
			print(message)
			
			shared_folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "{SHARED_FOLDER}")
			file_path = os.path.join(shared_folder_path, "prompt.txt")
			
			with open("prompt.txt", "w") as file:
				file.write(message)
		else:
			print(f"Error: response.status_code")
	except requests.exceptions.RequestException as e:
		print(f"Request error: {e}")

# Main loop to run the request every 8 hours
while True:
    fetch_and_store_message()
    print("Next prompt in " + f"{INTERVAL}" + " seconds")
    time.sleep(INTERVAL)