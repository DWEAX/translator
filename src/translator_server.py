from os import environ
from google.cloud import translate
import datetime
import logging 
from fastapi_offline import FastAPIOffline
from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 
import configparser 
from typing import Literal
import json 

config = configparser.ConfigParser()
config_file = 'conf/translator.conf'
config.read(config_file)

TITLE = config['TRANSLATOR_SERVER']['TITLE']
DESCRIPTION = config['TRANSLATOR_SERVER']['DESCRIPTION']
VERSION = config['TRANSLATOR_SERVER']['VERSION']
HOST = config['TRANSLATOR_SERVER']['HOST']
PORT = config['TRANSLATOR_SERVER'].getint('PORT')
LOG_LEVEL = config['TRANSLATOR_SERVER']['LOG_LEVEL']
PROJECT_ID = config['TRANSLATOR_SERVER']['PROJECT_ID']
assert PROJECT_ID
PARENT = f"projects/{PROJECT_ID}"

formatter = logging.Formatter(fmt='%(levelname)s: %(name)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('TRANSLATOR_SERVER')
if LOG_LEVEL == 'debug':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
file_handler = logging.FileHandler('logs/translator_server.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def print_supported_languages(display_language_code: str):
    client = translate.TranslationServiceClient()

    response = client.get_supported_languages(
        parent=PARENT,
        display_language_code=display_language_code,
    )

    languages = response.languages
    print(f" Languages: {len(languages)} ".center(60, "-"))
    for language in languages:
        language_code = language.language_code
        display_name = language.display_name
        print(f"{language_code:10}{display_name}")

def translate_text(text: str, target_language_code: str) -> translate.Translation:
    client = translate.TranslationServiceClient()

    response = client.translate_text(
        parent=PARENT,
        contents=[text],
        target_language_code=target_language_code,
    )

    return response.translations[0]

def detect_language(text: str) -> translate.DetectedLanguage:
    client = translate.TranslationServiceClient()

    response = client.detect_language(parent=PARENT, content=text)

    return response.languages[0]


tags_metadata = [
    {
        "name":"translate",
        "description":"입력된 문장을 Google Translator Server에 전달하고 결과를 반환함"
    },
    {
        "name":"detect_language",
        "description":"입력된 문장의 언어를 반환합니다."
    },
]

app = FastAPIOffline(
    title=TITLE,
    description=DESCRIPTION,
    openapi_tags=tags_metadata,
    version=VERSION, 
)

@app.post("/translate", tags=['translate'])
async def translate(sentence: str='request sententence', target_language: str='en'):
    logger.info('user request sentence: '+sentence)

    response = translate_text(sentence, target_language)

    logger.info(response)

    return response

@app.post("/detect_language", tags=['detect_language'])
async def detecte_language(sentence: str='request sententence'):
    logger.info('user request sentence: ' + sentence)

    response = detect_language(sentence)

    logger.info(response)

    return response

if __name__ == '__main__':
    try:
        logger.info("Start Translator Server : {} : {} : {}".format(HOST, PORT, LOG_LEVEL))
        uvicorn.run(app, host=HOST, port=PORT, log_level=LOG_LEVEL)
    except:
        logger.error("Can't load Translator Server. Check configuration.")
