import stanza
import os

path = os.path.dirname(os.path.dirname(__file__))
stanza.download('ru',processors='tokenize,lemma,pos,depparse',dir=path+"\stanza_resources",package='syntagrus')
