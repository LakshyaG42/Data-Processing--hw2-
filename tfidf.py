import re
import math
from collections import defaultdict
from collections import Counter

def preprocess_document(text):
    
    text = re.sub(r'[^\w\s]', '', text) #removing non-word characters
    text = re.sub(r'\s+', ' ', text) #removing extra whitespaces
    text = re.sub(r'\bhttps?\S+\b', '', text)# removing website links
    text = text.lower() # Convert all words to lowercase

    return text

def remove_stopwords(text, stopwords_set):
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords_set]
    return ' '.join(filtered_words)

def stem_and_lemmatize(text):
    rules = ['ing', 'ly', 'ment']
    for rule in rules:
        text = re.sub(r'{}\b'.format(rule), '', text)
    return text


#PART 2 

def compute_tf(text):
    words = text.split()
    word_count = Counter(words)
    total_words = len(words)
    tf_scores = {word: count / total_words for word, count in word_count.items()}
    return tf_scores

def compute_idf(documents):
    wordOccurance = defaultdict(int)
    total_documents = len(documents)
    for doc in documents:
        words_set = set(doc.split())
        for word in words_set:
            wordOccurance[word] += 1
    
    return {word: math.log(total_documents / presence) + 1 for word, presence in wordOccurance.items()}

def compute_tfidf(tf, idf):
    return {word: round(tf[word] * idf[word], 2) for word in tf}

def preprocess(doc, stopwords_set):
    doc = preprocess_document(doc)
    doc = remove_stopwords(doc, stopwords_set)
    doc = stem_and_lemmatize(doc)
    return doc

def main():
    with open('tfidf_docs.txt', 'r') as docs_file:
        documents = []
        filenames = []
        for line in docs_file:
            filename = line.strip()
            with open(filename, 'r') as doc_file:
                documents.append(doc_file.read())
                filenames.append(filename)
    print(filenames)
    with open('stopwords.txt', 'r') as stopwords_file:
        stopwords_set = set()
        for line in stopwords_file:
            word = line.strip()
            stopwords_set.add(word)
    
    preprocessed_docs = [preprocess(doc, stopwords_set) for doc in documents]
    idf_scores = compute_idf(preprocessed_docs)
    for doc, filename in zip(documents, filenames):
        preprocessed_doc = preprocess(doc, stopwords_set)
        with open(f'preproc_{filename}', 'w') as output_file:
            output_file.write(preprocessed_doc)
        tf_scores = compute_tf(preprocessed_doc)
        tfidf_scores = compute_tfidf(tf_scores, idf_scores)
        top_words = sorted(tfidf_scores.items(), key=lambda x: (-x[1], x[0]))[:5]
        
        with open(f'tfidf_{filename}', 'w') as output_file:
            output_file.write(str(top_words))




if __name__ == "__main__":
    main()
