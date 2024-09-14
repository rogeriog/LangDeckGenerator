#from LangDeckGen import Config
from LangDeckGen import pixabay as pb
import errno
import json
import logging
import mimetypes
import os
import shutil
import sys
from pathlib import Path
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from slugify import slugify
import time
from googletrans import Translator
from gtts import gTTS
import LangDeckGen
from LangDeckGen.memecaption import meme
from LangDeckGen.audiospeed import audiospeed
from pathlib import Path
import re
from bing_image_downloader import downloader
import validators
from pathlib import Path
language_code={'fr':'french','de':'german','sv':'swedish','fi':'finnish','es':'spanish'}
WAIT_TIME=2


def suppressOutput(func):
    def wrapper(*args, **kwargs):
        with open(os.devnull,"w") as devNull:
            original = sys.stdout
            sys.stdout = devNull
            func(*args, **kwargs)
            sys.stdout = original
    return wrapper

special_characters = ['!','#','$','%', '&','@','[',']',']','_',"'",'"',',']

downloader.download = suppressOutput(downloader.download)


class AnkiCard:

    def __init__(self, word: str, lang: str, *args,**kwargs):
        self.PIXABAY_KEY = os.environ.get("PIXABAY_KEY")
        self.OUTPUT_DIRECTORY = Path("./tmp").absolute()
        self.word = word
        self.lang = lang
        self.cardID=self.__create_id() 
        self.translation_dict = self.__translate_word(word,**kwargs)
        self.audio = self.__voice_translate(self.translation_dict["tl"],**kwargs)
        if kwargs.get("PhrasesOnly"):
            self.sentence = ["","","",""]
        else:
            self.sentence = self.__get_example_sentence()
        try:
            self.image = self.__download_word_image(*args,**kwargs)
        except:
            self.image = Path(LangDeckGen.__file__).parent / 'templates' / 'placeholder.png' 
            self.image = str(self.image)
        if not kwargs.get("PhrasesOnly"):
            self.sentence_audio = self.__generate_sentence_audio(**kwargs)
            self.dictionary_entry = self.__get_dictionary_entry()
    def __str__(self):
        return f"TLWord:{self.word}\n ENword:{self.translation_dict['en']}\n AUDIO_FILE:{self.audio}\n \
                 IMAGE_FILE: {self.image} SENTENCES: {self.sentence} SENTENCES_AUDIO_FILES:{self.sentence_audio}"

    def __create_id(self):
        id=0
        for char in self.word+self.lang:
            id+=ord(char)
        return id

    def __translate_word(self, word,**kwargs):
        translation_dict = {"en": "", "tl": ""}
        translator = Translator()
        translation_dict["tl"]=word
        time.sleep(WAIT_TIME)
        print('word',word)
        translation_dict["en"]=translator.translate(word, src=self.lang, dest='en').text
        if kwargs.get('back',False):    ## override tranlation with what was given
            translation_dict["en"]=kwargs['back']

        

        return translation_dict


    def __generate_sentence_audio(self,**kwargs):
        sentence_audio = list()
        TL_sentences = self.sentence[0::2]
        for sentence in TL_sentences:
            sentence_audio.append(self.__voice_translate(sentence,**kwargs))
        return sentence_audio

    def __voice_translate(self, phrase: str, **kwargs) -> str:
        # Define the path to tmp/sound
        audio_path = str(self.OUTPUT_DIRECTORY)+"/"+"sound"
        phraseprint = re.sub(r"[^a-zA-Z0-9 ]", "", phrase) ## remove special chars
        mp3_name = f"{phraseprint[:30].replace(' ','-')}{self.cardID}.mp3"
        # Join all the path ingredients together
        audio_file = audio_path+"/"+mp3_name

        time.sleep(WAIT_TIME) 
        if phrase == "":
            phrase = "okay"
        if kwargs.get('comment_symbol',False):
            phrase=phrase.split(kwargs['comment_symbol'])[0] ## ignore observations that follow after "- "
        tts = gTTS(phrase, lang=self.lang)

        tts.save(audio_file)
        if kwargs.get("tts_speed"):
            audio_file=audiospeed.ChangeAudioSpeed(audio_file,kwargs.get("tts_speed"))
        return(f"{audio_file}")

    def __download_word_image(self,*args,**kwargs):
        if not kwargs.get("UsePixabay"):
            newImgName=self.translation_dict["tl"][:30].replace(' ','-')+str(self.cardID)
            nimg=args[0] ## number of the image to take 1 to 3 
            img_dir= Path('./tmp/imgs').absolute()        
            

            if nimg.strip().isdigit():
                query_string=self.translation_dict["en"]
                gotFigure=True
                try:
                    downloader.download(query_string, limit=3,  output_dir='tmp', adult_filter_off=False, force_replace=False, timeout=60, verbose=True)  ## by default bing downloader will create a folder for every query inside output_dir
                except:
                    gotFigure=False

                for i in special_characters:
                    query_string = query_string.replace(i,'')
                bing_dir = Path('tmp').joinpath(query_string).absolute()
                try:
                    if not Path.is_dir(img_dir):
                        Path.mkdir(img_dir, parents=True)
                except:
                    print("couldnt create folder")
                try:
                    if not Path.is_dir(bing_dir):
                        Path.mkdir(bing_dir, parents=True)
                except:
                    print("couldnt create folder")

                if not gotFigure: ## case bing didnt bring any pics
                    imgformat='jpg'
                    newImgName=self.translation_dict["tl"][:30].replace(' ','-')+str(self.cardID)+'.'+imgformat
                    fullImgName='/'.join((str(img_dir),newImgName))
                    try:
                        if kwargs.get("PhrasesOnly"):
                            meme.DrawMeme(meme.getRandomBasePicture(),"",self.translation_dict["tl"],
                                      full_imgname)
                            meme.DrawMeme(meme.getRandomBasePicture(),self.translation_dict["tl"],self.sentence[0],
                                      full_imgname)
                    except:
                        print(f"Couldnt draw phrase in figure for {self.translation_dict['tl']}")
                    return full_imgname
                else:
                    listing=os.listdir(bing_dir)
                    imgformat='jpg'
                    try:
                        for each in listing:
                            if f"Image_{nimg}" in each:
                                imgformat=each.split('.')[-1]
                    except:
                        print('Didnt find extension, using jpg.')
                    
                    newImgName=newImgName+'.'+imgformat
                    shutil.copy(str(bing_dir.joinpath(f"Image_{nimg}.{imgformat}")), str(img_dir.joinpath(f"{newImgName}")))
                    shutil.rmtree(bing_dir)
                    fullImgName='/'.join((str(img_dir),newImgName))
                    try:
                        if kwargs.get("PhrasesOnly"):
                            meme.DrawMeme(fullImgName,"",self.translation_dict["tl"],fullImgName)
                        else:
                            meme.DrawMeme(fullImgName,self.translation_dict["tl"],self.sentence[0],
                                      fullImgName)
                    except:
                        print(f"Couldnt draw phrase in figure for {self.translation_dict['tl']}")
                    return fullImgName
            elif validators.url(nimg):  ## casearg is an url
                response = requests.get(nimg.strip())
                #ext=nimg.strip().split(".")[-1] ## get extension
                img = Image.open(BytesIO(response.content))
                try:
                    imgname=newImgName+".jpg"
                    fullImgName='/'.join((str(img_dir),imgname))
                    img.save(fullImgName)
                except:
                    imgname=newImgName+".png"
                    fullImgName='/'.join((str(img_dir),imgname))
                    img.save(fullImgName)
                return fullImgName

            else:  ## case arg is path 
                local_path= Path('.').absolute()        
                fullImgName = '/'.join((str(local_path),str(nimg)))
                return fullImgName
            
        else:
            bay = pb.PixaBay(key=self.PIXABAY_KEY)
            time.sleep(WAIT_TIME) 
            imgs = bay.get_images(search=self.translation_dict["en"])
            img_path = self.OUTPUT_DIRECTORY / "imgs"
            imgname=self.translation_dict["tl"][:30].replace(' ','-')+str(self.cardID)
            full_imgname=""
            if imgs.total != 0: 
                img_def=args[0]
                if img_def.strip().isdigit():
                    img=imgs.get_img(int(img_def.strip())-1) ## if specified arg can take another figure in the hits
                    imgname=img.download(img_path,name=imgname,size='web')
                    full_imgname='/'.join((str(img_path),imgname))
                else:  ## case arg is an url 
                    response = requests.get(img_def.strip())
                    ext=img_def.strip().split(".")[-1] ## get extension
                    img = Image.open(BytesIO(response.content))
                    try:
                        imgname=imgname+".jpg"
                        full_imgname='/'.join((str(img_path),imgname))
                        img.save(full_imgname)
                    except:
                        imgname=imgname+".png"
                        full_imgname='/'.join((str(img_path),imgname))
                        img.save(full_imgname)

                if not self.sentence==["","","","",""]: ## case of personal pronouns and maybe others
                    print(full_imgname,self.sentence[0],self.translation_dict["tl"])
                    meme.DrawMeme(full_imgname,self.translation_dict["tl"],self.sentence[0],
                              full_imgname)
                return full_imgname
            else: ## if no image is found in pixabay for the word
                full_imgname=str(img_path)+"/"+self.translation_dict["tl"]+str(self.cardID)+'.jpg'
                if not self.sentence==["","","","",""]: ## case of personal pronouns and maybe others
                    meme.DrawMeme(meme.getRandomBasePicture(),self.translation_dict["tl"],self.sentence[0],
                              full_imgname)
                return full_imgname

    def __get_example_sentence(self):
        language_ext=language_code[self.lang]
        req = requests.get(f"https://context.reverso.net/translation/{language_ext}-english/{self.translation_dict['tl']}",
                           headers={'User-Agent': 'Mozilla/5.0'})
        time.sleep(WAIT_TIME)
        soup = BeautifulSoup(req.text, 'lxml')
        sentences = [x.text.strip() for x in soup.find_all('span', {'class': 'text'}) if '\n' in x.text]
        if len(sentences) == 0 : # empty
            sentences=["-","-","-","-","-"]
        sentences.extend(["-","-","-","-","-"]) ## to be on safe side to have sentences filled.
        return sentences[:4]

    def __get_dictionary_entry(self):
        language_ext=language_code[self.lang]
        req = requests.get(f"https://dictionary.reverso.net/{language_ext}-english/{self.translation_dict['tl']}",
                   headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(req.text, 'html.parser')
        html_dict_entry=soup.find('div', {'id':"TableHTMLResult"})
        ## to remove some bad formatted icons  ## but it doesnt hide everything anymore now, try to fix later
#        html_dict_entry = re.sub("\<!-- google_ad_section_end --\>.*\<!-- end Block with commentaries --\>", '', str(html_dict_entry),0,re.DOTALL)
#        html_dict_entry="<div>\n"+html_dict_entry+"\n</div>"
#        html_dict_entry= re.sub("</div>\s*$","",str(html_dict_entry),0,re.DOTALL)
        return str(html_dict_entry)



