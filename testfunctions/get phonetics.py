import requests

word = 'example'
url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'

response = requests.get(url)
data = response.json()

# 提取音标
if isinstance(data, list) and len(data) > 0:
    phonetics_list = data[0].get('phonetics', [])
    ipa_transcriptions = [phonetic.get('text', '') for phonetic in phonetics_list]
    print(f"The IPA transcription(s) of '{word}': {ipa_transcriptions}")
else:
    print("Word not found or no IPA transcription available")
