import csv
import errno
import logging
import os
import shutil
import sys
from pathlib import Path
from time import sleep

#import genanki

from LangDeckGen.AnkiCard import AnkiCard
from LangDeckGen.AnkiDeck import AnkiDeck
from LangDeckGen.AnkiModel import AnkiModel
#from LangDeckGen.WordList import WordList
import wget 
class WordList:
    def __init__(self, lang, index):
        self.lang = lang
        if index == 'automatic':
            self.i_idx = 0
            self.f_idx = None
            self.length = None
        if isinstance(index,int):
            print(f'Length of WordList specified: {index}.')
            self.f_idx = index
            self.i_idx = 0
            self.length = index
        elif isinstance(index,list):
            self.i_idx, self.f_idx = index
            if self.f_idx is not None:
                self.length = self.f_idx - self.i_idx
            else:
                self.length = None
            print(f'Wordlists starts and end at: {self.i_idx} {self.f_idx}')
        self.rawlist = ""
        self.translation_list = []

    def __str__(self):
        return f"WordList(Language: {self.lang},\n Length: {self.length},\n List: {self.translation_list})"

    def downloadWordList(self):
        self.rawlist=self.__download_raw_word_list()
#        self.__process_list(self.rawlist)

    def __download_raw_word_list(self):
        url = f"https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/{self.lang}/{self.lang}_50k.txt"
        filename = wget.download(url)
        newtxt=""
        with open(filename, "r") as f:
            lines=f.readlines()
            for line in lines:
                newtxt+=line.split()[0]+f"; {self.lang}; 1\n"
        with open(filename,"w") as f:
            f.write(newtxt)
        return filename

    def __process_list(self, filename):
        newtxt=""
        with open(filename, "r") as f:
            lines=f.readlines()
            for line in lines:
                if len(line.split(';')) <= 2: ## so dont do this over again
                    newtxt+=line.strip()+f"; {self.lang}; 1\n"
                else:
                    newtxt+=line.strip()+"\n"
        with open(filename,"w") as f:
            f.write(newtxt)

    def importWordList(self, csv_file="", rawList=True) -> list:
        if csv_file == "": ## if nothing specified gets default from lang
            csv_file=f"{self.lang}_50k.txt"

        if rawList: ## case it just contains the phrases line by line
            self.__process_list(csv_file) ## it will read the file and add ; {selflang}

        translation_list = list()
        try:
            with Path(csv_file).open(encoding="utf-8") as stream:
                reader = csv.reader(stream,delimiter=';')
                for row in reader:
                    translation_list.append(row)
        except FileNotFoundError:
            logging.critical(f"Unable to locate '{csv_file}'. Check it exists.")
            sys.exit(errno.EIO)
        except TypeError:
            logging.critical(f"Unable to load '{csv_file}'. Check it is populated.")
            sys.exit(errno.EIO)
        else:
            self.translation_list=translation_list[self.i_idx:self.f_idx] ## returns list up to length specified
    
    def filterWordList(self, entries_to_filter):
        new_translation_list = []
        list_included=[]
        for sublist in self.translation_list:
            if sublist[0] not in entries_to_filter:
                if sublist[0] not in list_included:
                    print('included',list_included)
                    new_translation_list.append(sublist)
                    list_included.append(sublist[0])
        self.translation_list=new_translation_list
