from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

# Read the transcript from the file
with open("transcript.txt", "r") as f:
    transcript = f.read()

# Call the openai ChatCompletion endpoint, with the ChatGPT model
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the following text."},
        {"role": "assistant", "content": "Yes."},
        {"role": "user", "content": transcript}])

print(response.choices[0].message.content)

