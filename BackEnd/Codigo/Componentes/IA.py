import openai
from .Miscelania import Miscelania


class Openaai:
    def __init__(self, miscelanea: Miscelania) -> None:

        self.miscelania = miscelanea
        openai.api_key = "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"

    def generarConclusion(self, db):
        structure = [
            {"role": "user",
                "content": self.miscelania.generarResumenTextualRegion(db)},
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=structure,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['message']['content']
