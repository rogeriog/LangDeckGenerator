#!/usr/bin/env pipenv run python
# -*- coding: utf-8 -*-
import logging
import os
from LangDeckGen.WordList import WordList
from LangDeckGen.LangDeck import LangDeck
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    os.environ['PIXABAY_KEY'] = 'API-KEY-FOR-PIXABAY'
    ## create language deck from wordfrequency data
    ## how many entries will you get from the list

    myWordList=WordList("de",25)
    myWordList.downloadWordList()
    myWordList.importWordList(csv_file="de_phrs_clear.txt") 
    print(myWordList)
    ## defaults to read from "lang_50k.txt", 
    ## specify another with csv_file="path_and_name_of_file"
    # deck_name = input("Please enter your deck name: ")
    deck_name = "GermanDW_A1"
    myLangDeck=LangDeck(deck_name, myWordList,tts_speed=1.5,PhrasesOnly=True)
    # import the word list
