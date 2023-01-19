import os

import uuid
from pathlib import Path


def Config():
    # Azure Config
#    AZURE_SPEECH_KEY = os.environ.get("AZ-SPEECH-KEY")
#    AZURE_TRANSLATE_KEY = os.environ.get("AZ-TRANS-KEY")
#    AZURE_SSML_CONF = Path("ssml.xml")
    PIXABAY_KEY = os.environ.get("PIXABAY_KEY")

    # Google Config
#    GOOGLE_TRANSLATE_KEY = os.environ.get("GOOGLE-TRANS-KEY")

#    TRANSLATE_API_KEY = (GOOGLE_TRANSLATE_KEY if AZURE_TRANSLATE_KEY is None else AZURE_TRANSLATE_KEY)

#    VOICE_SUBSCRIPTION_REGION = (
#        os.environ.get("AZ-SUB-REGION") if os.environ.get("AZ-SUB-REGION") is not None else "australiaeast"
#    )

#    TRANSLATE_SUBSCRIPTION_REGION = (
#        os.environ.get("AZ-TRANS-REGION") if os.environ.get("AZ-TRANS-REGION") is not None else "australiaeast"
#    )

#    AZURE_IMAGE_API_URL = "https://api.bing.microsoft.com/v7.0/images/search"
#    AZURE_TRANSLATE_API_URL = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}"

#    GOOGLE_IMAGE_API_URL = ""
#    GOOGLE_TRANSLATE_API_URL = "https://translation.googleapis.com/language/translate/v2?format=text&source={}&target={}&key="+GOOGLE_TRANSLATE_KEY

#    TRANSLATE_API_URL = (GOOGLE_TRANSLATE_API_URL if AZURE_TRANSLATE_KEY is None else AZURE_TRANSLATE_API_URL)

#    ACCEPTED_IMG_FORMATS = ['jpeg', 'jpg', 'png', 'gif']

#    AZURE_HEADERS = {
#        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATE_KEY,
#        'Content-type': 'application/json',
#        'X-ClientTraceId': str(uuid.uuid4()),
#        'Ocp-Apim-Subscription-Region': TRANSLATE_SUBSCRIPTION_REGION
#    }

#    BING_HEADERS = {"Ocp-Apim-Subscription-Key": f"{BING_SEARCH_KEY}"}
#    BING_PARAMS = {
#        "mkt": "de-DE",
#        "imageType": "Photo",
#        "count": "3"
#    }
