# :video_game: :headphones: :rocket: Generic Visual Translator :rocket: :headphones: :video_game:
**GVT** is a generic translation tool for parts of text on the PC screen with Text to Speech functionality.
I wanted to create it because the existing tools that I experimented with did not satisfy me in ease-to-use experience and configuration.
Personally I used it with Lost Ark (example included generated by 2k monitor) to translate simple dialogues of quests in Italian.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C0AJECJ)

## :memo:Requirements

Tested Operating Systems : **Windows 10/11**
Python Version: **3.9.6**

- Easynmt
- OpenCV2
- Easyocr
- Numpy
- Deepl (Unofficial API)
- Pyttsx3
- Pywin32
- WXWidgets
- Pygame
- Keyboard

The `requirements.txt` file has been created with the versions currently installed on my pc, but it is not excluded that **GVT** could work also with newer or older versions of the same libraries

**Requirements installation command**
`pip install -r requirements.txt`

## :muscle:How it works

**GVT** simply translates a user-defined region of the screen and then recites it using Windows 10/11 TTS (Not tested on Windows 7) showing the translated text instead of the one on the screen.

Before using it, you need to configure the `config.yaml` file in the same folder.

Then you can run **GVT** using `run.bat` or with the command `python main.py`.


##:eyes:File description `config.yaml`.



| Variable Name                   | Type of variable                                     | Description                                                                                                                                                                                                                                                                         | Recommended |
|---------------------------------|------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| **game_name**                       | `string between "`                                   | Application Name                                                                                                                                                                                                                                                                    |             |
| **source_language**                 | Acronym that corresponds to the Application language (ex. en,de,ch,jp) | Language of the application.                                                                                                                                                                                                                                                         |             |
| **target_language**                 | Acronym that corresponds to the chosen language  (ex. en,de,ch,jp)     | Language in which to translate.                                                                                                                                                                                                                                                      |             |
| **translation_method**              | `deepl` \| `opus`                                    | Translation Engine. Deepl will use unofficial API.                                                                                                                                                                                                                                              | deepl       |
| **translation_internal_method**     | `offline` \| `online`                                | Used only when you select `internal` in the translation_method variable.   offline: is using the model downloaded in the **models\opus-mt** folder. You can download the entire model here : https://huggingface.co/Helsinki-NLP online: it download the model you need automatically.   |             |
| **gpu_enabled**                     | `True` \| `False`                                    | With `True` and a supported GPU the read of the text will be really fast.                                                                                                                                                                                                              | `True`        |
| **time_between_captures**           | `integer`                                       | Time that pass before **GVT** check a new element on the screen.                                                                                                                                                                                                                         | 1           |
| **skip_key**                        | `string between "` \| `"None"`                             | If the text can be sent forward, once read, with a key, **GVT** can send it forward automatically by telling it which key to press. If set to None it will not do anything.                                                                                                             |             |
| **show_text**                       | `True` \| `False`                                    | If set to `True`, an overlay will be shown on the application text, containing the translated text.                                                                                                                                                                                   |             |
| **time_to_wait_for_word**           | `float`                                         | If tss_enabled is set to `False` and show_text is set to `True` **GVT** will use this parameter to figure out how long to show the overlay text.  If tss_enabled is set to True this parameter will be ignored and the overlay will last as long as it takes to play the audio of the text. | 0.3         |
| **tts_enabled**                     | `True` \| `False`                                    | If enabled, **GVT** will use windows text to Speech the translated phrase.                                                                                                                                                                                                               |             |
| **tts_voice_number**                | `integer`                                    | Use voice_list.py to list all the voices on your system and to see which number corresponds to the one you want to choose.                                                                                                                                                           |             |
| **main_region**                     |                                                      | It contains the coordinates of the region of the screen where the text to be translated will appear. Use GetCoords.py to make your job easier.                                                                                                                                       |             |
| **main_region > X**                 | `integer`                                              | Starting point of the region on the X axis.                                                                                                                                                                                                                                          |             |
| **main_region > Y**                 | `integer`                                              | Starting point of the region on the Y axis.                                                                                                                                                                                                                                          |             |
| **main_region > extensionOfX**      | `integer`                                              | Number of pixels required to reach the end point of the frame on the X axis.                                                                                                                                                                                                         |             |
| **main_region > extensionOfY**      | `integer`                                              | Number of pixels required to reach the end point of the frame on the Y axis.                                                                                                                                                                                                         |             |
| **activator_region**                |                                                      | It contains the coordinates where **GVT** will look for the text activation image to be translated.  Once found, **GVT** will proceed with the translation.  Once it disappears it will return to idle state.                                                                                |             |
| **activator_region > name**         | `string` \| `"None" `                                      | Name of the image that you will cut from a screenshot of your screen and that identifies the appearance of a text to be translated in the application.It need to be placed in the **activators** folder                                                                                                                               |             |
| **activator_region > X**            | `integer`                                              | Starting point of the region on the X axis.                                                                                                                                                                                                                                          |             |
| **activator_region > Y**            | `integer`                                              | Starting point of the region on the Y axis.                                                                                                                                                                                                                                          |             |
| **activator_region > extensionOfX** | `integer`                                              | Number of pixels required to reach the end point of the frame on the X axis.                                                                                                                                                                                                         |             |
| **activator_region > extensionOfY** | `integer`                                              | Number of pixels required to reach the end point of the frame on the Y axis.                                                                                                                                                                                                         |             |



