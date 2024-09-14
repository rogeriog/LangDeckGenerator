"""
This module defines templates for Anki flashcards used in language learning.

MODEL_TEMPLATES:
    A list of dictionaries where each dictionary represents a template for a flashcard.
    - "name": The name of the template.
    - "qfmt": The front template format, which includes placeholders for the target language word, audio, and image.
    - "afmt": The back template format, which includes placeholders for the target language word, audio, English translation, and optional phrases with hints.

MODEL_TEMPLATES_PHR:
    A list of dictionaries where each dictionary represents a template specifically for phrase flashcards.
    - "name": The name of the template.
    - "qfmt": The front template format, similar to MODEL_TEMPLATES.
    - "afmt": The back template format, which includes placeholders for the target language word, audio, and English translation.

"""
MODEL_TEMPLATES = [
    {
        "name": "TL to English",
        # Front template format
        "qfmt": """
{{Word_TL}}{{Audio_Word}}<br>
{{Image_Word}}
        """,
        # Back template Format
        "afmt": """
{{Word_TL}}
{{Audio_Word}}


<hr id=answer>

{{Word_EN}}

<hr>

{{#Phr1_TL}}
<div style='font-family: Arial; font-size: 16px;'>{{Phr1_TL}}{{Audio_P1}}</div>
<div style='font-family: Arial; font-size: 14px;'>{{hint:Phr1_EN}}</div><br>
{{/Phr1_TL}}

{{#Phr2_TL}}
<div style='font-family: Arial; font-size: 16px;'>{{Phr2_TL}}{{Audio_P2}}</div>
<div style='font-family: Arial; font-size: 14px;'>{{hint:Phr2_EN}}</div><br>
{{/Phr2_TL}}

{{#Dict_Entry}}
<div style='font-family: Arial; font-size: 14px;'>{{hint:Dict_Entry}}</div><br>
{{/Dict_Entry}}
        """
    },]
MODEL_TEMPLATES_PHR = [
    {
        "name": "TL to English - Phrases",
        # Front template format
        "qfmt": """
{{Word_TL}}{{Audio_Word}}<br>
{{Image_Word}}
        """,
        # Back template Format
        "afmt": """
{{Word_TL}}
{{Audio_Word}}


<hr id=answer>

{{Word_EN}}

        """
    },
]
#{{#Satz4_TL}}
#<div style='font-family: Arial; font-size: 16px;'>{{Satz4_TL}}{{Audio_P4}}</div>
#<div style='font-family: Arial; font-size: 14px;'>{{hint:Satz4_EN}}</div><br>
#{{/Satz4_TL}}
