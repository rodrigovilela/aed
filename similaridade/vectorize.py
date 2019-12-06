import numpy as np
import math

from nltk.corpus import stopwords

# nltk.download('stopwords')

class vectorize():

    @staticmethod
    def remove_stop_words(document, language):
        if isinstance(document, str):
            t_doc = document.split(' ')
        else:
            t_doc = document
        t_doc = [word for word in t_doc if len(word) > 3]
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
                t_doc = vectorize.remove_stop_words(doc, 'portuguese')
                doc_dict = vectorize.get_dict(t_doc, doc_dict)
        else:
            for doc in documents:
                t_doc = [word for word in doc.split(' ') if len(word) > 3]
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
        _tokens = [word for word in tokens if len(word) > 3]        
        for token in _tokens:            
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
            if count > 0:
                tf[token] = count / float(len_doc)
            else:
                tf[token] = 0
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
            if count > 0:
                idf_dict[word] = math.log(n_docs / float(count))
            else:
                idf_dict[word] = 0

        return idf_dict

    @staticmethod
    def tf_idf(tf_document, idf_corpus):
        tfidf_dict = {}
        for word, tf in tf_document.items():
            tfidf_dict[word] = tf * idf_corpus[word]
        return tfidf_dict

