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
    from Chatbot_text import chatbot_text
    from transformers import pipeline
    from sentence_transformers import SentenceTransformer, util
    from Chatbot_text import chatbot_text
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

except KeyboardInterrupt:
    pass






def print_and_speech(speech):
    print(f"CB: {speech}")
    text_to_speech(speech,"en")


def load_database(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        if 'questions' not in data:
            raise ValueError("Invalid database format. 'questions' key missing.")
        return data
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading database: {e}")
        return {"questions": []}


def save_database(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


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

def greetings():
    hour = datetime.now().hour
    if hour < 12:
        return 'Good morning, how can I be of help to you?'
    elif hour < 18:
        return "Good afternoon,how can I be of help to you?"
    else:
        return "Good evening, how can I be of help to you?"


class VoiceChatbot:
    def __init__(self, database_path=None):
        self.database_path = database_path or 'Database.json'
        self.database: dict = load_database(self.database_path)
        self.recognizer = sr.Recognizer()
        self.math_reco = MathReco()
        self.timer_class = Timer()
        self.text = False




    def process_command(self, speech):
        if not speech:
            return

        # Handle text mode switch
        if speech.lower() == "text":
            chatbot_text()


        # Convert speech to lowercase for better pattern matching
        speech_lower = speech.lower()

        # Time patterns
        time_patterns = [
            "what time", "current time", "time now", "tell me time","what is the time"
        ]

        #News paterns
        news_patterns = [
            "news", "headlines", "what's happening", "current events", "latest news"
        ]

        # Farewell patterns
        farewell_patterns = [
            "goodbye", "bye", "exit", "quit", "turn off", "shut down", "end","off"
        ]

       # Greeting patterns
        greeting_patterns = [
            "hello", "hi ", "hey", "greetings", "howdy", "good morning", "good afternoon",
            "good evening", "what's up",
        ]

       #Math patterns
        math_patterns = [
            '+', '-', ' x ', '/'
        ]
        # Timer patterns
        start_timer_patterns = [
            "set a timer","set timer"
        ]
        stop_timer_patterns=[
            "stop the timer","timer stop"
        ]




        # Check for time patterns
        if any(pattern in speech_lower for pattern in time_patterns):
            VoiceChatbot.handle_time()
            return

        # Check for news patterns
        if any(pattern in speech_lower for pattern in news_patterns):
            VoiceChatbot.handle_news()
            return

        # Check for farewell patterns
        if any(pattern in speech_lower for pattern in farewell_patterns):
            print_and_speech("Turning off")
            sys.exit()

        # Check for math patterns
        if any(pattern in speech_lower for pattern in math_patterns):
            result = self.math_reco.main_math(speech)
            print(f"CB: {result}")
            text_to_speech(str(result), "en")
            return


        # Check for greeting patterns
        if any(pattern in speech_lower for pattern in greeting_patterns) and len(speech_lower.split()) < 5:
            response = greetings()
            print_and_speech(response)
            return

        #Check for start timer patterns
        if any(pattern in speech_lower for pattern in start_timer_patterns):
            self.timer_class.set_timer(speech_lower.split())
            self.timer_class.translate_time()
            print_and_speech(self.timer_class.return_start_time())
            self.timer_class.start_timer()
            return
        #Check for stop timer patterns
        if any(pattern in speech_lower for pattern in stop_timer_patterns):
            if self.timer_class.is_running:
                self.timer_class.stop_timer()
                print_and_speech("Stopping timer")
                return
            else:
                print_and_speech("No timer is running")
                return


        else :

            best_match,confidence = retrieve_relevant_question_nlp(speech_lower,self.database)
            if confidence > 0.6 :
                print_and_speech(f"{best_match['answer']}", )
            else:
                print_and_speech("I dont know this could ,you teach me")
                self.learn_new_answer(speech_lower)

    def handle_time(self):
        time = datetime.now()
        time_response = f'It is {time.strftime("%I")}:{time.strftime("%M")} {time.strftime("%p")}'
        print_and_speech(time_response)
        return

    def handle_news(self):
        bbc_head = get_bbc_headlines()
        if bbc_head:
            for idx, news in enumerate(bbc_head, 1):
                print(f"{idx}. {news}")
                text_to_speech(f" {news}", 'en')

            return
        else:
            print_and_speech("No news to display at the moment.")
            return

    def learn_new_answer(self, question):
        new_answer = input('Write the answer or type "skip" to skip: ')

        if new_answer.lower() != 'skip':
            self.database['questions'].append({
                'question': question,
                'answer': new_answer
            })
            save_database(self.database_path, self.database)
            print_and_speech('Thank you for teaching me!')
        else:
            print_and_speech("Skipped Learning")



    def listen_to(self):
        try:
            with sr.Microphone() as source:
                print("CB: Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source,timeout=5,phrase_time_limit=10)

            speech = self.recognizer.recognize_google(audio)
            print(f"You: {speech}")
            return speech
        except sr.UnknownValueError:
            print("CB:Sorry I didn't catch that")
            return None
        except sr.RequestError:
            print("CB: Could not request results from Google Speech Recognition service.")
            return None
        except sr.WaitTimeoutError:
            print("No speech detected in time (timeout). Skipping.")

    def run(self):
        greet = greetings()
        print_and_speech(greet)


        try:
            while True:
                speech = self.listen_to()
                if speech:
                    self.process_command(speech)

        except KeyboardInterrupt:
            print_and_speech("Goodbye")

