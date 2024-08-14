# Name: Le Thao Nhi Nguyen
# Student Number: N11527293
# Question 2 - Assignment 1 - IFN647

# Import necessary libraries
import os, glob, string, re, math
from stemming.porter2 import stem
from Q1 import parse_rcv1v2, parse_query

# Task 2.1 Question 2
# Function to calculate df of the collection and return a {term:df,...} dictionary
def my_df(coll):
    term_df = {}  # Initialise an empty dictionary to store document frequency for each term
    
    # Iterate over each document in the collection to update document frequency for each term
    for docID, rcv1_doc in coll.items():
        for term in rcv1_doc.terms.keys():
            if term in term_df:
                term_df[term] += 1
            else:
                term_df[term] = 1
                
    return term_df

# Task 2.2 Question 2
# Function to calculate TF*IDF value (weight) of every term in a Rcv1Doc object
def my_tfidf(doc, df, ndocs):
    term_weight = {} # Initialise an empty dictionary to store the weight for each term
    sqrt_sum = 0
    
    # Check if the input 'doc' is a Rcv1Doc object or a dictionary of {term:freq,...}
    if type(doc) != dict:
        terms = doc.get_term_list()
    
    # Calculate the TF*IDF value and store in the 'term_weight' dictionary
    for term, freq in terms:
        sqrt_sum += pow(((math.log(freq)+1)*math.log(ndocs/df[term])),2)
    for term, freq in terms:
        tfidf = ((math.log(freq)+1)*(math.log(ndocs/df[term])))/(math.sqrt(sqrt_sum))
        term_weight[term] = tfidf
    
    return term_weight

#Task 2.3 Question 2
if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()
    
    # Store the directory containing .py file before executing the file
    curr_path = os.getcwd()
    
    # Open and read the given stop word file and store them in the stopwordList
    with open('common-english-words.txt', 'r') as stopwords_f:
        stop_words = stopwords_f.read()
        stopwordList = stop_words.split(',')

    # Create a text file to open and write the output in it
    output_file = "LeThaoNhiNguyen_Q2.txt"
    with open(output_file, "w") as file:
        file.write(f"*******************************")
        file.write(f"\n*   Name: Le Thao Nhi Nguyen  *")
        file.write(f"\n*  Student Number: N11527293  *")
        file.write(f"\n*--- OUTPUT OF QUESTION 2 ----*")
        file.write(f"\n*******************************\n")
        
        # Parse the collection using function parse_rcv1v2() from Question 1
        Rcv1_Coll = parse_rcv1v2(sys.argv[1],stopwordList)
        
        # Call function my_df() from Task 2.1 to calculate document frequecy for a collection
        terms_doc_freq = my_df(Rcv1_Coll)
        # Sorted in descending order
        sorted_freq = {k: v for k, v in sorted(terms_doc_freq.items(), key=lambda item: item[1], reverse = True)}
        
        # Output for Task 2.1
        file.write(f"\n1/ Output of function my_df() defined from Task 2.1:\n")
        file.write(f"\nThere are {len(Rcv1_Coll)} documents in this dataset and contains {len(terms_doc_freq)} terms.")
        file.write(f"\nThe following are the terms’ document-frequency:")
        for term, df in sorted_freq.items():
            file.write(f"\n{term}: {df}")
                
        #Output for Task 2.2
        file.write(f"\n")
        file.write(f"\n2/ Output of function my_tfidf() defined from Task 2.2:\n")
        for docID, doc in Rcv1_Coll.items():
            file.write(f"\nDocument {docID} contains {len(doc.terms)} terms")   
            
            # Call function my_tfidf and print out top 20 terms for each document if it has more than 20 terms, or print out all terms if it has less than 20 terms
            tfidf_weight = my_tfidf(doc, terms_doc_freq, len(Rcv1_Coll))
            sorted_weight = sorted(tfidf_weight.items(), key=lambda x: x[1], reverse=True)
            if len(sorted_weight) > 20:
                for term, weight in sorted_weight[:20]:
                    file.write(f"\n{term}: {weight}")
            else:
                for term, weight in sorted_weight:
                    file.write(f"\n{term}: {weight}") 
            file.write(f"\n")
        
        #Titles of three XML documents from the dataset to test
        queries = ["Reuters French Advertising & Media Digest", "ISRAEL: 15 Palestinians, two Israelis killed in clashes.", "BELGIUM: MOTOR RACING-LEHTO AND SOPER HOLD ON FOR GT VICTORY.", "ISRAEL: Death toll 33 Arabs, 10 Israelis at 1400 gmt."]
        
        # Output for Task 2.3
        file.write(f"\n3/ Output of the ranking score of the query for each document in descending order:\n")
        for query in queries:
            # Parse the query (title) using parse_query() function from Question 1
            parsed_query = parse_query(query, stopwordList) 
            ranking_scores = {}  # Initialise an empty dictionary to store the ranking scores for documents 
            
            # Calculate ranking scores by multiplying document term weights with query term weights and then summing them
            for docID, doc in Rcv1_Coll.items():
                R = 0 # Initialise the ranking score for the current document
                tfidf_weights = my_tfidf(doc, terms_doc_freq, len(Rcv1_Coll))
                for term_query, freq in parsed_query.items():
                    if term_query in tfidf_weights:
                        R += freq * tfidf_weights[term_query]
                ranking_scores[docID] = R
                
                # Sorted the ranking score in a descending order
                sorted_scores = {k: v for k, v in sorted(ranking_scores.items(), key=lambda item: item[1], reverse = True)}
            
            file.write(f"\nThe Ranking Result for query: '{query}'")
            for docID, score in sorted_scores.items():
                file.write(f"\n{docID}: {score}")
            file.write(f"\n")
    
    # After writing the output into a text file, change directory to print out the output in terminal
    os.chdir(curr_path)
    with open(output_file, "r") as file:
        output = file.read()
        print(output)
