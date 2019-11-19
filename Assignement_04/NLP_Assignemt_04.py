import nltk
import re
import math

def read_file(file_name='tweets_corpus.txt'):
    with open(file_name,'r',encoding='utf-8') as file:
        text = file.read()
    text = text.translate(str.maketrans('', '', '!"#$%&\()*+,.:;<=>?@[\\]^_`{|}~')).lower()
    return text.split('\n')

def create_dataset(file_name='tweets_corpus.txt'):
    text = read_file(file_name)
    dataset = dict()
    unique_words = ''
    for i in text:
        data = i.split('\t')
        if data.__len__() == 2:
            dataset[data[0]] = data[1]
            unique_words += data[1] + ' '
    print(unique_words)
    unique_words = [key for key in nltk.FreqDist(unique_words.split()).keys()]
    # print(unique_words.__len__())
    unique_words = {words:list() for words in unique_words}
    # print_dict(unique_words)
    return dataset, unique_words

def print_dict(dict):
    for key, val in dict.items():
        print(key,':',val)

def create_inverted_index(dataset, unique_words):

    for key, val in dataset.items():
        for words in val.split():
            inverted_list = unique_words[words]
            # print(inverted_list)
            if type(inverted_list) == 'NonType':
                unique_words[words] = [key]
            else:
            # if len(inverted_list) == 0 or key not in inverted_list:
                inverted_list.append(key)
                unique_words[words] = list(set(inverted_list))
    print_dict(unique_words)
    return unique_words

def merge_query(query_str, inverted_list, dataset):
    universal_doc_list = [key for key in dataset.keys()]
    queries = re.findall('\((.*?)\)', query_str)
    if len(queries) != 0:
        print('Brakets:',queries)
        temp_str = query_str
        for qq in queries:
            # process_string(qq, inverted_list, dataset)
            temp_str = temp_str.replace(qq,'***')
        print(temp_str)
        str_tokenize = temp_str.split()
        result_list = [i for i in range(0, len(str_tokenize))]

        count = 0
        for tokens in enumerate(str_tokenize):
            if tokens[1] == '(***)':
                print('split(strs):',queries[count])
                temp_str_tokenize = queries[count].split()
                temp_result_list = [i for i in range(0, len(temp_str_tokenize))]
                result_list[tokens[0]] = process_string(temp_str_tokenize, temp_result_list, inverted_list, dataset)
                # str_tokenize[tokens[0]] = queries[count]
                print(result_list[tokens[0]])
                count+=1
        return process_string(str_tokenize, result_list, inverted_list, dataset)
    else:
        print(query_str)
        str_tokenize = query_str.split()
        result_list = [i for i in range(0, len(str_tokenize))]
        return process_string(str_tokenize, result_list, inverted_list, dataset)

def process_string(str_tokenize, result_list, inverted_list, dataset):
    i = 0
    while(i < len(str_tokenize)):
        if str_tokenize[i] == 'NOT':
            print(str_tokenize[i + 1])
            result_list[i+1] = NOT(str_tokenize[i+1], inverted_list, dataset)
            str_tokenize.remove('NOT')
            result_list.remove(i)
            i-=1
        if str_tokenize[i] not in ['AND','OR']:
            # print('resultlist', type(result_list))
            if str_tokenize[i] == '(***)':
                i += 1
                continue
            result_list[i] = inverted_list[str_tokenize[i]]
        i+=1

    for a in zip(str_tokenize, result_list):
        print(a[0], a[1])
    print('whole result')

    while(len(str_tokenize) > 1):
        min_index,str_tokenize,result_list = find_min_index(str_tokenize,result_list)
        print('whole result min index')
        print(min_index)
        for a in zip(str_tokenize,result_list):
            print(a[0], a[1])
        str_tokenize, result_list = proceed_Operation(min_index,str_tokenize,result_list)
        print('whole result')
        for a in zip(str_tokenize,result_list):
            print(a[0], a[1])

    print('Final Result:')
    print(result_list[0])
    return result_list[0]

