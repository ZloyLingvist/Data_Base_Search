import re
import math
from collections import Counter

def get_cosine(vec1, vec2):
    A=set(vec1.keys())
    B=set(vec2.keys())
    
    intersection =  A.intersection(B)
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def get_jaccard(vec1, vec2):
    A=set(vec1.keys())
    B=set(vec2.keys())
    intersection =  A.intersection(B)
    union=A.union(B)

    if len(union)!=0:
        return float(len(intersection)) / len(union)
    else:
        return 0.0

   
def text_to_vector(text):
    word = re.compile(r'\w+')
    words = word.findall(text)
    return Counter(words)


def get_result(content_a, content_b,mode):
    text1 = content_a
    text2 = content_b

    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    if mode==1:
        cosine_result = get_cosine(vector1, vector2)
        return cosine_result

    if mode==2:
        jaccard_result=get_jaccard(vector1,vector2)
        return jaccard_result


