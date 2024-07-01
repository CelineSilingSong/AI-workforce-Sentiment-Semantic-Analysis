from googletrans import Translator

translator = Translator()

text = 'Artificial Intelligence'
translated = translator.translate(text, dest='pt').text
print(translated)

#languages_info = [
#    {'dest':'en','hl': 'en-US', 'gl': 'US', 'ceid': 'US:en'},
#    {'dest':'en','hl': 'en-GB', 'gl': 'GB', 'ceid': 'GB:en'},
#    {'dest':'es','hl': 'es-ES', 'gl': 'ES', 'ceid': 'ES:es'},
#    {'dest':'es','hl': 'es-419', 'gl': 'MX', 'ceid': 'MX:es-419'},
#    {'dest':'fr','hl': 'fr-FR', 'gl': 'FR', 'ceid': 'FR:fr'},
#    {'dest':'de','hl': 'de-DE', 'gl': 'DE', 'ceid': 'DE:de'},
#    {'dest':'it','hl': 'it-IT', 'gl': 'IT', 'ceid': 'IT:it'},
#    {'dest':'pt','hl': 'pt-BR', 'gl': 'BR', 'ceid': 'BR:pt-BR'},
#    {'dest':'pt','hl': 'pt-PT', 'gl': 'PT', 'ceid': 'PT:pt'},
#    {'dest':'zh-cn','hl': 'zh-CN', 'gl': 'CN', 'ceid': 'CN:zh-CN'},
#    {'dest':'zh-tw','hl': 'zh-TW', 'gl': 'TW', 'ceid': 'TW:zh-TW'},
#    {'dest':'ja','hl': 'ja-JP', 'gl': 'JP', 'ceid': 'JP:ja-JP'},
#    {'dest':'ko','hl': 'ko-KR', 'gl': 'KR', 'ceid': 'KR:ko-KR'},
#    {'dest':'ru','hl': 'ru-RU', 'gl': 'RU', 'ceid': 'RU:ru-RU'},
#    {'dest':'hi','hl': 'hi-IN', 'gl': 'IN', 'ceid': 'IN:hi-IN'},
#    {'dest':'en','hl': 'en-IN', 'gl': 'IN', 'ceid': 'IN:en-IN'},
#    {'dest':'en','hl': 'en-CA', 'gl': 'CA', 'ceid': 'CA:en'},
#    {'dest':'en','hl': 'en-AU', 'gl': 'AU', 'ceid': 'AU:en'},
#    {'dest':'fr','hl': 'fr-CA', 'gl': 'CA', 'ceid': 'CA:fr'},
#    {'dest':'ar','hl': 'ar', 'gl': 'SA', 'ceid': 'SA:ar'}
#]
#
#topics = ['Education', 'Tech', 'Business', 'Politics', 'Regulation']
#
#query = [
#    ['AI', 'Artificial Intelligence', 'Large Language Models', 'Generative AI'],
#    ['Job', 'Work', 'Workforce', 'employment']
#]
#
#def translate_query(query, language):
#    # Translate each element in the nested array
#    translated_double_array = []
#    for inner_array in query:
#        translated_inner_array = []
#        for text in inner_array:
#            translated = translator.translate(text, dest=language)  
#            translated_inner_array.append(translated.text)
#        translated_double_array.append(translated_inner_array)
#    return translated_double_array
#
#for topic in topics:
#    for language_info in languages_info:
#        if language_info['dest'] != 'en':
#            translated_topic = translator.translate(topic, language_info['dest']).text
#            translated_query = translate_query(query,language_info['dest'])
#            print(translated_topic)
#            print(translated_query)
#
#
#text = 'great'
#translated = translator.translate(text, dest='fr').text
#print(translated)
#
#