def find_min_index(str_tokenize,result_list):
    min_val = 100000
    min_index = -1
    for i in range(0, len(result_list)):
        if str_tokenize[i] == 'AND':
            if min_val >= min(len(result_list[i-1]),len(result_list[i-1])):
                min_val = min(len(result_list[i-1]),len(result_list[i-1]))
                min_index = i
            result_list[i] = min(len(result_list[i-1]),len(result_list[i-1]))
        elif str_tokenize[i] == 'OR':
            if min_val >= max(len(result_list[i-1]),len(result_list[i-1])):
                min_val = max(len(result_list[i-1]),len(result_list[i-1]))
                min_index = i
            result_list[i] = max(len(result_list[i-1]),len(result_list[i-1]))
    print('Min Index:',min_val)
    return min_index,str_tokenize,result_list

def proceed_Operation(index, str_tokenize,result_list):
    if str_tokenize[index] == 'AND':
        result_list[index-1] = AND(result_list[index-1], result_list[index+1])
        str_tokenize[index-1] = str_tokenize[index-1] + ' ' + str_tokenize[index] + ' ' + str_tokenize[index+1]
    elif str_tokenize[index] == 'OR':
        result_list[index-1] = OR(result_list[index-1], result_list[index+1])
        str_tokenize[index-1] = str_tokenize[index-1] + ' ' + str_tokenize[index] + ' ' + str_tokenize[index+1]

    return str_tokenize[:index] + str_tokenize[index+2:], result_list[:index] + result_list[index+2:]

def OR(list1, list2):
    return list(set(list1).union(set(list2)))

def AND(list1, list2):
    return list(set(list1).intersection(set(list2)))

# def OR(word1, word2, inverted_list):
#     list1 = set(inverted_list[word1])
#     list2 = set(inverted_list[word2])
#     return list(list1.union(list2))

def NOT(word, inverted_list, dataset):
    total_doc_list = [key for key in dataset.keys()]
    print(total_doc_list)
    lists = inverted_list[word]
    print(lists)
    for a in lists:
        print(a)
        total_doc_list.remove(a)
    return total_doc_list

# def AND(word1, word2, inverted_list):
#     list1 = set(inverted_list[word1])
#     list2 = set(inverted_list[word2])
#     return list(list1.intersection(list2))


def TF(word, doc_ID, dataset):
    return dataset[doc_ID].split().count(word) / len(dataset[doc_ID].split())

def IDF(word, dataset, inverted_index):
    return math.log10(len(dataset)/len(inverted_index[word]))

def TF_IDF(word, doc_ID, dataset, inverted_index):
    return TF(word, doc_ID, dataset) * IDF(word, dataset, inverted_index) * 1.0

def TF_IDF_QUERY(query_str, inverted_list, dataset):
    query_result = merge_query(query_str, inverted_list, dataset)
    query_list = [words for words in query_str.split() if words not in ['AND', 'OR', 'NOT']]
    print(query_list)
    TF_IDF_Dict = dict()
    for doc_ID in query_result:
        score = 0.0
        for words in query_list:
            score += TF_IDF(words, doc_ID, dataset, inverted_list)
        TF_IDF_Dict[doc_ID] = score
    for key, val in TF_IDF_Dict.items():
        print(key, ':', val, ':', dataset[key])
    return TF_IDF_Dict

def print_result(lists, dataset):
    for ll in lists:
        print(ll, ':', dataset[ll])

if __name__=='__main__':
    dataset, unique_words = create_dataset()
    inverted_list = create_inverted_index(dataset, unique_words)
    # print_dict(inverted_list)
    query = [
        'egg OR cheese',
        'egg AND NOT cheese',
        'chocolate AND strawberry',
        'eggs AND cheese AND bacon AND chocolate',
        'chocolate OR strawberry OR eggs OR NOT bacon',
        'eggs AND cheese OR strawberry AND NOT chocolate',
        '(eggs AND cheese) OR (eggs AND bacon)'
    ]
    # for q in query:
    results = merge_query(query[6], inverted_list,dataset)
    print_result(results, dataset)
    # TF_IDF_QUERY(query[5], inverted_list,dataset)

