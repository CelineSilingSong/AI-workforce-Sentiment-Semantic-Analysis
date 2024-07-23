from googletrans import Translator

translator = Translator()

string = 'bonjour'
translated_description = translator.translate(string, src = 'fr', dest = 'en').text
print(translated_description)