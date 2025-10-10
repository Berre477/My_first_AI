import sys
from Timer_ask import Timer
from News import get_bbc_headlines
from Math_reco import MathReco
import datetime
from sentence_transformers import SentenceTransformer, util
from Text_to_speech import text_to_speech
import os
from translate_file import load_database_,save_database

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
os.environ["TOKENIZERS_PARALLELISM"] = "false"
class Chatbot_text:
    def __init__(self):
        self.math_model = MathReco()
        self.database_path = self.database_path or 'Database.json'
        self.database: dict = load_database_(self.database_path)

        self.timer_class = Timer()
        self.text = False


    def process_text(self,text):
        while True:
            speech_text=input("You: ").lower()

            #Tell the time patterns
            time_patterns = [
                "what time", "current time", "time now", "tell me time", "what is the time"
            ]

            # News paterns
            news_patterns = [
                "news", "headlines", "what's happening", "current events", "latest news"
            ]

            # Farewell patterns
            farewell_patterns = [
                "goodbye", "bye", "exit", "quit", "turn off", "shut down", "end", "off"
            ]

            # Greeting patterns
            greeting_patterns = [
                "hello", "hi ", "hey", "greetings", "howdy", "good morning", "good afternoon",
                "good evening", "what's up",
            ]

            # Math patterns
            math_patterns = [
                '+', '-', ' x ', '/'
            ]
            # Timer patterns
            start_timer_patterns = [
                "set a timer", "set timer"
            ]
            stop_timer_patterns = ["stop the timer", "timer stop" ]

            data = {
                tuple(start_timer_patterns): self.start_timer,
                tuple(stop_timer_patterns): self.stop_timer,
                tuple(math_patterns): self.calculate_math,
                tuple(greeting_patterns): self.greetings,
                tuple(time_patterns): self.handle_time,
                tuple(farewell_patterns): self.turn_off,
                tuple(news_patterns): self.handle_news}


    
    def print_and_speech(text:str):
         print(text)
         text_to_speech(text,"en")

    def turn_off(self):
        self.print_and_speech("Turning off")
        sys.exit()

    @staticmethod
    def retrieve_relevant_question_nlp(query, database):
        questions = [entry['question'] for entry in database['questions']]

        if not questions:
            return {"question": "", "answer": ""}, 0.0

        query_embedding = embedding_model.encode(query, convert_to_tensor=True)
        query_embedding = query_embedding.unsqueeze(0)

        question_embeddings = embedding_model.encode(questions, convert_to_tensor=True)

        similarities = util.cos_sim(query_embedding, question_embeddings)
        best_match_index = similarities.argmax().item()
        best_match = database['questions'][best_match_index]
        confidence = similarities[0][best_match_index].item()

        return best_match, confidence






