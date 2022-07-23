import pandas as pd
import numpy as np
import networkx as nx
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from flask import Flask, redirect, url_for, render_template, request

app=Flask(__name__)

@app.route("/home")
def home():
     return render_template("home.html")

def read_article(fname):
    file=open(fname,"r",encoding="utf-8")
    filedata=file.readlines()
    filedata=[x for x in filedata if x !='\n']
    filedata=[x.replace('\n',' ') for x in filedata]
    para=[]
    for para in filedata:
        article=para.split(".")
        sentences=[]
        for sentence in article:
            print(sentence)
            sentences.append(sentence.replace("[a-ZA-Z]"," ").split(" "))
        sentences.pop()
        return sentences

def build_similarity_matrix(sentences, stop_words):
    similarity_matrix=np.zeros((len(sentences),len(sentences)))
    
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1==idx2:
                 continue
            similarity_matrix[idx1][idx2]=sentence_similarity(sentences[idx1],sentences[idx2],stop_words)
            
    return similarity_matrix

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords=[]
        
    sent1=[w.lower() for w in sent1]
    sent2=[w.lower() for w in sent2]
    
    all_words=list(set(sent1+sent2))
    
    vector1=[0]*len(all_words)
    vector2=[0]*len(all_words)
    
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)]+=1
        
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)]+=1
        
    return 1-cosine_distance(vector1, vector2)

def generate_summary(file_name,top_n=30):
    stop_words=stopwords.words('english')
    summarize_text=[]
    
    sentences=read_article(file_name)
    
    sentence_similarity_matrix=build_similarity_matrix(sentences, stop_words)
    
    sentence_similarity_graph=nx.from_numpy_array(sentence_similarity_matrix)
    scores=nx.pagerank(sentence_similarity_graph)
    
    ranked_sentences=sorted(((scores[i],s) for i,s in enumerate(sentences)),reverse=True)
    print("Indices of top ranked sentences are",ranked_sentences)
    
    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentences[i][1]))
        
    print("Summarized Text :\n", ". ".join(summarize_text))

    return summarize_text


t2=[]

@app.route("/",methods=["POST"])
def file():
    if request.method=="POST":                                                   
        t1=request.form["text"]

        file_writing=open("FIRST.txt","w+")
        file_writing.writelines(t1)
        file_writing.close()
        summary=generate_summary("FIRST.txt",8)
    return render_template("result.html",summary=summary)

if __name__=="__main__":
     app.run(debug=True)