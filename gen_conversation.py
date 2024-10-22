from dotenv import load_dotenv
import os
from openai import OpenAI
import fitz  # PyMuPDF
from prompt import gen_podcast, parsed_podcast
from pydantic import BaseModel
import logging


# load .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def _extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def _generate_origin_conversation(text):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": gen_podcast},
                {"role": "user", "content": text},
            ],
            temperature=1.0,
        )
        result = completion.choices[0].message.content
        logging.info(f"Generated conversation successfully!")
        print("Generated conversation successfully!")
        return result
    except Exception as e:
        logging.error(f"Error generating conversation: {e}")
        raise e


def _parse_conversation(conversation):
    try:

        class ConversationEvent(BaseModel):
            Conversation: list[str]

        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": parsed_podcast,
                },
                {
                    "role": "user",
                    "content": conversation,
                },
            ],
            response_format=ConversationEvent,
        )
        result = completion.choices[0].message.parsed
        logging.info(f"Parsed conversation successfully!")
        print("Parsed conversation successfully!")
        return result.Conversation
    except Exception as e:
        logging.error(f"Error parsing conversation: {e}")
        raise e


def generate_conversation(pdf_path=None, text=None):
    combined_text = ""
    if pdf_path is not None:
        pdf_text = _extract_text_from_pdf(pdf_path)
        combined_text += pdf_text
    if text is not None:
        combined_text += text
    conversation = _generate_origin_conversation(combined_text)
    parsed_conversation = _parse_conversation(conversation)
    return parsed_conversation


if __name__ == "__main__":
    pdf_path = "test.pdf"
    conversation = generate_conversation(pdf_path)
