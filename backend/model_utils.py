import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FAQMatcher:
    def __init__(self, csv_path):
        """
        Initialize the FAQ matcher with a CSV file containing questions and answers.
        
        Args:
            csv_path (str): Path to the CSV file with columns: Question_ID, Question, Answer
        """
        self.model = None
        self.faq_df = None
        self.question_embeddings = None
        
        try:
            # Load the CSV file
            self.faq_df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(self.faq_df)} FAQ entries from {csv_path}")
            
            # Load the Sentence-BERT model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Loaded Sentence-BERT model")
            
            # Encode all questions
            self.encode_questions()
        except Exception as e:
            logger.error(f"Error initializing FAQ matcher: {e}")
            raise
    
    def encode_questions(self):
        """Encode all questions in the FAQ dataset."""
        if self.faq_df is None or self.model is None:
            raise ValueError("FAQ dataframe or model not initialized")
        
        questions = self.faq_df['Question'].tolist()
        self.question_embeddings = self.model.encode(questions)
        logger.info(f"Encoded {len(questions)} questions")
    
    def find_best_match(self, query, threshold=0.5):
        """
        Find the best matching question and answer for a given query.
        
        Args:
            query (str): The user's question
            threshold (float): Minimum similarity score to consider a match
            
        Returns:
            tuple: (answer, similarity_score, question)
        """
        try:
            # Encode the query
            query_embedding = self.model.encode([query])
            
            # Calculate cosine similarity
            similarities = cosine_similarity(
                query_embedding, 
                self.question_embeddings
            )[0]
            
            # Get the index of the most similar question
            best_idx = np.argmax(similarities)
            best_score = similarities[best_idx]
            
            if best_score < threshold:
                return (
                    "I'm not sure I understand your question. Could you please rephrase?",
                    best_score,
                    None
                )
            
            best_question = self.faq_df.iloc[best_idx]['Question']
            best_answer = self.faq_df.iloc[best_idx]['Answer']
            
            return (best_answer, best_score, best_question)
        
        except Exception as e:
            logger.error(f"Error finding match for query: {e}")
            return ("Sorry, I encountered an error processing your question.", 0.0, None)
