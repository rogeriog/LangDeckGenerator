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

    # Set API key for Pixabay (if required by the application)
    os.environ['PIXABAY_KEY'] = 'API-KEY-FOR-PIXABAY'

    # Initialize a WordList object with the language code and number of entries
    myWordList = WordList("de", 25)
    
    # Download and process the word list
    myWordList.downloadWordList()
    
    # Import phrases from a specified file into the WordList object
    myWordList.importWordList(csv_file="de_phrs_clear.txt")
    
    # Print the WordList object for verification
    print(myWordList)
    
    # Define the name of the Anki deck
    deck_name = "GermanDW_A1"
    
    # Create a LangDeck object with the specified deck name, WordList, and additional options
    myLangDeck = LangDeck(deck_name, myWordList, tts_speed=1.5, PhrasesOnly=True)
    
    # Note: The 'tts_speed' and 'PhrasesOnly' parameters are specific to the LangDeck class

if __name__ == '__main__':
    main()
