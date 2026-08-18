import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI


app = FastAPI()


client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)


class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "status": "ok",
        "app": "Isalni API"
    }


@app.post("/ask")
def ask(data: Question):

    question = data.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="السؤال فارغ"
        )


    try:

        response = client.responses.create(
            model="gpt-5.6",
            input=question
        )


        return {
            "answer": response.output_text
        }


    except Exception:

        raise HTTPException(
            status_code=500,
            detail="حدث خطأ أثناء معالجة السؤال"
        )
