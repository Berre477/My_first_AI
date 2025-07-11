from VoiceBot import retrieve_relevant_question_nlp
from Timer_ask import Timer
from News import get_bbc_headlines
from Math_reco import MathReco
import datetime
def chatbot_text():

    while True:
        the_input=input("You: ").lower()

        # Time patterns
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
        stop_timer_patterns = [
            "stop the timer", "timer stop"
        ]

        #Tell the time
        if any(  pattern in time_patterns for pattern in time_patterns ):
            time = datetime.now()
            time_response = f'It is {time.strftime("%I")}:{time.strftime("%M")} {time.strftime("%p")}'
            print(f"CB: {time_response}")

        #Math operations

