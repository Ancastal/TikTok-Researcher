# TikTok Video Information Saver

This Python program is designed to leverage the capabilities of the TikTok API to fetch and save detailed information about videos on TikTok based on hashtags, author details, likes, comments, and more. It provides an efficient way to gather insights from video content and metadata on TikTok, making it easier for researchers, marketers, and content creators to analyze trends, engagement, and content strategies on the platform.

The program was developed in accordance with the requirements requested by a dear friend, for whom this application was developed. Currently, search is only available by hashtag, as that is what was necessary for him to have.

## Features

- **Hashtag Search**: Utilize hashtags to discover and fetch relevant video content, making it easier to analyze specific trends or topics.
- **Video Information**: Comprehensive extraction of video details, including video ID, URL, author username, likes, comments, and hashtags, provides a rich dataset for analysis.
Custom Selections: Offers flexibility by allowing users to select specific pieces of information they want to save, tailoring the data collection to specific research needs.
- **File Saving**: Enables the organized saving of extracted information into text files, facilitating easy access and further analysis.
- **User-Friendly Interface**: Incorporates prompt_toolkit to offer an engaging and intuitive user interface, ensuring a seamless user experience for data collection tasks.
- **Transcription**: Features transcription capabilities utilizing OpenAI's Whisper, allowing for the conversion of video audio into text, broadening the scope of content analysis. Before using the transcription service, please, check its pricing from the [OpenAI Whisper](https://openai.com/research/whisper) website.

## Future Updates

- Improved search capabilities (by keywords, author, hashtags, trends)
- Machine translation from and into any high-resource language.

## Requirements

- Python 3.6+
- [TikTokApi](https://github.com/davidteather/TikTok-Api)
- [pyktok](https://github.com/dfreelon/pyktok)
- [openai](https://github.com/openai)
- [python-prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)
- asyncio

## Installation

Before you begin, ensure you have Python 3.6 or newer installed on your system.

1. Clone this repository or download the source code.
2. Run `setup.py`

```bash
python setup.py
```

3. Follow the instructions to install the requirements and add the necessary API tokens.
4. After the setup, run the main application normally.

## Usage

To run the program:

```bash
python app.py
```

Follow the interactive prompts to enter hashtags, select the number of videos to process, and choose the information you wish to save.

## API Token

The `ms-token` is necessary to retrieve data from the TikTok services. You can retrieve your `ms-token` by going opening a TikTok video in your Chrome browser. From there, open your browser's inspection page and look for `ms-token` by going to the Application tab and then opening TikTok's cookies.

The `openai_api_key` can be obtained from OpenAI's [Official Platform](https://platform.openai.com/api-keys).

## Acknowledgements

This program is built using the [TikTokApi](https://github.com/davidteather/TikTok-Api) by David Teather and [pyktok](https://github.com/dfreelon/pyktok) by Deen Freelon. Their efforts in creating and maintaining these libraries have significantly simplified the process of interacting with TikTok's data, offering a powerful toolset for developers and researchers interested in analyzing TikTok content. We extend our gratitude to the creators and contributors of these projects for their valuable contributions to the open-source community.

## License

This program is distributed under the AGPL-3.0 License. See `LICENSE` for more information.

## Contact

For any queries or contributions, please open an issue in this repository.

---
**Note**: This program is intended for educational and research purposes only. Always adhere to TikTok's terms of service and use the APIs responsibly.
