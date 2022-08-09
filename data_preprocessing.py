from numpy import True_
import pandas as pd
import os
import string
import nltk
from textstat.textstat import textstatistics
import re

url_df=pd.read_excel(r'D:\20211030 Test Assignment\Input.xlsx')


def file_name(url_id):
    return str(url_id)
url_df['file_name']=url_df["URL_ID"].apply(file_name)


def data_reader(file_name):
    path=r'D:\20211030 Test Assignment\Extracted text'
    file_path="{}\{}.txt".format(path,file_name)
    with open(file_path,'r', encoding="utf-8") as f:
        return f.read()
url_df["file_data"]=url_df["file_name"].apply(data_reader)



def stopword():
    path=r'D:\20211030 Test Assignment\StopWords'
    stop_word=set()
    for i in os.listdir(path):
        file_path="{}\{}".format(path,i)
        with open(file_path,'r') as f:
            for i in f:
                i=i.strip('\n')
                a=i.split()
                for j in a:
                    if j.isalnum():
                        stop_word.add(j.lower())
    return stop_word
stop_word=stopword()


positive_words=set()
negative_words=set()
d=''
with open(r'D:\20211030 Test Assignment\MasterDictionary\negative-words.txt','r') as n:
    d=n.readlines(0)
    for i in d:
        i=i.strip('\n')
        negative_words.add(i)
    
   

with open(r'D:\20211030 Test Assignment\MasterDictionary\positive-words.txt','r') as n:
    d=n.readlines(0)
    for i in d:
        i=i.strip('\n')
        positive_words.add(i)



#creating dictionary and assined +1 for positive words and -1 for negative words
def positive_score_calculator(text):
    text=text.lower()#lowering
    words=nltk.tokenize.word_tokenize(text)#tokenization
    y=[]
    for word in words:
        if word.isalnum():#removing special characters
            y.append(word)
    text=y[:]
    y.clear()
    for word in text:#removing stowords and punctuation
        if word not in stop_word and word not in string.punctuation:
            y.append(word)
        
    clean_text= " ".join(y)


    positive_dictionary=dict()
    for i in clean_text.split():
        if i in positive_words:
            #print('positive_words')
            positive_dictionary[i]=+1
    return sum(positive_dictionary.values())
url_df['positive_score']=url_df['file_data'].apply(positive_score_calculator)

def negative_score_calculator(text):
    text=text.lower()#lowering
    words=nltk.tokenize.word_tokenize(text)#tokenization
    y=[]
    for word in words:
        if word.isalnum():#removing special characters
            y.append(word)
    text=y[:]
    y.clear()
    for word in text:#removing stowords and punctuation
        if word not in stop_word and word not in string.punctuation:
            y.append(word)
        
    clean_text= " ".join(y)

    negative_dictionary=dict()
    for i in clean_text.split():
        if i in negative_words:
            #print('negative_words')
            negative_dictionary[i]=-1
    return sum(negative_dictionary.values())*-1
url_df['negative_score']=url_df['file_data'].apply(negative_score_calculator)



#Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
def polarity_score(positive_score,negative_score):
    return (positive_score-negative_score)/((positive_score+negative_score)+0.000001)
url_df['polarity_score']=url_df.apply(lambda x: polarity_score(x['positive_score'], x['negative_score']), axis=1)


#Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
def transform_text(text):
    text=text.lower()#lowering
    words=nltk.tokenize.word_tokenize(text)#tokenization
    y=[]
    for word in words:
        if word.isalnum():#removing special characters
            y.append(word)
    text=y[:]
    y.clear()
    for word in text:#removing stowords and punctuation
        if word not in stop_word and word not in string.punctuation:
            y.append(word)
        
    return " ".join(y)

def subjectivity_score(positive_score,negative_score,text):
    length=len(transform_text(text).split())
    return (positive_score+negative_score)/((length)+0.000001)
url_df['subjectivity_score']=url_df.apply(lambda x: subjectivity_score(x['positive_score'], x['negative_score'], x['file_data']), axis=1)

#Avergae sentence length
def average_sentence_length(text):
    words=nltk.tokenize.word_tokenize(text)
    y=[]
    for word in words:
        if word.isalnum():#removing special characters
            y.append(word)
    number_of_words=len(y)
    number_of_sentences=len(nltk.tokenize.sent_tokenize(text))
    average_sentence_length=number_of_words/number_of_sentences
    return average_sentence_length
