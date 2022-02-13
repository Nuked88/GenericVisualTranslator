from random import random
from easynmt import EasyNMT, models
from grabscreen import grab_screen
from pathlib import Path
from easyocr import Reader
from sklearn.feature_extraction.text import TfidfVectorizer
import yaml
import cv2
import deepl
import pyttsx3
import numpy as np
import keyboard
import Overlay as ov
import time
# Set main path
main_path = Path(__file__).parent

# Load Config
config_path = f"{main_path}\\config.yaml"
with open(config_path) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    game_name = config['game_name']
    rc = config['main_region']
    ac = config['activator_region']



# Load Models
print("Loading models...")

# Load our model only if is internal
if config['translation_method'] == 'opus':
    if config['translation_internal_method'] == 'online':
        model = EasyNMT('opus-mt')
    elif config['translation_internal_method'] == 'offline':
        # Load Translator Offline download the model from https://huggingface.co/Helsinki-NLP and put everything in the models\opus-mt folder
        model = EasyNMT(translator=models.AutoModel(f"{main_path}\\models\\opus-mt\\"))

# Load OCR
reader = Reader(['en'], gpu=config["gpu_enabled"])

if config['tts_enabled']:
    # Load TTS
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[config["tts_voice_number"]].id)
print("Models loaded!")

# Init variables
fulltext_temp = ""
image_temp = np.array([])
image_crop_temp = np.array([])

def find_image( image_full, image_to_find):
    # Using template matching to find the image
    image_to_find = cv2.imread(image_to_find)
    res = cv2.matchTemplate(image_full, image_to_find, cv2.TM_CCOEFF_NORMED)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(res)

    (startX, startY) = maxLoc
    endX = startX + image_to_find.shape[1]
    endY = startY + image_to_find.shape[0]
    if maxVal > 0.9:
        return [True,startX, startY, endX, endY]
    else:
        return [False,0,0,0,0]

def translate(text,source_language, target_language, method='internal'):
    if method == 'opus':
        translated_text = model.translate(fulltext, target_lang=target_language)
    elif method == 'deepl':
        translated_text = deepl.translate(source_language=source_language, target_language=target_language, text=text)
    else:
        raise ValueError("Method not supported")

    return translated_text

def check_string_similarity(arr_string):                                                                                                                                                                            
    vect = TfidfVectorizer(min_df=1, stop_words="english")                                                                                                                                                                                                   
    tfidf = vect.fit_transform(arr_string)                                                                                                                                                                                                                       
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity.toarray()[0][1]

def read_text(image):
    fulltext = ""
    ocr_res = reader.readtext(image,batch_size=512)
    # join all the text
    for oc in ocr_res:
        fulltext = fulltext +" "+ oc[1]
    return fulltext

def clear_string(string):
    string = string.replace("(optional, probably does not need a translation)","")
    string = string.replace("_"," ")
    return string.strip().capitalize()



if config['show_text']:
    t = ov.Main(rc)
    t.start()
    time.sleep(1)
    t.hide()

########################################################################################
#                                MAIN FUNCTION                                        #
########################################################################################

while True:
    try:
        image_full = grab_screen(region=(ac["X"], ac["Y"], ac["extensionOfX"], ac["extensionOfY"]))
        image = grab_screen(region=(rc["X"], rc["Y"], rc["extensionOfX"], rc["extensionOfY"]))
        cv2.imwrite(f"{main_path}\\captured.png", image_full)
        image_full = cv2.imread(f"{main_path}\\captured.png")
    
        #compare if current image is the same of the last image
        if  np.array_equal(image_temp,image):
            continue
        else:
            image_temp = image

            # Detect if activator is in screen
            res = find_image( image_full, f"{main_path}\\activators\\" + ac['name'])

            if  res[0]:

                # Read text from screen
                fulltext = read_text(image)

                
                # Check if the text is the same of the last text
                similarity_score = check_string_similarity([fulltext,fulltext_temp])
                
                # Check if the text is similar to the last text
                if  similarity_score < 0.7 and  "~[-" not in fulltext:
                    fulltext_temp = fulltext
                    translated_text = translate(fulltext, config['source_language'], config['target_language'], method=config['translation_method'])
                    
                    # Clear from weirdness
                    translated_text = clear_string(translated_text)

                    print(f"#####################################\n{translated_text}\n#####################################")
                    
                    if config['show_text']:
                        t.setTextx(translated_text)
                        t.show()
                        
                    if config['tts_enabled']:
                        engine.say(translated_text)
                        engine.runAndWait()
                    else:
                        #calculate sleep time for words in translated text
                        time_to_sleep = len(translated_text.split(" ")) * config['time_to_wait_for_word']
                        time.sleep(time_to_sleep)

                    if config['show_text']:
                        t.hide()
                    
                    if config['skip_key'] != "None":
                        # Randomly skip a few milliseconds
                        time.sleep(random.uniform(0.02, 0.15))
                        # Press the skip key
                        keyboard.press_and_release(config['skip_key'])

                                      

        time.sleep(config['time_between_captures'])
    except:
        pass

        

     

