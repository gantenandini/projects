# # # # import os
# # # # import PyPDF2
# # # # import pymongo
# # # # import logging
# # # # from concurrent.futures import ProcessPoolExecutor

# # # # # MongoDB Configuration
# # # # client = pymongo.MongoClient('mongodb://localhost:27017/')
# # # # db = client['pdf_db']
# # # # collection = db['pdf_metadata']

# # # # # Configure logging
# # # # logging.basicConfig(level=logging.INFO)

# # # # # Function to process a single PDF
# # # # def process_pdf(pdf_path):
# # # #     try:
# # # #         with open(pdf_path, 'rb') as file:
# # # #             reader = PyPDF2.PdfReader(file)
# # # #             num_pages = len(reader.pages)

# # # #             # Prepare metadata for MongoDB
# # # #             metadata = {
# # # #                 'name': os.path.basename(pdf_path),
# # # #                 'path': pdf_path,
# # # #                 'size': os.path.getsize(pdf_path),
# # # #                 'num_pages': num_pages,
# # # #             }

# # # #             # Check if the document already exists in the collection
# # # #             existing_doc = collection.find_one({'name': metadata['name']})
# # # #             if existing_doc:
# # # #                 logging.info(f"{metadata['name']} already exists in the database.")
# # # #             else:
# # # #                 # Insert new document into MongoDB
# # # #                 doc_id = collection.insert_one(metadata).inserted_id
# # # #                 logging.info(f"Processed {pdf_path} and stored metadata with ID: {doc_id}")

# # # #     except Exception as e:
# # # #         logging.error(f"Error processing {pdf_path}: {str(e)}")

# # # # # Function to process all PDFs in a folder
# # # # def process_folder(folder_path):
# # # #     pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
# # # #     # Process PDFs concurrently
# # # #     with ProcessPoolExecutor() as executor:
# # # #         executor.map(process_pdf, pdf_files)

# # # # if __name__ == "__main__":
# # # #     folder_path = r"C:\Users\Shivani\OneDrive\Desktop\pdf"  # Replace with your PDF folder path
# # # #     process_folder(folder_path)

# # # import os
# # # import PyPDF2
# # # import pymongo
# # # import logging
# # # from concurrent.futures import ProcessPoolExecutor
# # # import spacy

# # # # Load spaCy model for keyword extraction
# # # nlp = spacy.load("en_core_web_sm")

# # # # MongoDB Configuration
# # # client = pymongo.MongoClient('mongodb://localhost:27017/')
# # # db = client['pdf_db']
# # # collection = db['pdf_metadata']

# # # # Configure logging
# # # logging.basicConfig(level=logging.INFO)

# # # # Function to summarize text (simple approach)
# # # def generate_summary(text, max_length=150):
# # #     sentences = text.split('. ')
# # #     if len(sentences) <= 3:
# # #         return text  # Return the whole text if it's short
# # #     return '. '.join(sentences[:3]) + '.'  # Return first three sentences as summary

# # # # Function to extract keywords
# # # def extract_keywords(text, num_keywords=5):
# # #     doc = nlp(text)
# # #     keywords = {token.text for token in doc if token.is_alpha and not token.is_stop}
# # #     return list(keywords)[:num_keywords]

# # # # Function to process a single PDF
# # # def process_pdf(pdf_path):
# # #     try:
# # #         with open(pdf_path, 'rb') as file:
# # #             reader = PyPDF2.PdfReader(file)
# # #             num_pages = len(reader.pages)
# # #             text = ""

# # #             # Extract text from all pages
# # #             for page in reader.pages:
# # #                 text += page.extract_text() + " "

# # #             # Generate summary and extract keywords
# # #             summary = generate_summary(text)
# # #             keywords = extract_keywords(text, num_keywords=5)

# # #             # Prepare metadata for MongoDB
# # #             metadata = {
# # #                 'name': os.path.basename(pdf_path),
# # #                 'path': pdf_path,
# # #                 'size': os.path.getsize(pdf_path),
# # #                 'num_pages': num_pages,
# # #                 'summary': summary,
# # #                 'keywords': keywords
# # #             }

