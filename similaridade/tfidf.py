from similaridade.vectorize import vectorize

class tfidf:
    def __init__(self, documents, stopwords):
        """ 
            documents = lista de textos
            stopwords = True or False
        """
        self.stopwords = stopwords
        self.documents = documents
        self.doc_map_idx = self.get_map_doc_idx()

        self.documents_dict = self.get_documents_dict()
        self.corpus = self.get_corpus()
        self.idf = self.get_idf()

    def get_map_doc_idx(self):
        """  
            [{1: txt1}, {2: txt2}, ...]
        """
        doc_dict = {}
        for doc in self.documents:
            doc_dict[doc.id] = doc.texto
        return doc_dict

    def get_documents_dict(self):
        return vectorize.get_all_dict([doc.texto for doc in self.documents], self.stopwords)         

    def get_corpus(self):
        corpus = list()
        if self.stopwords is True:            
            for doc in self.documents:
                t_doc = vectorize.remove_stop_words(doc.texto, 'english')
                bag_words = vectorize.get_bag_words(t_doc, self.documents_dict)
                corpus.append(bag_words)
        else:
            for doc in self.documents:
                t_doc = doc.texto.split(' ')
                bag_words = vectorize.get_bag_words(t_doc, self.documents_dict)
                corpus.append(bag_words)
        return corpus
    
    def get_idf(self):
        return vectorize.idf(self.corpus)

    def get_all_tf_idf(self):
        tf_idf_documents = {}

        if self.stopwords is True:
            for idx, doc in self.doc_map_idx.items():
                t_doc = vectorize.remove_stop_words(doc, 'english')
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
            
