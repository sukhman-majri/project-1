from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color
import speech_recognition as sr
import pyttsx3

class AssistantWidget(Widget):
    def __init__(self, **kwargs):
        super(AssistantWidget, self).__init__(**kwargs)

        # Draw a big round circle
        with self.canvas:
            Color(0.3, 0.5, 0.8)  # Set color (RGB)
            self.circle = Ellipse(pos=self.pos, size=(300, 300))

        # Initialize SpeechRecognition
        self.recognizer = sr.Recognizer()

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

        # Add a Label widget for displaying recognized text
        self.label = Label(text='', pos=self.center, font_size=20, font_name='Roboto-Bold',
                           size_hint=(None, None), size=(300, 100), halign='center', valign='middle')
        self.add_widget(self.label)

        # Add a Label at the top-left of the window
        self.developer_label = Label(text="Developed by: Sukhman Majri", pos=(10, self.height - 30),
                                     font_size=16, font_name='Roboto-Bold', color=(1, 1, 1, 1))
        self.add_widget(self.developer_label)

    def on_size(self, instance, value):
        # Update the circle size when the widget size changes
        self.circle.size = self.size

    def on_touch_down(self, touch):
        if self.is_point_inside_circle(touch.pos):
            # Start speech recognition
            self.recognize_speech()

    def is_point_inside_circle(self, point):
        # Check if the point is inside the circle
        cx, cy = self.center
        r = self.circle.size[0] / 2  # Assuming the circle is a perfect circle
        return (point[0] - cx) ** 2 + (point[1] - cy) ** 2 <= r ** 2

    def recognize_speech(self):
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio_data = self.recognizer.listen(source, timeout=5)
                print("Recognition in progress...")
                text = self.recognizer.recognize_google(audio_data)
                print("You said: ", text)

                # Update the label with the recognized text
                self.label.text = f'You said:\n{text.capitalize()}'

                # Speak the recognized text
                self.engine.say(text)
                self.engine.runAndWait()

        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == '__main__':
    from kivy.app import App

    class AssistantApp(App):
        def build(self):
            return AssistantWidget()

    AssistantApp().run()
