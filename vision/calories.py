from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "How many calories in this image?"},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://onesweetharmony.com/wp-content/uploads/2024/03/Panda-Express-Chicken-Teriyaki-2.jpg",
          },
        },
      ],
    }
  ],
  max_tokens=300,
)
print(response.choices[0].message.content)

