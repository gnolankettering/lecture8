import openai
import config
import time

client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

file = client.files.create(
  file=open("ExplorersGuide.pdf", "rb"),
  purpose='assistants'
)

zelda_expert_assistant = client.beta.assistants.create(
  name="Zelda expert",
  instructions="""You're an expert on the video game Zelda, and you're going to answer my questions about the game using the file I've given you.""",
  model="gpt-4-turbo-preview",
  tools=[{"type": "file_search"}],
   tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
   }
)
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is Link's traditional outfit color?"
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=zelda_expert_assistant.id
)

run.status

def waiting_assistant_in_progress(thread_id, run_id, max_loops=20):
    for _ in range(max_loops):
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status != "in_progress":
            break
        time.sleep(1)
    return run

run = waiting_assistant_in_progress(thread.id, run.id)
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)



