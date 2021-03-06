from collections import defaultdict
import yaml
import pymorphy2
import os

path = os.path.dirname(os.path.dirname(__file__)) or '.'
morph = pymorphy2.MorphAnalyzer()


def load_synonyms(file):
    try:
        data = yaml.load(open(file, 'rt', encoding='utf8'), Loader=yaml.FullLoader)
        d = {}
        for k, v in data.items():
            for x in v: d[x] = k
        return d
    except FileNotFoundError:
        print(f'cannot open synonym dictionary {file}')
        return {}


def load_set(file):
    try:
        data = yaml.load(open(file, 'rt', encoding='utf8'), Loader=yaml.FullLoader)
        # print(data)
        return set(data)
    except FileNotFoundError:
        print(f'error: cannot open file {file}')
        return set()


synonyms = load_synonyms(path + '/Files/synonyms-kw.yml')
skip_words = load_set(path + '/Files/skip.yml')


def get_normal_form(word: str):
    if word[0].isascii():
        return synonyms.get(word, word)
    p = morph.parse(word)[0]
    return synonyms.get(p.normal_form, p.normal_form)


def in_skip(word: str):
    if word[0].isascii():
        return word in skip_words
    p = morph.parse(word)[0]
    return p.normal_form in skip_words


def is_prep(word: str):
    if word[0].isascii():
        return False
    p = morph.parse(word)[0]
    return p.tag.POS == 'PREP'


def simple_tokenize(text: str):
    curr = ''

    def add(cc=''):
        nonlocal curr
        if curr: yield curr
        curr = cc

    for c in text:
        if c.isspace():
            yield from add()
        elif curr == '' or curr[-1] == '\\':
            curr += c
        elif curr[-1].isalpha() and c.isalpha():
            curr += c
        elif curr[-1].isnumeric() and c.isnumeric():
            curr += c
        else:
            yield from add(c)
    yield from add()


def canonical_form(x: str, normal_form=get_normal_form, skip=in_skip):
    separators = {',', '.', '\\displaystyle'}
    if x in separators: return '.'
    if skip(x): return None

    return normal_form(x)


def convert_text(text, tokenize=simple_tokenize, get_canonical=canonical_form, **kwargs):
    tokens = tokenize(text)
    w = [get_canonical(x, **kwargs) for x in tokens]
    return [x for x in w if x]


def get_text_stats(words, sep='.', use_pairs=True):
    st = defaultdict(lambda: 0.)
    for w in words:
        if w != sep: st[w] = 1
    if use_pairs:
        for i, x in enumerate(words[:-1]):
            if x == sep: continue
            for j, y in enumerate(words[i + 1:]):
                if y == sep: break
                st[(x, y)] += 1 / 1.2 ** j
                st[(y, x)] += 0.5 / 1.2 ** j
    return st


class SimpleDB:
    def __init__(self, texts, stats_func=get_text_stats, convert_opts={}, stats_opts={}):
        self._stats_func = stats_func
        self._stats_params = stats_opts
        self._convert_opts = convert_opts
        self._texts = texts
        self._toks = [convert_text(s, **convert_opts) for s in texts]
        self._stats = [stats_func(x, **stats_opts) for x in self._toks]

        s = defaultdict(lambda: 0)
        for st in self._stats:
            for x, y in st.items():
                s[x] += y
        self._wt = defaultdict(lambda: 0)
        self._wt.update({x: 1 / y for (x, y) in s.items()})

    def ranger(self, text):
        toks = convert_text(text, **self._convert_opts)
        # print(f'toks = {toks}')
        stats = self._stats_func(toks, **self._stats_params)
        rks = [self._diff_stats(stats, st) for st in self._stats]
        # print(f'ranks = {rks}')
        idx = sorted(range(len(rks)), key=lambda i: rks[i], reverse=True)
        return [(i, rks[i]) for i in idx]

    def _diff_stats(self, st1, st2):
        keys = set(st1) | set(st2)

        mx = sum(self._wt[k] * max(st1[k], st2[k]) for k in keys)
        mn = sum(self._wt[k] * min(st1[k], st2[k]) for k in keys)

        return mn / mx


class Tester:
    def __init__(self, fn, **kwargs):
        self._data = yaml.load(open(fn, 'rt', encoding='utf8'), Loader=yaml.FullLoader)
        if type(self._data) is dict:
            self._data = list(self._data.items())
        else:
            self._data = sum((list(x.items()) if type(x) is dict else [x] for x in self._data), [])
        self._db = SimpleDB([y for _, y in self._data], **kwargs)

    def test(self):
        n = len(self._data)

        results = []
        order_list = []

        for i in range(n):
            key, text = self._data[i]
            order = self._db.ranger(text)
            r = 0
            k = 0

            for idx, _ in order:
                if self._data[idx][0] == i:
                    continue
                if self._data[idx][0] != key:
                    k += 1
                else:
                    r = k

            order_list.append(order)
            results.append(f"{1 - r / n:.3f}")

        return results, order_list


def keyword_search():
    file = path + '/Temp/label_list.yml'
    t = Tester(file)
    res, order = t.test()
    return res, order