# # #             # Check if the document already exists in the collection
# # #             existing_doc = collection.find_one({'name': metadata['name']})
# # #             if existing_doc:
# # #                 logging.info(f"{metadata['name']} already exists in the database.")
# # #                 # Update the existing document with new summary and keywords
# # #                 collection.update_one({'_id': existing_doc['_id']}, {"$set": {'summary': summary, 'keywords': keywords}})
# # #                 logging.info(f"Updated {metadata['name']} with new summary and keywords.")
# # #             else:
# # #                 # Insert new document into MongoDB
# # #                 doc_id = collection.insert_one(metadata).inserted_id
# # #                 logging.info(f"Processed {pdf_path} and stored metadata with ID: {doc_id}")

# # #     except Exception as e:
# # #         logging.error(f"Error processing {pdf_path}: {str(e)}")

# # # # Function to process all PDFs in a folder
# # # def process_folder(folder_path):
# # #     pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
# # #     # Process PDFs concurrently
# # #     with ProcessPoolExecutor() as executor:
# # #         executor.map(process_pdf, pdf_files)

# # # if __name__ == "__main__":
# # #     folder_path = r"C:\Users\Shivani\OneDrive\Desktop\pdf"  # Replace with your PDF folder path
# # #     process_folder(folder_path)

# # import os
# # import PyPDF2
# # import pymongo
# # import logging
# # from concurrent.futures import ProcessPoolExecutor
# # import spacy
# # from collections import Counter

# # # Load spaCy model for custom tokenization (no pre-built pipeline)
# # nlp = spacy.load("en_core_web_sm")

# # # MongoDB Configuration
# # client = pymongo.MongoClient('mongodb://localhost:27017/')
# # db = client['pdf_db']
# # collection = db['pdf_metadata']

# # # Configure logging
# # logging.basicConfig(level=logging.INFO)

# # # Function to summarize text based on length (simple approach)
# # def generate_summary(text, max_sentences=5):
# #     sentences = text.split('. ')
# #     if len(sentences) <= max_sentences:
# #         return text  # Short text, return as-is
# #     return '. '.join(sentences[:max_sentences]) + '.'  # Limit to the first few sentences

# # # Function to extract keywords from text
# # def extract_keywords(text, num_keywords=10):
# #     doc = nlp(text)
# #     keywords = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
# #     keyword_freq = Counter(keywords)
# #     return [keyword for keyword, freq in keyword_freq.most_common(num_keywords)]

# # # Function to process a single PDF
# # def process_pdf(pdf_path):
# #     try:
# #         with open(pdf_path, 'rb') as file:
# #             reader = PyPDF2.PdfReader(file)
# #             num_pages = len(reader.pages)
# #             text = ""
# #             chunk_size = 10  # Process 10 pages at a time for larger PDFs
# #             summaries = []
# #             keywords = Counter()

# #             # Process PDF in chunks based on size
# #             for i in range(0, num_pages, chunk_size):
# #                 chunk_text = ""
# #                 for page_num in range(i, min(i + chunk_size, num_pages)):
# #                     chunk_text += reader.pages[page_num].extract_text() + " "
                
# #                 # Summarize chunk and extract keywords
# #                 chunk_summary = generate_summary(chunk_text)
# #                 chunk_keywords = extract_keywords(chunk_text)
                
# #                 summaries.append(chunk_summary)
# #                 keywords.update(chunk_keywords)
            
# #             # Combine summaries and top keywords
# #             final_summary = " ".join(summaries)
# #             final_keywords = [keyword for keyword, _ in keywords.most_common(10)]

# #             # Prepare metadata for MongoDB
# #             metadata = {
# #                 'name': os.path.basename(pdf_path),
# #                 'path': pdf_path,
# #                 'size': os.path.getsize(pdf_path),
# #                 'num_pages': num_pages,
# #                 'summary': final_summary,
# #                 'keywords': final_keywords
# #             }

# #             # Store in MongoDB
# #             existing_doc = collection.find_one({'name': metadata['name']})
# #             if existing_doc:
# #                 logging.info(f"{metadata['name']} already exists in the database.")
# #                 collection.update_one({'_id': existing_doc['_id']}, {"$set": {'summary': final_summary, 'keywords': final_keywords}})
# #                 logging.info(f"Updated {metadata['name']} with new summary and keywords.")
# #             else:
# #                 doc_id = collection.insert_one(metadata).inserted_id
# #                 logging.info(f"Processed {pdf_path} and stored metadata with ID: {doc_id}")

