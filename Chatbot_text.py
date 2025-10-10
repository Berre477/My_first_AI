try:
    import sys
    import speech_recognition as sr
    from datetime import datetime
    from Math_reco import MathReco
    from Text_to_speech import text_to_speech
    import json
    from Timer_ask import Timer
    from News import get_bbc_headlines
    import os
    from googletrans import Translator
    translator = Translator()
    from transformers import pipeline
    from sentence_transformers import SentenceTransformer, util
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    import json
except KeyboardInterrupt:
    pass



def load_database(file_path: str):
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
        return data


def save_database(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


class Chatbot_text:
    def __init__(self,database_path=None):
        self.math_model = MathReco()
        self.database_path = database_path or 'Database.json'
        self.database: dict = load_database(self.database_path)
        self.timer_class = Timer()
        self.text = False


    def process_text(self):
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
            matched = False
            for patterns, func in data.items():
                if any(pattern in speech_text for pattern in patterns):
                    matched = True
                    if func in [self.calculate_math, self.start_timer]:
                        func(speech_text)
                    else:
                        func()
                    break  # Important to break on first match

            if not matched:
                best_match, confidence = self.retrieve_relevant_question_nlp(speech_text, self.database)
                if confidence > 0.6:
                    print(best_match['answer'])
                else:
                    print("I dont know this could ,you teach me")
                    self.learn_new_answer(speech_text)

    def greetings(self):
        hour = datetime.now().hour
        if hour < 12:
            return 'Good morning, how can I be of help to you?'
        elif hour < 18:
            return "Good afternoon,how can I be of help to you?"
        else:
            return "Good evening, how can I be of help to you?"
    
    def print_and_speech(self,text:str):
         print(text)
         text_to_speech(text,"en")

    def turn_off(self):
        self.print_and_speech("Turning off")
        sys.exit()

    @staticmethod
    def handle_time():
        time = datetime.now()
        time_response = f'It is {time.strftime("%I")}:{time.strftime("%M")} {time.strftime("%p")}'
        print(time_response)
        return

    @staticmethod
    def handle_news():
        bbc_head = get_bbc_headlines()
        if bbc_head:
            for idx, news in enumerate(bbc_head, 1):
                print(f"{idx}. {news}")
            return
        else:
            print("No news to display at the moment.")
            return



    def retrieve_relevant_question_nlp(self,query, database):
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

    #Start timer
    def start_timer(self,speech):
        self.timer_class.set_timer(speech.split())
        self.timer_class.translate_time()
        print(self.timer_class.return_start_time())
        self.timer_class.start_timer()
        return

    #Stopping timer
    def stop_timer(self,speech):
        if self.timer_class.is_running:
            self.timer_class.stop_timer()
            print("Stopping timer")
            return
        else:
            print("No timer is running")
            return
    def calculate_math(self,speech):
        result = self.math_model.main_math(speech)
        print(f"CB: {result}")
        return
    def learn_new_answer(self, question):
        new_answer = input('Write the answer or type "skip" to skip: ')

        if new_answer.lower() != 'skip':
            self.database['questions'].append({
                'question': question,
                'answer': new_answer
            })
            save_database(self.database_path, self.database)
            print('Thank you for teaching me!')
        else:
            print("Skipped Learning")

t=Chatbot_text()
t.process_text()






