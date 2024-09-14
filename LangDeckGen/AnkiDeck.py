from typing import List
import genanki
from LangDeckGen.AnkiCard import AnkiCard
"""
AnkiDeck.py — Class for Managing Anki Decks

This module extends the genanki.Deck class to manage the creation of Anki decks with custom card details,
including images, audio, and sentences. It handles the packaging of the deck and note creation.
This is based on the discontinued repository of errbufferoverfl/pearl-memory 
"""

class AnkiDeck(genanki.Deck):
    """
    Class: AnkiDeck
    
    Extends the genanki.Deck class to handle custom Anki decks, including card media and note creation.
    """
    deck_id = str
    anki_cards = List[AnkiCard]
    model = genanki.Model

    def __init__(self, title: str, anki_cards: List[AnkiCard], **kwargs):
        """
        Initializes the AnkiDeck object with a title and a list of AnkiCards.

        Parameters:
        - title (str): The name of the deck.
        - anki_cards (List[AnkiCard]): List of AnkiCard objects to be included in the deck.
        - kwargs: Additional keyword arguments.
        """
        super().__init__(name=title, deck_id=hash(title))
        self.anki_cards = anki_cards

    def __build_media_lib(self,**kwargs):
        """
        Builds a list of media files (images and audio) used in the deck.

        Parameters:
        - kwargs: Additional keyword arguments.

        Returns:
        - media (list): List of media file paths.
        """
        media = list()
        for card in self.anki_cards:
            media.append(card.image)
            media.append(card.audio)
            if not kwargs.get("PhrasesOnly"):
                media.extend(card.sentence_audio)
        return media

    def package_deck(self, anki_deck: genanki.Deck, **kwargs) -> genanki.Package:
        """
        Packages the AnkiDeck into a genanki.Package, including media files.

        Parameters:
        - anki_deck (genanki.Deck): The Anki deck to be packaged.
        - kwargs: Additional keyword arguments.

        Returns:
        - package (genanki.Package): The packaged Anki deck.
        """
        package = genanki.Package(anki_deck)
        package.media_files = self.__build_media_lib(**kwargs)
        return package

    def create_notes(self, model: genanki.Model,**kwargs):
        """
        Creates genanki.Note objects from the AnkiCards for the deck.

        Parameters:
        - model (genanki.Model): The Anki model to be used for creating notes.
        - kwargs: Additional keyword arguments.

        Returns:
        - notes (list): List of genanki.Note objects.
        """
        notes = list()
        for card in self.anki_cards:
            if not kwargs.get("PhrasesOnly"):
                notes.append(genanki.Note(
                    model=model,
                    fields=[card.translation_dict["tl"],
                            card.translation_dict["en"],
                            f"[sound:{card.audio.split('/')[-1]}]",
                            card.sentence[0],
                            card.sentence[1],
                            f"[sound:{card.sentence_audio[0].split('/')[-1]}]",
                            card.sentence[2],
                            card.sentence[3],
                            f"[sound:{card.sentence_audio[1].split('/')[-1]}]",
            #                card.sentence[5],
            #                card.sentence[4],
            #                f"[sound:{card.sentence_audio[2]}]",
            #                card.sentence[7],
            #                card.sentence[6],
            #                f"[sound:{card.sentence_audio[3]}]",
                            f"<img src='{card.image.split('/')[-1]}'>",
                            card.dictionary_entry]
                    ))
            else:
                notes.append(genanki.Note(
                    model=model,
                    fields=[card.translation_dict["tl"],
                            card.translation_dict["en"],
                            f"[sound:{card.audio.split('/')[-1]}]",
                            ""]
                            # f"<img src='{card.image.split('/')[-1]}'>"]
                    ))

        return notes

    def __str__(self):
        """
        Returns a string representation of the AnkiDeck object, including the deck name, ID, and number of cards.
        """
        return print(f"<AnkiDeck {self.name} {self.deck_id} {len(self.anki_cards)}>")
