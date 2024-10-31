from flask import Flask, request, render_template
from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)
from typing import List

app = Flask(__name__)

def assist_journalist(facts: List[str], tone: str, length_words: int, style: str):
    facts = ", ".join(facts)
    msgs=[{"role": "system", "content": "You are an assistant for journalists. \
        Your task is to write articles, based on the FACTS that are given to you. \
        You should respect the instructions: the TONE, the LENGTH, and the STYLE"},
        {"role": "user", "content": f'FACTS: {facts} TONE: {tone} LENGTH: {length_words} words STYLE: {style}'}
    ]
    response = client.chat.completions.create(model="gpt-4o", messages=msgs)
    return (response.choices[0].message.content)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    facts = request.form["facts"]
    tone = request.form["tone"]
    length = int(request.form["length"])
    style = request.form["style"]
    ai_response = assist_journalist(facts.split(","), tone, length, style)
    return render_template("index.html",article=ai_response)

if __name__ == "__main__":
    app.run()

# print(assist_journalist(['The sky is blue', 'The grass is green'], 'informal', 100, 'blogpost'))
