import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import cv2
import wikipediaapi
import subprocess
import os


class VoiceAssistantApp:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = True  
        self.is_running = True 

        # Initialize Wikipedia API with user agent
        self.wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent='VoiceAssistant/1.0'
        )
        
        self.applications = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
        }
            
        self.listen_for_wakeup()
    
    
    def listen_for_wakeup(self):
        while self.is_listening and self.is_running:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening for wakeup word and command...")
                audio = self.recognizer.listen(source)
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    print(f"Heard: {text}")                 # Print what the assistant hears
                    
                    if text.lower().startswith("computer"):
                        command = text.lower().replace("computer", "").strip()
                        print(f"You said: {command}")
                        self.engine.say("Yes sir")
                        self.engine.runAndWait()
                        self.respond(command)
                except sr.UnknownValueError:
                    pass                                    # Silence the error in the face :v
                except sr.RequestError:
                    print("Network error")
    
    def respond(self, command):
        response = ""
        
        if "time" in command:
            response = self.get_time()
        elif "create file" in command or "create a file" in command:
            response = self.create_file()
        elif "open camera" in command or "take selfie" in command:
            response = self.open_camera(command)
        elif "open" in command and any(app in command for app in self.applications):
            response = self.open_application(command)
        elif "search" in command:
            response = self.search_web(command)
        elif "wikipedia" in command:
            response = self.search_wikipedia(command)
        elif "close" in command:
            self.close_assistant()
            return
        else:
            response = self.extract_info(command)
        
        print(f"Response: {response}")                      # printing response boss :)
        self.engine.say(response)
        self.engine.runAndWait()

    def get_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {current_time}"

    def create_file(self):
        filename = "nigga.txt"
        with open(filename, 'w') as file:
            file.write("This is a new file created by the voice assistant.")
            file.close()
        return f"File {filename} created successfully."

    def open_camera(self, command):
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("Camera")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Camera", frame)

            if "take selfie" in command:
                cv2.imwrite("selfie.jpg", frame)
                cap.release()
                cv2.destroyAllWindows()
                return "Selfie taken and saved as selfie.jpg"

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return "Camera closed."
    
    def open_application(self, command):
        for app, path in self.applications.items():
            if app in command:
                try:
                    subprocess.Popen(path)
                    return f"Opening {app}"
                except Exception as e:
                    return f"Failed to open {app}: {str(e)}"
        return "Application not recognized."

    def search_web(self, command):
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query}"

    def search_wikipedia(self, command):
        query = command.replace("wikipedia", "").strip()
        try:
            page = self.wiki_wiki.page(query)
            if page.exists():
                summary_lines = page.summary.split('\n')
                first_three_lines = '\n'.join(summary_lines[:3])
                return first_three_lines
            else:
                return "No page found for the query."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def extract_info(self, command):
        if "tell me about" in command or "what is" in command:
            query = command.replace("tell me about", "").replace("what is", "").strip()
            response = self.search_wikipedia(query)
        else:
            response = "Sorry, I don't understand that command."
        return response

    def close_assistant(self):
        response = "Closing the assistant"
        print(response)
        self.engine.say(response)
        self.engine.runAndWait()
        self.is_running = False                                     # Shut main loop in the face :)

if __name__ == "__main__":
    app = VoiceAssistantApp()                   # aja mera main function.....
