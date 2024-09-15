#!/usr/bin/env pipenv run python
# -*- coding: utf-8 -*-
"""
Main script for creating an Anki deck from a word list and phrases.
"""

import logging
import os
from LangDeckGen.WordList import WordList
from LangDeckGen.LangDeck import LangDeck

def main():
    """
    Main function to create an Anki deck from word and phrase lists.
    """
    # Configure logging to display informational messages
    logging.basicConfig(level=logging.INFO)

    # Set API key for Pixabay (otherwise bing images will be used)
    os.environ['PIXABAY_KEY'] = 'API-KEY-FOR-PIXABAY'

    # Initialize a WordList object with the language code and number of entries
    myWordList = WordList("de", 25)
    
    # Example 1: Download and process the word list
    myWordList.downloadWordList()
    myWordList.importWordList(csv_file=myWordList.rawlist)
    PhrasesOnly = False
    deck_name = "GermanDW_words"

    # Example 2: Import phrases from a specified file into the WordList object
    # myWordList.importWordList(csv_file="de_phrs_clear.txt")
    # PhrasesOnly = False
    # Define the name of the Anki deck
    # deck_name = "GermanDW_A1"

    # Print the WordList object for verification
    print(myWordList)
    
    
    
    # Create a LangDeck object with the specified deck name, WordList, and additional options
    myLangDeck = LangDeck(deck_name, myWordList, tts_speed=1.5, PhrasesOnly=PhrasesOnly)
    
    # Note: The 'tts_speed' and 'PhrasesOnly' parameters are specific to the LangDeck class

if __name__ == '__main__':
    main()
