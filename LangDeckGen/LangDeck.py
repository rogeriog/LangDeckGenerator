import genanki
from LangDeckGen.AnkiCard import AnkiCard
from LangDeckGen import WordList
from LangDeckGen.AnkiDeck import AnkiDeck
from LangDeckGen.AnkiModel import AnkiModel
from time import sleep
import logging
import shutil
class LangDeck:
    def __init__(self, deck_name: str, wordlist: WordList, **kwargs):
        self.deck_name = deck_name
        self.wordlist=wordlist
        self.deck=self.createLangDeck(self.deck_name,self.wordlist,**kwargs)
        self.package=self.packageLangDeck(self.deck,**kwargs)
        self.outputLangDeck(self.package)
        self.clearMedia()

    def createLangDeck(self, deck_name, wordlist, **kwargs) -> AnkiDeck:
        def chunk_list (mylist,x):
            return [mylist[i:i+x] for i in range(0, len(mylist), x)]
        deck_name = deck_name.replace(" ","-")
        anki_model = AnkiModel(**kwargs)
        anki_cards = list()
        chunk_size=kwargs.get('chunk_size',10)
        for chunk in chunk_list(wordlist.translation_list,chunk_size):
            ## this loop inserts entries, chunk_size entries at a time
            for entry in chunk:
                word,lang=map(str.strip,entry[:2])
                args=list(map(str.strip,entry[2:]))
                try:
                    anki_card=AnkiCard(str(word),str(lang),*args,**kwargs)
                    anki_cards.append(anki_card)
                except Exception as e:
                    print(e)
                    print(f"Coundnt generate card for {word}.")
                sleep(2)
                logging.info(f"[ {word} ] card added. Sleeping for 2 seconds.")
            ## this part will output a langdeck, it increments at every 10.
            deck = AnkiDeck(title=deck_name, anki_cards=anki_cards)
            deck_notes = deck.create_notes(anki_model,**kwargs)
            for note in deck_notes:
                deck.add_note(note)
            logging.info("Waiting 60 s to start next chunk of cards...")
            sleep(60) ## sleep so site doesnt complain
            package=self.packageLangDeck(deck,**kwargs)
            self.outputLangDeck(package) ## generates partial deck every 10 new entries
        #self.clearMedia()
        return deck

    def packageLangDeck(self,deck,**kwargs):
        def package_deck(new_deck: genanki.Deck, media: list) -> genanki.Package:
            TL_package = genanki.Package(new_deck)
            TL_package.media_files = media
            return TL_package
        package = deck.package_deck(deck,**kwargs)
        return package

    def outputLangDeck(self,package):
        package.write_to_file(f"{self.deck_name}.apkg")

    def clearMedia(self):
        shutil.rmtree("./tmp/imgs")
        shutil.rmtree("./tmp/sound")