# #     except Exception as e:
# #         logging.error(f"Error processing {pdf_path}: {str(e)}")

# # # Function to process all PDFs in a folder
# # def process_folder(folder_path):
# #     pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
# #     # Process PDFs concurrently
# #     with ProcessPoolExecutor() as executor:
# #         executor.map(process_pdf, pdf_files)

# # if __name__ == "__main__":
# #     folder_path = r"C:\Users\Shivani\OneDrive\Desktop\pdf"  # Replace with your PDF folder path
# #     process_folder(folder_path)

# import os
# import PyPDF2
# import pymongo
# import logging
# from concurrent.futures import ProcessPoolExecutor
# from collections import Counter
# import spacy

# # Load spaCy model for keyword extraction
# nlp = spacy.load("en_core_web_sm")

# # MongoDB Configuration
# client = pymongo.MongoClient('mongodb://localhost:27017/')
# db = client['pdf_db']
# collection = db['pdf_metadata']

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Function to summarize text (improved approach)
# def generate_summary(text, doc_length):
#     sentences = text.split('. ')
#     if doc_length <= 10:
#         return '. '.join(sentences[:2]) + '.' if len(sentences) > 2 else text  # Concise summary for short docs
#     elif 10 < doc_length <= 30:
#         return '. '.join(sentences[:5]) + '.' if len(sentences) > 5 else text  # Medium-length summary
#     else:
#         return '. '.join(sentences[:10]) + '.' if len(sentences) > 10 else text  # Detailed summary for long docs

# # Custom function to extract keywords based on document length
# def extract_keywords(text, doc_length):
#     doc = nlp(text)
    
#     # Filter out stop words, numbers, and very common words
#     keywords = [
#         token.lemma_ for token in doc 
#         if token.is_alpha and not token.is_stop and len(token) > 2
#     ]
    
#     # Use noun chunks and named entities for more meaningful keywords
#     noun_chunks = [chunk.text for chunk in doc.noun_chunks]
#     entities = [ent.text for ent in doc.ents]
    
#     # Combine all keywords, noun chunks, and named entities
#     all_keywords = keywords + noun_chunks + entities
    
#     # Count the frequency of each keyword
#     keyword_freq = Counter(all_keywords)
    
#     # Adjust the number of keywords based on document length
#     if doc_length <= 10:
#         num_keywords = 5  # Short documents get fewer keywords
#     elif 10 < doc_length <= 30:
#         num_keywords = 10  # Medium documents get more
#     else:
#         num_keywords = 15  # Long documents get even more keywords
    
#     # Get the top keywords by frequency
#     final_keywords = [keyword for keyword, _ in keyword_freq.most_common(num_keywords)]
    
#     return final_keywords

# # Function to process a single PDF
# def process_pdf(pdf_path):
#     try:
#         with open(pdf_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             num_pages = len(reader.pages)
#             text = ""

#             # Extract text from all pages
#             for page in reader.pages:
#                 text += page.extract_text() + " "

#             # Generate summary and extract keywords
#             summary = generate_summary(text, num_pages)
#             keywords = extract_keywords(text, num_pages)

#             # Prepare metadata for MongoDB
#             metadata = {
#                 'name': os.path.basename(pdf_path),
#                 'path': pdf_path,
#                 'size': os.path.getsize(pdf_path),
#                 'num_pages': num_pages,
#                 'summary': summary,
#                 'keywords': keywords
#             }

#             # Check if the document already exists in the collection
#             existing_doc = collection.find_one({'name': metadata['name']})
#             if existing_doc:
#                 logging.info(f"{metadata['name']} already exists in the database.")
#                 # Update the existing document with new summary and keywords
#                 collection.update_one({'_id': existing_doc['_id']}, {"$set": {'summary': summary, 'keywords': keywords}})
#                 logging.info(f"Updated {metadata['name']} with new summary and keywords.")
#             else:
#                 # Insert new document into MongoDB
#                 doc_id = collection.insert_one(metadata).inserted_id
#                 logging.info(f"Processed {pdf_path} and stored metadata with ID: {doc_id}")

