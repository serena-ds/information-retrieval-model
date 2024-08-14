# Name: Le Thao Nhi Nguyen
# Student Number: N11527293
# Question 1 - Assignment 1 - IFN647

# Import necessary libraries
import os, glob, string, re
from stemming.porter2 import stem

# Task 1.1 Question 1
# Define a class to represent a document
class Rcv1Doc:
    def __init__(self, docID, terms, doc_len):
        self.docID = docID
        self.terms = terms
        self.doc_len = doc_len
    
    # Method to add new term or increase term frequency when the term occurs again
    def add_term(self, term):
        try:
            self.terms[term] += 1
        except KeyError: 
            self.terms[term] = 1
    
    # Method to get the document length
    def getDocLen(self): #for task 3
        return self.doc_len
    
    # Method to set the document length
    def setDocLen(self, doc_len):#for task 3
        self.doc_len = doc_len
    
    # Method to get a sorted list in descending order of all terms occurring in the document
    def get_term_list(self):
        sorted_terms = sorted(self.terms.items(), key=lambda x: x[1], reverse=True)
        return sorted_terms

# Function to parse a collection and return the result as a dictionary structure for storing a collection of Rcv1Doc objects
def parse_rcv1v2(inputpath, stop_words):
    collection = {} # Initialise an empty dictionary to store the collection of Rcv1Doc objects
    os.chdir(inputpath) # Change the current working directory to the input dataset
    xml_files = glob.glob(os.path.join(inputpath, '*.xml')) # Get a list of XML files from the input path
    
    # Iterate over each XML file in the list
    for xml_file in xml_files:
        doc_len = 0  # Initialise the document length
        terms = {}   # Initialise an empty dictionary to store the terms and their frequencies
        
        with open(xml_file) as seq:   
            file = seq.readlines()
            start_end = False # Initialise a flag to track where we are in the document
            
            for line in file:
                line = line.strip() # Remove leading and trailing whitespace
                if(start_end == False): 
                    # Extract Document ID
                    if line.startswith("<newsitem "):
                        for part in line.split():
                            if part.startswith("itemid="):
                                docID = part.split("=")[1].split("\"")[1]
                                rcv1_doc = Rcv1Doc(docID, terms, doc_len) #Create a new Rcv1Doc object
                                break  
                    # Set the flag to 'True' if we are inside the <text> tag
                    if line.startswith("<text>"):
                        start_end = True 
                # Exit the for loop if we meet the closing </text> tag
                elif line.startswith("</text>"):
                    break
                else:
                    # Tokenize the '<text> ... </text>' part of the document, exclude all tags, discard punctuations and numbers, and standardise the white space
                    line = line.replace("<p>", "").replace("</p>", "")
                    line = line.translate(str.maketrans('', '', string.digits)).translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
                    line = re.sub("\s+", " ", line)
                    
                    for term in line.split():
                        rcv1_doc.doc_len += 1  # Calculate document length
                        term = stem(term.lower())  # Stem the term and convert it to lowercase
                        # If the term has more than two characters and not in the given stopping words list, add new term or increase term frequency when the term occurs again
                        if (len(term) > 2) and (term not in stop_words):
                            rcv1_doc.add_term(term)
                            
        # Set the document length to the Rcv1Doc object
        rcv1_doc.setDocLen(rcv1_doc.doc_len)    
        
        # Store the Rcv1Doc object in the collection with document ID as the key
        collection[docID] = rcv1_doc 
    return collection

#Task 1.2 Question 1
# Function to parse a query
def parse_query(query0, stop_words):
    dict_query = {} # Initialise an empty dictionary to store the terms of query and their frequencies
    
    # Use the identical steps for parsing document to parse the query
    words = query0.replace("<p>", "").replace("</p>", "")
    words = words.strip().translate(str.maketrans('', '', string.digits)).translate(
                            str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    words = re.sub("\s+", " ", words).split()
    
    for term in words:
        term = stem(term.lower())
        if len(term) > 2 and term not in stop_words:
            try:
                dict_query[term] += 1
            except KeyError:
                dict_query[term] = 1
    return dict_query

#Task 1.3 Question 1
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
    output_file = "LeThaoNhiNguyen_Q1.txt"
    with open(output_file, "w") as file:
        file.write(f"*******************************")
        file.write(f"\n*   Name: Le Thao Nhi Nguyen  *")
        file.write(f"\n*  Student Number: N11527293  *")
        file.write(f"\n*--- OUTPUT OF QUESTION 1 ----*")
        file.write(f"\n*******************************\n")
        
        # Call function parse_rcv1v2() from Task 1.1 to parse the document
        file.write(f"\n1/ Output of function parse_rcv1v2() defined from Task 1.1\n")
        
        # Output for Task 1.1
        Rcv1_Coll = parse_rcv1v2(sys.argv[1],stopwordList)
        for docID, rcv1_doc in Rcv1_Coll.items():
            file.write(f"\nOutput Example for file {docID}news.xml")
            file.write(f"\nDocument {docID} contains {len(rcv1_doc.terms)} terms and has total {rcv1_doc.doc_len} words")
            
            # Output a sorted term:freq list
            for term, freq in rcv1_doc.get_term_list():
                file.write(f"\n{term}: {freq}")
            file.write(f"\n")
        
        # Call function parse_query() from Task 1.2 to parse a query
        file.write(f"\n2/ Output of function parse_query() defined from Task 1.2\n")
        
        # Example of a query to test the function
        query = 'CANADA: Sherritt to buy Dynatec, spin off unit, canada.'
        
        # Output for Task 1.2
        file.write(f"\nQuery: {query}")
        file.write(f"\nThe parsed query:")
        query_terms = parse_query(query, stop_words)
        file.write(f"\n{query_terms}")
    
    # After writing the output into a text file, change directory to print out the output in terminal
    os.chdir(curr_path)
    with open(output_file, "r") as file:
        output = file.read()
        print(output)
