from gensim.test.utils import datapath, get_tmpfile
import gensim.corpora

import dados

path_to_wiki_dump = datapath("enwiki-latest-pages-articles1.xml-p000000010p000030302-shortened.bz2")
corpus_path = get_tmpfile("wiki_corpus.mm")

wiki = gensim.corpora.WikiCorpus(path_to_wiki_dump)
wiki.metadata = True

# _docs = [(arg2[1], " ".join(arg1)) for arg1, arg2 in wiki.get_texts()]
_docs = [(arg2, arg1) for arg1, arg2 in wiki.get_texts()]
print(_docs[0])
# dados.db.query_insert(_docs, "wikipedia")

#gensim.corpora.MmCorpus.serialize(corpus_path, wiki, progress_cnt=1000, metadata=True)

# mm_corpus = gensim.corpora.MmCorpus(datapath(corpus_path))
# for doc in mm_corpus:
# 	print(doc)
# 	break


#filter_func = gensim.corpora.wikicorpus.filter_example
#dewiki = gensim.corpora.WikiCorpus(path_to_wiki_dump, filter_articles=filter_func)
#dewiki.metadata = True




