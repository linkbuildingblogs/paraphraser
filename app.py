import spacy
import en_core_web_sm
from fastapi import FastAPI , Response, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import nest_asyncio
import uvicorn
nlp = en_core_web_sm.load()
from sentence_splitter import SentenceSplitter, split_text_into_sentences
splitter = SentenceSplitter(language='en')
from parrot import Parrot
import string
import torch
import warnings
from nltk import tokenize
import re
import nltk
nltk.download('punkt')
warnings.filterwarnings("ignore")

#uncomment to get reproducable paraphrase generations
def random_state(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)
random_state(1234)

#Init models (make sure you init ONLY once if you integrate this to your code)
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")

def paraphrase(text):
  phrases = splitter.split(text)
  while("" in phrases) :
    phrases.remove("")
  paraphrased_list = []
  for phrase in phrases:
    para_phrases = parrot.augment(input_phrase=phrase, use_gpu=False)
    if para_phrases==None:
      paraphrased_list.append(phrase)
    else:
      score_list = []
      for i in range(len(para_phrases)):
        score_list.append(para_phrases[i][1])
      for i in range(len(para_phrases)):
        if para_phrases[i][1]==max(score_list):
          paraphrased_list.append(para_phrases[i][0].capitalize()+'.')
    text = ' '.join(paraphrased_list)
    text = re.sub(r'[\?\.\!]+(?=[\?\.\!])', '', text)
  return text

def listToString(s): 
    str1 = " " 
    txt = str1.join(s)
    text = re.sub(r"[-\"#/@;:<>{}=~|]", "", txt)
    return text

def deliver(sentence):
    stripped = []
    for i in tokenize.sent_tokenize(sentence):
        if "." in i:
            stripped.append(i)
        else:
            pass
    return {"CONTENT":listToString(stripped) , "CHAR COUNT": sum([i.strip(string.punctuation).isalpha() for i in sentence.split()])}

app = FastAPI(
    title='LBB Paraphraser API', openapi_url='/openapi.json', docs_url='/docs',
    description='paraphraser app'
)

@app.get('/')
async def home():
    return {"message": "Paraphaser System is Live ✔"}

@app.post('/paraphrase')
async def home(Text: str , request: Request):
  text_unicode = paraphrase(text=Text)
  text_encode = text_unicode.encode(encoding="ascii", errors="ignore")
  text_decode = text_encode.decode()
  clean_text = " ".join([word for word in text_decode.split()])
  return deliver(clean_text)
