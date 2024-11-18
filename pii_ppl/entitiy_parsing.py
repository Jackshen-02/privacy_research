from openai import OpenAI
import re
import json
import os

with open('input/secret.json', 'r', encoding='UTF-8') as file:
        secret_json = json.load(file)
API_KEY = secret_json['OPENAI_API_KEY']
client = OpenAI(api_key =API_KEY)
FULL_TEXT = 0
D = {'NAME_STUDENT': ('@@@','###'), 
      'URL_PERSONAL':('&&&','$$$'),
      'EMAIL':('QQQ','^^^'),
      'PHONE_NUM':(r'%%%',r'~~~'),
     }
PATTERN = r'@@@(.*?)###|&&&(.*?)\$\$\$|QQQ(.*?)\^\^\^|%%%(.*?)~~~'

IndexTable =[key for key in D.keys()]

def count_special_token(text:str)->int:
    #params: text: string of annotated text
    #output: number of special tokens(in num_chars) in the input text, int
    acc = 0
    for val in D.values():
 
        tok1,tok2 = val
        #print(f'{tok1} count:',text.count(tok1))
        #print(f'{tok2} count:',text.count(tok2))
        acc += text.count(tok1)*3 + text.count(tok2)*3
    return acc

def parse_return(text:str): 
    #param: string of annotated text
    #output: string * string * int * int list, string of entity name, string of entity type, int * int of start and end index 

    matches = re.finditer(PATTERN, text)
    extracted_matches = []
    #extract all the matched sub-string
    
    for match in matches:
        for i in range(1,len(match.groups())+1):
            match_text = match.group(i)

            if match_text != None:
                label = IndexTable[i-1]
                offset = count_special_token(text[:match.start(i)])
                start_index = match.start(i) - offset
                end_index = match.end(i) - offset

                extracted_matches.append([match_text, label,start_index, end_index])
    return extracted_matches 


def get_gpt_response(input_text:str) -> str:
    #param: string of text to be annotated 
    #out: string of text annotated 

    system_prompt = 'You are an expert in labeling personally identifiable information'

    ins_prompt = 'Label the entity of the following text: @@@,### to label student name; &&&,$$$ to label personal URL; QQQ,^^^ to label personal email; %%%,~~~ to label phone number\n'

    response = client.chat.completions.create(
    model="ft:gpt-4o-mini-2024-07-18:cmu-plus::A7fVfDc8",
    messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": ins_prompt + input_text}],
    temperature = 0)
    return response.choices[0].message.content 



def add_document(
    main_dict,
    identifier: str,
    text: str,
    entities
) -> None:
    """
    Adds a document with its text and entities to the main dictionary.

    Parameters:
    - main_dict (Dict[str, Dict]): The main dictionary holding all documents.
    - identifier (str): A unique identifier for the document (e.g., "doc1").
    - text (str): The main text of the document.
    - entities (List[List]): A list of entities, each represented as
      [entity_text (str), entity_type (str), start_pos (int), end_pos (int)].

    Returns:
    - None: The function updates the main_dict in place.
    """
    main_dict[identifier] = {
        "text": text,
        "entities": [
            {
                "entity_text": entity[0],
                "type": entity[1],
                "positions": [
                    entity[2],
                    entity[3]
                ]
            }
            for entity in entities
        ]
    }



def extract_parse_store(text_list,identifier_list,directory):
    res = dict()
    for (text,label) in zip(text_list, identifier_list): 
        response = get_gpt_response(text)
        entities = parse_return(response)
        add_document(res,label,text,entities)
    file_path = os.path.join(directory, "gpt_result.json")
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' is ready.")
    except Exception as e:
        print(f"Error creating directory '{directory}': {e}")
        return
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(res, json_file, indent=4)
        print(f"JSON data successfully saved to '{file_path}'.")
    except Exception as e:
        print(f"Error saving JSON to '{file_path}': {e}")
    

