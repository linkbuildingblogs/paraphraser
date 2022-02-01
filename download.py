from parrot import Parrot
import string
import torch
import warnings
from nltk import tokenize
import re
import nltk
nltk.download('punkt')

#Init models (make sure you init ONLY once if you integrate this to your code)
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")
