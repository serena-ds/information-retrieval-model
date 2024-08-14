# Name: Le Thao Nhi Nguyen
# Student Number: N11527293
# Question 3 - Assignment 1 - IFN647

# Import necessary libraries
import os, glob, string, re, math
from stemming.porter2 import stem
from Q1 import parse_rcv1v2, parse_query
from Q2 import my_df

# Task 3.1 Question 3
# Function to calculate and return the average document length in the collection
def avg_length(coll):
    totalDocLength = 0
    
    # Calculate average document length by summing the document length of all Rcv1Doc objects and dividing by the total number of documents
    for rcv1_doc in coll.values():
        totalDocLength += rcv1_doc.getDocLen()
    avgDocLength = totalDocLength / len(coll)
    
    return avgDocLength

# Task 3.2 Question 3
# Function to calculate documents' BM25 score for a given original query
def my_bm25(coll, q, df):
    ri = 0 # Number of relevant documents containing term i, assume ri = 0
    R = 0 # Total number of relevant documents in the collection, assume R = 0
    N = len(coll) # Total number of rdocuments in the collection
    avdl = avg_length(coll) # The average length of the collection, using function from Task 3.1
    
    # Typical TREC value for k1, k2 and b, referenced from the lecture
    k1 = 1.2
    k2 = 100
    b = 0.75
    
    doc_bm25 = {} # Initialise an empty dictionary to store BM25 scores for each document
    
    # Calculate the BM-25 score based on the equation from the Question 3's requirements, using Document-at-a-time method
    for docID, rcv1_doc in coll.items():
        bm25_score = 0
        dl = rcv1_doc.getDocLen() # Doc Length
        K = k1*((1-b)+((b*dl)/avdl))
        
        for term, q_freq in parsed_query.items():
            ni = df[term] # Number of documents containing term i
            
            # Frequency weight of term i in the document
            if term in rcv1_doc.terms:
                fi = rcv1_doc.terms[term] 
            else:
                fi = 0
            
            # Frequency weight of term i in the query
            qfi = q_freq
        
            binary_scores = math.log2(((ri + 0.5)/ (R-ri+0.5))/((ni-ri+0.5)/(N-ni-R+ri+0.5)))
            bm25_score += binary_scores * (((k1+1)*fi)/(K+fi))*(((k2+1)*qfi)/(k2+qfi))
        
        # Store BM25 score for current document
        doc_bm25[docID] = bm25_score
        
    return doc_bm25

#Task 3.3 Question 3
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
    output_file = "LeThaoNhiNguyen_Q3.txt"
    with open(output_file, "w") as file:
        file.write(f"*******************************")
        file.write(f"\n*   Name: Le Thao Nhi Nguyen  *")
        file.write(f"\n*  Student Number: N11527293  *")
        file.write(f"\n*--- OUTPUT OF QUESTION 3 ----*")
        file.write(f"\n*******************************\n")
        
        # To output the results of 3 tasks, use parse_rcv1v2() from Question 1 and my_df() from Question 2 to parse the collection and calculate document frequecy for a collection
        Rcv1_Coll = parse_rcv1v2(sys.argv[1],stopwordList)
        terms_doc_freq = my_df(Rcv1_Coll)
        
        # Output for Task 3.1
        avg_len_coll = avg_length(Rcv1_Coll)
        file.write(f"\n1/ Output of function avg_length() defined from Task 3.1:\n")
        file.write(f"\nAverage document length for this collection is: {avg_len_coll}")
        file.write(f"\n")

        #Output for Task 3.2 and 3.3
        file.write(f"\n2/ Output of function my_bm25() defined from Task 3.2 to rank all documents in the collection and top-6 posible relevant documents for a given query:\n")
        
        # Queries to test the function
        queries = ["The British-Fashion Awards", "Rocket attacks", "Broadcast Fashion Awards", "stock market"]
        
        for query in queries:
            # Use parse_query() from Question 1 to parse the query for the input q of my_bm25() function
            parsed_query = parse_query(query, stopwordList)

            # Call the my_bm25 function() from Task 3.2
            bm25_scores = my_bm25(Rcv1_Coll, parsed_query, terms_doc_freq)
            
            # Task 3.2 - Output the BM25 scores for each document
            file.write(f"\nThe query is: {query}")
            file.write(f"\nThe following are the BM25 score for each document:")
            for docID, score in bm25_scores.items():
                file.write(f"\nDocument ID: {docID}, Doc Length: {Rcv1_Coll[docID].getDocLen()} -- BM25 Score: {score}")

            #Task 3.3 - Output the ranking score for top-6 possible relevant documents
            file.write(f"\n")
            sorted_bm25_scores = sorted(bm25_scores.items(), key=lambda item: item[1], reverse=True)
            file.write(f"\nFor query '{query}', the top-6 possible relevant documents are:")
            for docID, score in sorted_bm25_scores[:6]:
                file.write(f"\n{docID} {score}")
            file.write(f"\n")
    
    # After writing the output into a text file, change directory to print out the output in terminal
    os.chdir(curr_path)
    with open(output_file, "r") as file:
        output = file.read()
        print(output)