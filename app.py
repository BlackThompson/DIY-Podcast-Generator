import logging
from gen_conversation import generate_conversation
from gen_audio import gen_all_speech
from gen_video import generate_video, concatenate_mp3s_to_wav
import asyncio
import os
import gradio as gr

# 配置日志
logging.basicConfig(
    filename="DIY_Podcast.log",  # 日志文件路径
    level=logging.INFO,  # 日志等级
    format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
)


def clear_mp3_files(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".mp3"):
            file_path = os.path.join(folder_path, file_name)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    logging.info(f"Deleted all mp3 files in {folder_path}")


def gen_audio_video(pdf_file, text):
    subtitles = generate_conversation(pdf_file, text)
    asyncio.run(gen_all_speech(input_text_list=subtitles))
    audio_path = concatenate_mp3s_to_wav()
    yield audio_path, None

    video_path = generate_video(subtitles=subtitles, wav_file=audio_path)
    yield audio_path, video_path


def enable_submit(pdf_input, text_input):
    if pdf_input is not None or text_input.strip():
        return gr.update(interactive=True)
    return gr.update(interactive=False)


with gr.Blocks(
    theme=gr.themes.Ocean(),
    # fill_height=True,
) as demo:
    gr.Markdown(
        """
    # 💬 DIY Podcast Generator 🎙️

    - You can upload a paper in `PDF format` or enter some text in the `textbox`. **DIY Podcast Generator** will generate a `podcast audio` and a `podcast video` with subtitles based on the content you provide.
    - The audio will be generated faster than video. The video generation may take over 30 minutes :)
    """
    )
    with gr.Row(equal_height=True):
        with gr.Column():
            pdf_input = gr.File(label="Input (PDF Document)")
            text_input = gr.Textbox(label="Input (Text)", lines=10)
            submit = gr.Button("Submit", interactive=False)
        with gr.Column():
            audio_output = gr.Audio(
                label="Podcast Audio",
                interactive=False,
                show_download_button=True,
                type="filepath",
            )
            video_output = gr.Video(
                label="Podcast Video",
                interactive=False,
                show_download_button=True,
            )

    pdf_input.change(enable_submit, inputs=[pdf_input, text_input], outputs=submit)
    text_input.change(enable_submit, inputs=[pdf_input, text_input], outputs=submit)

    submit.click(
        gen_audio_video,
        inputs=[pdf_input, text_input],
        outputs=[audio_output, video_output],
    )


if __name__ == "__main__":
    temp_audio_dir = r"./temp_audio"
    # delete all mp3 files in the temp_audio directory before starting
    clear_mp3_files(temp_audio_dir)

    demo.launch()
    clear_mp3_files(temp_audio_dir)
