"""
WordList.py — Class for Managing Word Lists

This module handles the downloading, processing, and filtering of word frequency lists used for generating Anki decks.
It manages raw data from language-specific lists, processes them, and stores them for use in creating Anki cards.
"""

import csv
import errno
import logging
import sys
from pathlib import Path

from LangDeckGen.AnkiCard import AnkiCard
from LangDeckGen.AnkiDeck import AnkiDeck
from LangDeckGen.AnkiModel import AnkiModel

import wget 
class WordList:
    """
    Class: WordList
    
    This class manages word lists, including downloading raw frequency lists, processing them into a standardized format, 
    and filtering entries. It supports a variety of list formats and index ranges.
    """
    def __init__(self, lang, index):
        """
        Initializes the WordList object with a specific language and index range.

        Parameters:
        - lang (str): The language for which the word list is relevant (e.g., 'fr' for French).
        - index (int, list, or 'automatic'): Specifies the range of words to include:
            - 'automatic': Use default index (start at 0).
            - int: Specifies the length of the word list (i.e., number of entries).
            - list: A pair [i_idx, f_idx] specifying the start and end index for the word list.
        
        Attributes:
        - lang: Language code.
        - i_idx, f_idx: Start and end indices for the list (if specified).
        - length: Length of the word list (based on index).
        - rawlist: Stores the raw downloaded word list.
        - translation_list: Processed list of word translations.
        """
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
        """
        Returns a string representation of the WordList object, including the language, length, and word list.
        """
        return f"WordList(Language: {self.lang},\n Length: {self.length},\n List: {self.translation_list})"

    def downloadWordList(self):
        """
        Downloads the raw word list from the Hermit Dave repository and stores it as `rawlist`.
        """
        self.rawlist=self.__download_raw_word_list()

    def __download_raw_word_list(self):
        """
        Helper function to download the raw word list based on the language.

        Returns:
        - filename (str): The name of the downloaded word list file.
        
        Process:
        - Downloads the word list from Hermit Dave's frequency words repository.
        - Reformats the list to include the language and frequency count.
        """
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
        """
        Helper function to process the raw word list and reformat lines by appending the language and frequency.

        Parameters:
        - filename (str): The file path to the word list to be processed.
        """
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
        """
        Imports the word list, processes it if necessary, and converts it into a list of translations.

        Parameters:
        - csv_file (str): The path to the CSV file. If not specified, the default language list is used.
        - rawList (bool): Whether the word list is raw and needs processing.

        Process:
        - If `rawList` is True, calls `__process_list` to format the file.
        - Reads the CSV file, splitting entries by semicolons (';'), and populates `translation_list` based on the start and end indices.

        Returns:
        - list: The processed translation list.
        """
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
        """
        Filters out specific words from the translation list to avoid duplicates or irrelevant entries.

        Parameters:
        - entries_to_filter (list): List of words to be filtered from the translation list.
        
        Process:
        - Iterates through the translation list and excludes any words found in `entries_to_filter`.
        - Ensures no duplicate entries are added to the new translation list.
        """
        new_translation_list = []
        list_included=[]
        for sublist in self.translation_list:
            if sublist[0] not in entries_to_filter:
                if sublist[0] not in list_included:
                    print('included',list_included)
                    new_translation_list.append(sublist)
                    list_included.append(sublist[0])
        self.translation_list=new_translation_list
