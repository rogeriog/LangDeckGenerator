from pathlib import Path

import genanki
import LangDeckGen
from LangDeckGen import AnkiTemplates
import os
import random

class AnkiModel(genanki.Model):
    try: 
        os.mkdir("./tmp")
    except Exception as e:
        print(e)
    try: 
        os.mkdir("./tmp/sound")
    except Exception as e:
        print(e)
    try: 
        os.mkdir("./tmp/imgs")
    except Exception as e:
        print(e)
    model_id = str
    fields = [
        {"name": "Word_TL"},
        {"name": "Word_EN"},
        {"name": "Audio_Word"},
        {"name": "Phr1_TL"},
        {"name": "Phr1_EN"},
        {"name": "Audio_P1"},
        {"name": "Phr2_TL"},
        {"name": "Phr2_EN"},
        {"name": "Audio_P2"},
       # {"name": "Phr3_TL"},
       # {"name": "Phr3_EN"},
       # {"name": "Audio_P3"},
        {"name": "Image_Word"},
        {"name": "Dict_Entry"},
#        {"name": "Phr4_TL"},
#        {"name": "Phr4_EN"},
#        {"name": "Audio_S4"},
    ]
    fields_phrs = [
        {"name": "Word_TL"},
        {"name": "Word_EN"},
        {"name": "Audio_Word"},
        {"name": "Image_Word"},
    ]
    templates = AnkiTemplates.MODEL_TEMPLATES
    templates_phr = AnkiTemplates.MODEL_TEMPLATES_PHR
    packagefolder=Path(LangDeckGen.__file__).parent
    css_file= packagefolder / Path("templates/anki.css")
    css = css_file.open().read()

    def __init__(self, **kwargs):
        if not kwargs.get("PhrasesOnly"):
            super(AnkiModel, self).__init__(name="Simple Vocabulary",
                                            model_id=self.__create_id("Simple Vocabulary"), 
                                            fields=self.fields,
                                            templates=self.templates,
                                            css=self.css)
        else:
            super(AnkiModel, self).__init__(name="Simple Vocabulary2",
                                            model_id=self.__create_id("Simple Vocabulary2"), 
                                            fields=self.fields_phrs,
                                            templates=self.templates_phr,
                                            css=self.css)

    def __create_id(self,name : str):
        id=0
        for char in name:
            id+=ord(char)
        return id


    def __str__(self):
        return f"<AnkiModel {self.model_id}>"

