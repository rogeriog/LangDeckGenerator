

# LangDeckGen

**LangDeckGen** is a Python package for generating Anki decks from word and phrase lists. It allows you to create decks for language learning using frequency-based word lists and custom phrases.

## Overview

This repository includes scripts and modules to:
- Download and process word lists.
- Generate Anki decks with vocabulary and phrases.
- Customize the deck with audio, images, and specific formats.

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/rogeriog/LangDeckGenerator.git
   cd LangDeckGen
   ```

2. **Install dependencies using Pipenv:**

   ```sh
   pipenv install
   ```

3. **Activate the virtual environment:**

   ```sh
   pipenv shell
   ```

## Usage

### File Structure

- **`LangDeck.py`**: Contains the `LangDeck` class to create and package Anki decks.
- **`WordList.py`**: Contains the `WordList` class to manage and process word lists.
- **`AnkiDeck.py`**: Contains the `AnkiDeck` class to handle Anki deck-specific operations.
- **`AnkiModel.py`**: Contains the `AnkiModel` class for defining Anki card models.
- **`de_phrs_clear.txt`**: Example file with phrases in the format: `phrase; language; 1`.

### Creating a Deck

1. **Prepare your word list and phrases file:**

   Place your word and phrase lists in the same directory or specify the path.

2. **Run the main script:**

   ```sh
   python main.py
   ```

   The script will:
   - Download a default word list.
   - Import phrases from the `de_phrs_clear.txt` file.
   - Generate an Anki deck with the name `GermanDW_A1`.

   The main file (`main.py`) example:

   ```python
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
       logging.basicConfig(level=logging.INFO)
       os.environ['PIXABAY_KEY'] = 'API-KEY-FOR-PIXABAY'

       myWordList = WordList("de", 25)
       myWordList.downloadWordList()
       myWordList.importWordList(csv_file="de_phrs_clear.txt")
       print(myWordList)

       deck_name = "GermanDW_A1"
       myLangDeck = LangDeck(deck_name, myWordList, tts_speed=1.5, PhrasesOnly=True)

   if __name__ == '__main__':
       main()
   ```

## Classes and Methods

### `WordList`

- **`__init__(self, lang, index)`**: Initializes the WordList with language and index.
- **`downloadWordList(self)`**: Downloads the word list from the web.
- **`importWordList(self, csv_file="", rawList=True)`**: Imports phrases from a specified file.
- **`filterWordList(self, entries_to_filter)`**: Filters the word list based on specified criteria.

### `LangDeck`

- **`__init__(self, deck_name: str, wordlist: WordList, **kwargs)`**: Initializes the LangDeck and creates the Anki deck.
- **`createLangDeck(self, deck_name, wordlist, **kwargs)`**: Creates the Anki deck from the word list.
- **`packageLangDeck(self, deck, **kwargs)`**: Packages the deck with media files.
- **`outputLangDeck(self, package)`**: Writes the deck to a file.
- **`clearMedia(self)`**: Clears temporary media files.

### `AnkiDeck`

- **`__init__(self, title: str, anki_cards: List[AnkiCard], **kwargs)`**: Initializes the AnkiDeck.
- **`package_deck(self, anki_deck: genanki.Deck, **kwargs)`**: Packages the deck with media files.
- **`create_notes(self, model: genanki.Model, **kwargs)`**: Creates notes for the deck based on the card model.

### `AnkiModel`

- **`__init__(self, **kwargs)`**: Initializes the AnkiModel with fields, templates, and CSS.
- **`__create_id(self, name: str)`**: Creates a unique model ID based on the name.

## Contribution

Feel free to contribute to this project by submitting issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Replace placeholders such as `your-username` and `API-KEY-FOR-PIXABAY` with the appropriate values before using the README. This structure should give users clear guidance on setting up, using, and contributing to your project.