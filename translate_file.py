from deep_translator import GoogleTranslator
import json
import sys

def load_knowledge_base(file_path: str):
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
        return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
dff=load_knowledge_base('Database_fr.json')
df:dict=load_knowledge_base('knowledge_base_eng.json')

df=df["questions"]

#translation=translator.translate()
def translate(df):
    i=0
    for sentence in df[i:]:
        try:

                question = GoogleTranslator(source='en', target='fr').translate(sentence['question'])
                answer = GoogleTranslator(source='en', target='fr').translate(sentence['answer'])
                dff['questions'].append({"question":question,"answer":answer})
                save_knowledge_base("Database_fr.json",dff)
                i+=1
                print(i)


        except Exception as e:
                print('error1')