#     except Exception as e:
#         logging.error(f"Error processing {pdf_path}: {str(e)}")

# # Function to process all PDFs in a folder
# def process_folder(folder_path):
#     pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
#     # Process PDFs concurrently
#     with ProcessPoolExecutor() as executor:
#         executor.map(process_pdf, pdf_files)

# if __name__ == "__main__":
#     folder_path = r"C:\Users\Shivani\OneDrive\Desktop\pdf"  # Replace with your PDF folder path
#     process_folder(folder_path)

import os
import PyPDF2
import pymongo
import logging
from concurrent.futures import ProcessPoolExecutor
from collections import Counter
import spacy

# Load spaCy model for keyword extraction
nlp = spacy.load("en_core_web_sm")

# MongoDB Configuration
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['pdf_db']
collection = db['pdf_metadata']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to summarize text based on document length
def generate_detailed_summary(text, num_pages):
    sentences = text.split('. ')
    
    # Summary length proportional to document size
    if num_pages <= 10:
        summary_sentences = 5  # Short documents
    elif 10 < num_pages <= 30:
        summary_sentences = 10  # Medium-length documents
    else:
        summary_sentences = min(15 + num_pages // 2, len(sentences))  # Long documents
    
    # Extract the key sentences for the summary
    return '. '.join(sentences[:summary_sentences]) + '.' if len(sentences) > summary_sentences else text

# Improved function to extract keywords
def extract_keywords(text, num_pages):
    doc = nlp(text)
    
    # Filter out stop words, numbers, and common words
    words = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop and len(token) > 2]
    
    # Use noun chunks and named entities for more meaningful keywords
    noun_chunks = [chunk.text for chunk in doc.noun_chunks]
    entities = [ent.text for ent in doc.ents]
    
    # Combine words, noun chunks, and named entities
    all_keywords = words + noun_chunks + entities
    
    # Use frequency count to prioritize important terms
    keyword_freq = Counter(all_keywords)
    
    # Define how many keywords to extract based on document size
    if num_pages <= 10:
        num_keywords = 10  # Short documents
    elif 10 < num_pages <= 30:
        num_keywords = 20  # Medium documents
    else:
        num_keywords = min(40, len(keyword_freq))  # Long documents
    
    # Return top `num_keywords` most frequent keywords
    final_keywords = [keyword for keyword, _ in keyword_freq.most_common(num_keywords)]
    
    return final_keywords

# Function to process a single PDF
def process_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            text = ""

            # Extract text from all pages
            for page in reader.pages:
                text += page.extract_text() + " "

            # Generate detailed summary and extract keywords
            summary = generate_detailed_summary(text, num_pages)
            keywords = extract_keywords(text, num_pages)

            # Prepare metadata for MongoDB
            metadata = {
                'name': os.path.basename(pdf_path),
                'path': pdf_path,
                'size': os.path.getsize(pdf_path),
                'num_pages': num_pages,
                'summary': summary,
                'keywords': keywords
            }

            # Check if the document already exists in the collection
            existing_doc = collection.find_one({'name': metadata['name']})
            if existing_doc:
                logging.info(f"{metadata['name']} already exists in the database.")
                # Update the existing document with new summary and keywords
                collection.update_one({'_id': existing_doc['_id']}, {"$set": {'summary': summary, 'keywords': keywords}})
                logging.info(f"Updated {metadata['name']} with new summary and keywords.")
            else:
                # Insert new document into MongoDB
                doc_id = collection.insert_one(metadata).inserted_id
                logging.info(f"Processed {pdf_path} and stored metadata with ID: {doc_id}")

    except Exception as e:
        logging.error(f"Error processing {pdf_path}: {str(e)}")

# Function to process all PDFs in a folder
def process_folder(folder_path):
    pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    # Process PDFs concurrently
    with ProcessPoolExecutor() as executor:
        executor.map(process_pdf, pdf_files)

if __name__ == "__main__":
    folder_path = r"C:\Users\Shivani\OneDrive\Desktop\pdf"  # Replace with your PDF folder path
    process_folder(folder_path)
