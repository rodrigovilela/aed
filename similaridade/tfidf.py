from similaridade.vectorize import vectorize
import _pickle as pickle

class data_persistence:

    @staticmethod
    def write(data, path):
        with open(path, 'wb') as file:
            file.write(pickle.dumps(data))

    @staticmethod
    def load(path):
        with open(path, 'rb') as file:
            return pickle.load(file)


class tfidfall:
    def __init__(self, tfidf_list, stopwords):
        self.stopwords = stopwords
        self.tfidf_list = tfidf_list

        self.docs_dict = self.get_documents_dict()
        self.corpus = self.get_corpus()
        self.idf = self.get_idf()

    def get_documents_dict(self):
        dict_docs = list()
        for elem in self.tfidf_list:            
            dict_docs += vectorize.get_dict(vectorize.get_all_dict(elem.documents, self.stopwords), dict_docs)
        return dict_docs
    
    def get_corpus(self):
        corpus = list()
        if self.stopwords is True:            
            for elem in self.tfidf_list:
                t_doc = list()
                for doc in elem.documents:
                    t_doc = t_doc + vectorize.remove_stop_words(doc, 'portuguese')
                bag_words = vectorize.get_bag_words(t_doc, self.docs_dict)
                corpus.append(bag_words)
        else:
            for elem in self.tfidf_list:
                t_doc = list()
                for doc in elem.documents:
                    t_doc = t_doc + [word for word in doc.split() if len(word) > 3]
                bag_words = vectorize.get_bag_words(t_doc, self.docs_dict)
                corpus.append(bag_words)
        return corpus 
    
    def get_idf(self):
        return vectorize.idf(self.corpus)

    def get_tf_idf(self, elem):
        """ 
            elem = tfidf com trechos
        """
        tf_idf_documents = {}

        if self.stopwords is True:
            for idx, doc in elem.doc_map_idx.items():
                t_doc = vectorize.remove_stop_words(doc, 'portuguese')
                bag_words = vectorize.get_bag_words(t_doc, self.docs_dict)
                tf_doc = vectorize.tf(bag_words, elem.documents_dict)

                tamanho_trecho = len(t_doc)
                tf_idf_documents[idx] = (vectorize.tf_idf(tf_doc, self.idf), tamanho_trecho)
        else:
            for idx, doc in elem.doc_map_idx.items():
                t_doc = [word for word in doc.split(' ') if len(word) > 3]
                bag_words = vectorize.get_bag_words(t_doc, self.docs_dict)
                tf_doc = vectorize.tf(bag_words, elem.documents_dict)

                tamanho_trecho = len(t_doc)
                tf_idf_documents[idx] = (vectorize.tf_idf(tf_doc, self.idf), tamanho_trecho)
        return tf_idf_documents

class tfidf:
    def __init__(self, documents, stopwords, trecho, id_noticia):
        """ 
            documents = lista de textos
            stopwords = True or False
        """
        self.id_noticia = id_noticia
        self.trecho = trecho
        self.stopwords = stopwords        

        if trecho is False:
            self.documents = documents
            self.doc_map_idx = self.get_map_doc_idx()
            self.documents_dict = self.get_documents_dict()
            self.corpus = self.get_corpus()
            self.idf = self.get_idf()
        else:
            self.documents = [trecho.valor for trecho in documents]
            self.doc_map_idx = self.get_map_doc_idx()
            self.documents_dict = self.get_documents_dict()

    def get_map_doc_idx(self):
        """
            [{1: txt1}, {2: txt2}, ...]
        """
        doc_dict = {}
        if self.trecho is False:
            for doc in self.documents:
                doc_dict[doc.id] = doc.texto
        else:
            for idx, trecho in enumerate(self.documents):
                doc_dict[idx] = trecho
        return doc_dict
    
    def get_documents_dict(self):
        if self.trecho is False:
            return vectorize.get_all_dict([doc.texto for doc in self.documents], self.stopwords)
        else:
            return vectorize.get_all_dict(self.documents, self.stopwords)

    def get_corpus(self):
        corpus = list()
        if self.stopwords is True:            
            for doc in self.documents:
                if self.trecho is False:
                    t_doc = vectorize.remove_stop_words(doc.texto, 'portuguese')
                else:
                    t_doc = vectorize.remove_stop_words(doc, 'portuguese')
                bag_words = vectorize.get_bag_words(t_doc, self.documents_dict)
                corpus.append(bag_words)
        else:
            for doc in self.documents:
                if self.trecho is False:
                    t_doc = doc.texto.split(' ')
                else:
                    t_doc = doc.split(' ')
                bag_words = vectorize.get_bag_words(t_doc, self.documents_dict)
                corpus.append(bag_words)
        return corpus
    
    def get_idf(self):
        return vectorize.idf(self.corpus)

    def get_all_tf_idf(self):
        tf_idf_documents = {}

        if self.stopwords is True:
            for idx, doc in self.doc_map_idx.items():
                t_doc = vectorize.remove_stop_words(doc, 'portuguese')
                bag_words = vectorize.get_bag_words(t_doc, self.documents_dict)
                tf_doc = vectorize.tf(bag_words, vectorize.get_dict_doc(t_doc))
                tf_idf_documents[idx] = vectorize.tf_idf(tf_doc, self.idf)
        else:
            for idx, doc in self.doc_map_idx.items():
                t_doc = doc.split(' ')
                bag_words = vectorize.get_bag_words(t_doc, self.documents_dict)
                tf_doc = vectorize.tf(bag_words, vectorize.get_dict_doc(t_doc))
                tf_idf_documents[idx] = vectorize.tf_idf(tf_doc, self.idf)
        return tf_idf_documents
            
