import os, re, json

def readfiles():
    drct = os.listdir('.')
    texts = []
    data = []
    for name in drct:
        if name.startswith('udm_lexemes_'):
            file = open(name, 'r', encoding = 'utf-8')
            text = file.read()
            data.append(text)
            file.close()
    return data

def make_dict(data):
    lexs = []
    for text in data:
        result = re.findall('lex: (.*?)\n stem: \w+\.\n gramm: (.*?)\n paradigm: [A-Za-z\-_]+\n trans_ru:(.*?)\n', text)
        for el in result:
            lexs.append(el)
    udmrus_dict = {}
    for lex in lexs:
        udmrus_dict[lex[0]] = (lex[1], lex[2].strip(' '))
    return udmrus_dict

def wr_json(s, path):
    file = open(path, 'w', encoding = 'utf-8')
    json.dump(s, file, ensure_ascii=False)
    file.close()

def rev_dict(dct):
    final_dct = {}
    for word in dct:
        res = re.search('[1-9]\.', dct[word][1])
        if res:
            trans = re.split('[1-9]\.', dct[word][1])
            for tran in trans:
                if tran != '':
                    final_dct[tran.strip(' .,')] = (dct[word][0], word)
        else:
            if dct[word][1] != '':
                final_dct[dct[word][1]] = (dct[word][0], word)
    return final_dct

def main():
    udmrus_dict = make_dict(readfiles())
    wr_json(udmrus_dict, 'udmrus_dict.txt')
    rusudm_dict = rev_dict(udmrus_dict)
    wr_json(rusudm_dict, 'rusudm_dict.txt')

if __name__ == '__main__':
    main()