url_df['average_sentence_length']=url_df['file_data'].apply(average_sentence_length)


#Percentage of complex words
def percentage_of_complex_words(text):
    raw_words=nltk.tokenize.word_tokenize(text)
    clean_word=[]
    for word in raw_words:
        if word.isalnum():#removing special characters
            clean_word.append(word)
 
    # difficult words are those with syllables > 2
    # easy_word_set is provide by Textstat as
    # a list of common words
    diff_words_set = set()
     
    for word in clean_word:
        syllable_count = textstatistics().syllable_count(word)
        if word not in stop_word and syllable_count > 2:
            diff_words_set.add(word)
 
    return len(diff_words_set)/len(clean_word)
url_df['percentage_of_complex_words']=url_df["file_data"].apply(percentage_of_complex_words)


#Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
def fog_index(average_sentence_length,percentage_of_complex_words):
    return 0.4*(average_sentence_length+percentage_of_complex_words)
url_df['fog_index']=url_df.apply(lambda x : fog_index(x['average_sentence_length'], x['percentage_of_complex_words']), axis=1)


#average_number_of_word_per_sentence
def average_number_of_word_per_sentence(text):
    words=nltk.tokenize.word_tokenize(text)
    y=[]
    for word in words:
        if word.isalnum():#removing special characters
            y.append(word)
    number_of_words=len(y)
    number_of_sentences=len(nltk.tokenize.sent_tokenize(text))
    average_sentence_length=number_of_words/number_of_sentences
    return average_sentence_length
url_df['average_number_of_word_per_sentence']=url_df['file_data'].apply(average_number_of_word_per_sentence)


# Compelx word count
def complex_word_count(text):
    raw_words=nltk.tokenize.word_tokenize(text)
    clean_word=[]
    for word in raw_words:
        if word.isalnum():#removing special characters
            clean_word.append(word)
 
    # difficult words are those with syllables > 2
    diff_words_set = set()
    for word in clean_word:
        syllable_count = textstatistics().syllable_count(word)
        if word not in stop_word and syllable_count > 2:
            diff_words_set.add(word)
 
    return len(diff_words_set)
url_df['complex_word_count']=url_df["file_data"].apply(complex_word_count)


#Word Count
def word_count(text):
    raw_words=nltk.tokenize.word_tokenize(text)
    clean_word=[]
    for word in raw_words:
        if word.isalnum():#removing special characters
            clean_word.append(word)

    diff_words_set = list()
    for word in clean_word:
        if word not in stop_word :
            diff_words_set.append(word)
    
    return len(diff_words_set)

url_df['word_count']=url_df["file_data"].apply(word_count)


#Syllable Count
def syllable_count(text):
    raw_words=nltk.tokenize.word_tokenize(text)
    clean_word=[]
    for word in raw_words:
        if word.isalnum():#removing special characters
            clean_word.append(word)

    
    count = 0
    for word in clean_word:
        word = word.lower()
        vowels = "aeiou"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
                if word.endswith("es") or word.endswith("ed"):
                    count -= 1
        if count == 0:
            count += 1
    return count
url_df['syllable_count']=url_df["file_data"].apply(syllable_count)


#No of personal pronouc such as I,We,My,Ours,Us
def personal_pronoun(text):
    data=text.replace('\n','')
    data=data.replace('\xa0','')
    pronounRegex = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)
    pronouns = pronounRegex.findall(data)
    return len(pronouns)
url_df["personal_pronouns"]=url_df["file_data"].apply(personal_pronoun)

#Average Word Length
def average_word_length(text):
    raw_words=nltk.tokenize.word_tokenize(text)
    clean_word=''
    number_of_words=0
    for word in raw_words:
        if word.isalnum():#removing special characters
            clean_word+=word+' '
            number_of_words+=1
    return len(clean_word)/number_of_words

url_df["average_word_length"]=url_df["file_data"].apply(average_word_length)  




df=url_df[['URL_ID', 'URL', 'positive_score',
       'negative_score', 'polarity_score', 'subjectivity_score',
       'average_sentence_length', 'percentage_of_complex_words', 'fog_index',
       'average_number_of_word_per_sentence', 'complex_word_count',
       'word_count', 'syllable_count', 'personal_pronouns',
       'average_word_length']]



df.to_csv('output.csv', header=True, index=False)

print(url_df.columns)


print(url_df)
