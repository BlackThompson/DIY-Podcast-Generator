from pydub import AudioSegment
from moviepy.config import change_settings
from moviepy.editor import (
    VideoClip,
    TextClip,
    concatenate_videoclips,
    CompositeVideoClip,
    AudioFileClip,
    ColorClip,
)
from pydub import AudioSegment
import os
import logging

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick\magick.exe"})


def _get_mp3_files(temp_dir):
    mp3_files = [f for f in os.listdir(temp_dir) if f.endswith(".mp3")]
    sorted_mp3_files = sorted(
        mp3_files, key=lambda x: int(x.split("_")[1].split(".")[0])
    )
    mp3_files_path = [os.path.join(temp_dir, f) for f in sorted_mp3_files]

    return mp3_files_path


def concatenate_mp3s_to_wav(temp_dir=r"./temp_audio", output_dir=r"./final_generate"):
    # get all mp3 files in the temp directory
    sorted_mp3_files = _get_mp3_files(temp_dir)
    # create a new AudioSegment object
    combined = AudioSegment.empty()
    for mp3_file in sorted_mp3_files:
        audio = AudioSegment.from_mp3(mp3_file)
        combined += audio

    output_wav = os.path.join(output_dir, "podcast_audio.wav")

    combined.export(output_wav, format="wav")
    print(f"Audio exported as: {output_wav}")
    logging.info(f"Audio exported as: {output_wav}")
    return output_wav


def generate_video(
    subtitles, wav_file, temp_dir=r"./temp_audio", output_dir=r"./final_generate"
):
    # calculate timestamps for each subtitle
    timestamps = []
    start_time = 0
    mp3_files = _get_mp3_files(temp_dir)
    for mp3_file in mp3_files:
        audio = AudioSegment.from_mp3(mp3_file)
        duration = len(audio) / 1000  # in seconds
        timestamps.append((start_time, start_time + duration))
        start_time += duration

    # create video clips for each subtitle
    clips = []
    for i, (start, end) in enumerate(timestamps):
        subtitle = subtitles[i]
        # create a black background clip
        black_background = ColorClip(
            size=(1280, 720), color=(0, 0, 0), duration=end - start
        )

        # create a text clip with the subtitle,leave some margin
        text_clip = TextClip(
            subtitle,
            fontsize=40,
            color="white",
            size=(1000, 720),
            method="caption",
            font="Arial-Bold",
        )

        # set the position of the text clip to the center
        text_clip = text_clip.set_position(("center", "center")).set_duration(
            end - start
        )

        # create a composite video clip with the black background and text clip
        video_clip = (
            CompositeVideoClip([black_background, text_clip])
            .set_start(start)
            .set_end(end)
        )

        # add the video clip to the list of clips
        clips.append(video_clip)

    # concatenate the video clips
    intermediate_videos = []
    step = 5
    for i in range(0, len(clips), step):
        sub_clips = clips[i : i + step]
        intermediate = concatenate_videoclips(sub_clips, method="compose")
        intermediate_videos.append(intermediate)

    video = concatenate_videoclips(intermediate_videos, method="compose")
    # video = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(wav_file)
    video = video.set_audio(audio)  # add audio to the video

    # export the video
    output_video = os.path.join(output_dir, "podcast_video.mp4")
    video.write_videofile(output_video, fps=24, codec="libx264", audio_codec="aac")
    print(f"Video exported as: {output_video}")
    logging.info(f"Video exported as: {output_video}")
    return output_video


if __name__ == "__main__":
    subtitles = [
        "This is the first test.",
        "This is the second test.",
        "This is the third test.",
        "This is the fourth test.",
        "This is the fifth test.",
    ]
    generate_video(subtitles, "podcast_audio.wav")
