import nltk
import numpy as np
import math

from nltk.corpus import stopwords

nltk.download('stopwords')

class vectorize():

    @staticmethod
    def remove_stop_words(document, language):
        if isinstance(document, str):
            t_doc = document.split(' ')

        return list(set(t_doc) - set(stopwords.words(language)))

    @staticmethod
    def get_dict(t_a, t_b):
        """ 
            Retorna conjunto de palavras unicas
        """
        return list(set(t_a).union(set(t_b)))

    @staticmethod
    def get_dict_doc(t_doc):        
        return list(set(t_doc))

    @staticmethod
    def get_all_dict(documents, stopwords):
        """ 
            documents = [doc1, doc2, ...]
        """
        doc_dict = []
        if stopwords is True:
            for doc in documents:
                t_doc = vectorize.remove_stop_words(doc, 'english')
                doc_dict = vectorize.get_dict(t_doc, doc_dict)
        else:
            for doc in documents:
                t_doc = doc.split(' ')
                doc_dict = vectorize.get_dict(t_doc, doc_dict)
        
        return doc_dict

    @staticmethod
    def get_bag_words(tokens, doc_dict):
        """ 
            tokens = conjunto de palavras do documento
            doc_dict = dicionario, conjunto com palavras unicas

            Frequencia de cada palavra por documento
        """
        bag_words = dict.fromkeys(doc_dict, 0)
        for token in tokens:
            bag_words[token] += 1
        return bag_words

    @staticmethod
    def tf(bag_words, doc_dict):
        """ 
            bag_words = frequencia que cada palavra ocorre no documento
            doc_dict = conjunto de palavras unicas do documento = tokens

            Porcentagem de cada palavra por documento
        """
        tf = {}
        len_doc = len(doc_dict)

        for token, count in bag_words.items():
            tf[token] = count / float(len_doc)
        return tf

    @staticmethod
    def idf(corpus):
        """ 
            corpus = [[bag_words_a], [bag_words_b], ...]
        """
        n_docs = len(corpus)
        idf_dict = dict.fromkeys(corpus[0].keys(), 0)

        for bag_word in corpus:
            for word, count in bag_word.items():
                if count > 0:
                    idf_dict[word] += 1

        for word, count in idf_dict.items():
            idf_dict[word] = math.log(n_docs / float(count))

        return idf_dict

    @staticmethod
    def tf_idf(tf_document, idf_corpus):
        tfidf_dict = {}
        for word, tf in tf_document.items():
            tfidf_dict[word] = tf * idf_corpus[word]
        return tfidf_dict

