import asyncio
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv
import os
from openai import OpenAI
import logging

# load .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# Async function to generate MP3 audio file from text
async def _generate_single_speech(voice, input_text, output_file, speed=1.0):
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=input_text,
        speed=speed,
    )
    response.stream_to_file(output_file)


async def gen_all_speech(
    input_text_list, voice1="nova", voice2="echo", save_dir=r"./temp_audio"
):
    tasks = []
    for index, text in enumerate(input_text_list):
        save_path = os.path.join(save_dir, f"output_{index}.mp3")
        if index % 2 == 0:
            tasks.append(_generate_single_speech(voice1, text, save_path))
        else:
            tasks.append(_generate_single_speech(voice2, text, save_path))
    await asyncio.gather(*tasks)
    logging.info(f"Generated all speech successfully!")


if __name__ == "__main__":
    input_text_list = [
        "This is the first test.",
        "This is the second test.",
    ]

    asyncio.run(gen_all_speech(input_text_list))
