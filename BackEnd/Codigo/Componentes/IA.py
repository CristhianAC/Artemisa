import openai
from .Miscelania import Miscelania
class Openaai:
    def __init__(self, db, miscelanea:Miscelania = None) -> None:
        
        
        openai.api_key = "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"
        structure = [
            {"role" : "user", "content": miscelanea.generarResumenTextualRegion(db)},
        ]
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = structure,
            max_tokens = 250,
            temperature = 0.7,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0
        )
        print(response['choices'][0]['message']['content'])
openaiii = Openaai()