## :rocket:Getting started

This is an example based on the LostArk video game
- Clone this repository on your pc or download the folder and enter in it
- Launch LostArk and reach a dialogue scene
- Run `runCoordHelper.bat` or the command `python GetCoords.py`
- Press <kbd>Z</kbd> on the upper left point of the text box
- Press <kbd>Z</kbd> on the lower right point of the text box
- Copy the coordinates from the console instead of the empty fields in the `config.yaml` file under the` main_region` and close the console
- Find the dot or icon that appears whenever the text to be translated also appears, in the case of LostArk it is the `Leave` button at the bottom right
- Press the <kbd> Shift </kbd> + <kbd> Win </kbd> + <kbd> S </kbd> buttons on Windows 10 or 11 and select this image and save it later in the ** activators ** folder with a recognizable name
- Run `runCoordHelper.bat` again or the command` python GetCoords.py
- Use the same method as above to get the coordinates of a not too narrow box surrounding the ** activator ** in-game image
- Copy the coordinates from the console and paste it instead of the empty fields in the `config.yaml` file under the` activator_region` and close the console 
- Set the `source_language` with the acronym of the language you want to translate from, and the `target_language` for the language you want to translate the game into (use https://github.com/ptrstn/deepl-translate for the reference table and languages supported by deepl or go here https://huggingface.co/Helsinki-NLP for opus models)
- Set the dialog progress key if desired, otherwise leave it at `None`. **Note:** Leave to `None` if your game have a heavy anti-cheat system that not allow anything except you to press the keys of your keyboard
- Set `show_text` and `tts_enabled` according to what you want enabled/disabled
- If you have set `tts_enabled` to `True`, `run runVoiceList.bat` or  `python voice_list.py` to find out the number matched to the voices installed in your Windows distribution (is the one in the square parentheses) and set the variable `tts_voice_number` to the desired number.

#### Here is an example of the complete file :clipboard:
```
game_name:  Lost_Ark
source_language: en
target_language: it
translation_method: deepl
translation_internal_method: offline
gpu_enabled: True
time_between_captures: 1
skip_key: "g"
show_text: False
time_to_wait_for_word: 0.3
tts_enabled: True
tts_voice_number: 0

main_region: 
  X: 567
  Y: 1304
  extensionOfX: 2068
  extensionOfY: 1439
activator_region:
  name: "lost_ark.png"
  X: 2
  Y: 1308
  extensionOfX: 2559
  extensionOfY: 1439

```

- Execute `run.bat`

## :thought_balloon:To Do
- Add the capability to define more regions and activator at once
- Add the capability to support multiple game just chosing it from a menu