from typing import List

import genanki
from LangDeckGen.AnkiCard import AnkiCard


class AnkiDeck(genanki.Deck):
    deck_id = str
    anki_cards = List[AnkiCard]
    model = genanki.Model

    def __init__(self, title: str, anki_cards: List[AnkiCard], **kwargs):
        super().__init__(name=title, deck_id=hash(title))
        self.anki_cards = anki_cards

    def __build_media_lib(self,**kwargs):
        media = list()
        for card in self.anki_cards:
            media.append(card.image)
            media.append(card.audio)
            if not kwargs.get("PhrasesOnly"):
                media.extend(card.sentence_audio)
        return media

    def package_deck(self, anki_deck: genanki.Deck, **kwargs) -> genanki.Package:
        package = genanki.Package(anki_deck)
        package.media_files = self.__build_media_lib(**kwargs)
        return package

    def create_notes(self, model: genanki.Model,**kwargs):
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
        return print(f"<AnkiDeck {self.name} {self.deck_id} {len(self.anki_cards)}>")
