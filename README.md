# Document & Query Parsing and IR Models
## Overview
This repository contains Python implementations for parsing documents and queries, as well as building TF-IDF and BM25-based Information Retrieval (IR) models. The project involves processing text data from the RCV1v2 dataset.

The repository includes three Python files corresponding to the three tasks in the assignment.

## Usage
### Step 1: Run the Python Scripts
- Open Terminal in PyCharm, Command Prompt on Windows, or Terminal on macOS.
### Step 2: Navigate to the Project Directory (if not using PyCharm)
- Change the directory to the folder containing the .py files.
- Command: cd "<folder path>" (include the path inside double quotes).
- *Example*: macOS: cd "/Users/YourName/ProjectFolder" | Windows: cd "\Users\YourName\ProjectFolder"
### Step 3: Execute the Python Script
- Run the script using python <script.py> "<folder path/data>" or py <script.py> data.
- *Example*: python Q1.py "/Users/YourName/ProjectFolder/data" | py Q1.py data

## Tasks
### Task 1: Document & Query Parsing
- Document Parsing: Parses XML files to extract and preprocess document data.
- Query Parsing: Processes queries using the same preprocessing steps as documents.
### Task 2: TF-IDF Model
- TF-IDF Calculation: Computes TF-IDF scores for terms in documents and ranks them based on relevance to queries.
### Task 3: BM25 Model
- BM25 Calculation: Implements the BM25 ranking algorithm to score and rank documents based on queries.

## Outputs
Results are saved in text files named according to the task.

## License
This project is for educational purposes.

