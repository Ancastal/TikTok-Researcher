import asyncio
import os
import re
import yaml
import pyktok as pyk
import pandas as pd
from TikTokApi import TikTokApi
from openai import OpenAI
from glob import glob

from prompt_toolkit.shortcuts import (
    checkboxlist_dialog, input_dialog,
    message_dialog, yes_no_dialog
    )

pyk.specify_browser('chrome')

async def search_hashtag(tag, number):
    """
    Search for videos associated with a specific hashtag.

    Args:
        tag (str): The hashtag to search for.
        number (int): The number of videos to retrieve.

    Returns:
        list: A list of video IDs associated with the hashtag.
    """
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1,
                                  sleep_after=3, headless=False)
        hashtag_obj = api.hashtag(name=tag)
        os.system("clear") if os.name == "posix" else os.system("cls")
        print("Please, wait a moment...")
        print("We are processing the hashtag: ", tag)

        videos = hashtag_obj.videos(count=number)

        video_ids = [video.id async for video in videos]
        return video_ids

async def save_video_info(video_id, selections):
    """
    Saves the information of a TikTok video to a text file.

    Args:
        video_id (str): The ID of the TikTok video.
        selections (list): A list of strings representing the information to be saved.

    Returns:
        dict: A dictionary containing the selected information.

    Raises:
        None
    """
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1,
                                  sleep_after=3, headless=False)

        video = api.video(id=video_id)
        stats = await api.video(url=f"https://www.tiktok.com/@user/video/{video_id}").info()

        os.system("clear") if os.name == "posix" else os.system("cls")
        print("We are processing the video with ID: ", video_id)
        print("Please, wait a moment...")

        info_dict = {}

        async def get_comments():
            return [comment.text async for comment in video.comments()]

        async def get_hashtags():
            return [hashtag.name async for hashtag in video.hashtags()]

        selection_functions = {
            "comments": get_comments,
            "likes": lambda: stats['stats']['diggCount'],
            "author": lambda: stats['author']['nickname'],
            "hashtags": get_hashtags,
            "description": lambda: stats['desc'],
            "video_id": lambda: video_id,
            "video_url": lambda: f"https://www.tiktok.com/@{stats['author']['nickname']}/video/{video_id}"
        }

        for selection in selections:
            if selection in selection_functions:
                if asyncio.iscoroutinefunction(selection_functions[selection]):
                    info_dict[selection] = await selection_functions[selection]()
                else:
                    info_dict[selection] = selection_functions[selection]()

        with open(f"{video_id}.txt", "w") as file:
            for key, value in info_dict.items():
                file.write(f"{key}: {value}\n")

        return info_dict


def collect_video_ids(hashtag, number):
    return asyncio.run(search_hashtag(hashtag, number))

def input_top_k_dialog():
    return input_dialog(
        title="How many videos do you want to process?",
        text="Input number of videos:",
        default="30"
    ).run()

def select_info_dialog():
    return checkboxlist_dialog(
        title="Select information to save",
        text="Which information do you want to save?",
        values=[
            ("video_id", "Video ID"),
            ("video_url", "Video URL"),
            ("author", "Author"),
            ("description", "Description"),
            ("likes", "Likes"),
            ("comments", "Comments"),
        ],
    ).run()

def save_info_dialog(selections):
    if selections:
        selected_info = ", ".join(selections)
        message_dialog(
            title="Information to save",
            text=f"You have selected:\n{selected_info}"
        ).run()
    else:
        message_dialog(
            title="No selection",
            text="You did not select any information to save."
        ).run()

def download_videos(video_ids, selections, continue_or_exit):
    """
    Downloads videos from TikTok based on the provided video IDs.

    Args:
        video_ids (list): List of video IDs to download.
        selections (bool): Flag indicating whether to save video info.
        continue_or_exit (bool): Flag indicating whether to continue downloading more videos.

    Returns:
        None
    """
    for video_id in video_ids:
        if selections:
            asyncio.run(
                save_video_info(video_id, selections)
                )

        if continue_or_exit is True:
            pyk.save_tiktok(
                f'https://www.tiktok.com/@tiktok/video/{video_id}?is_copy_url=1&is_from_webapp=v1',
                True)
            os.system("clear") if os.name == "posix" else os.system("cls")

            message_dialog(
                title="Download complete",
                text="The video has been downloaded."
            ).run()

            continue_or_exit = yes_no_dialog(
                title="Continue?",
                text="Do you want to download another video?",
            ).run()

            if continue_or_exit is False:
                break

def save_to_excel_dialog():
    return yes_no_dialog(
        title="Save to Excel?",
        text="Do you want to save the information to an Excel file?",
    ).run()

def save_to_excel(hashtag):
    files = glob("*.txt")
    data = []
    for file in files:
        with open(file, "r") as f:
            lines = f.readlines()
            data.append({line.split(":")[0]: line.split(":")[1].strip()
                         for line in lines})

    df = pd.DataFrame(data)
    df.to_excel(f"{hashtag}_info.xlsx", index=False)

if __name__ == "__main__":

    with open('secrets.yaml', 'r') as file:
        secrets = yaml.safe_load(file)
        ms_token = secrets.get('ms-token', None)
        openai_api_key = secrets.get('api', None)

    message_dialog(
        title="TikTok Helper",
        text="Welcome to TikTok Helper!"
    ).run()

    hashtag = input_dialog(
        title="Input hashtag you want to search",
        text="Please enter the hashtag:"
    ).run()

    number = int(input_dialog(
                title='How many videos do you want to search?',
                text='Input number of videos:',
                default="30"
            ).run()
        )

    video_ids = collect_video_ids(hashtag, number)

    message_dialog("Video IDs collected successfully!",
               "I was able to collect {} video IDs for the hashtag #{}"
               .format(len(video_ids), hashtag)
               ).run()

    top_k = input_top_k_dialog()
    video_ids = video_ids[:int(top_k)]

    selections = select_info_dialog()
    save_info_dialog(selections)

    continue_or_exit = yes_no_dialog(
        title="Download videos?",
        text="Do you want to download the videos?",
    ).run()

    download_videos(video_ids, selections, continue_or_exit)

    trascribe = yes_no_dialog(
        title="Transcribe?",
        text="Do you want to transcribe every video in your folder?",
    ).run()

    if trascribe is True:
        client = OpenAI(api_key=openai_api_key)
        videos = glob("*.mp4")
        # ids are numbers, extract them from the file names using regex
        ids = [re.search(r'\d+', video).group() for video in videos]
        for video in videos:
            audio_file = open(video, 'rb')
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )

            with open(f"{ids[0]}.txt", "a") as file:
                file.write("transcript: " + transcript)
            audio_file.close()

            message_dialog(
                title="Transcription complete",
                text="The video has been transcribed and saved to file."
            ).run()

    ask_if_excel = save_to_excel_dialog()
    if ask_if_excel is True:
        save_to_excel(hashtag)
