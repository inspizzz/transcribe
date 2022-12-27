import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
from word import Word as Word
from pydub import AudioSegment



class Transcribe:
    def __init__(self, model_path="models/vosk-model-small-en-us-0.15"):
        self.model_path = model_path

        self.model = Model(self.model_path)
        self.audio = None

        self.results = []
        self.segment = AudioSegment.empty()


    def recognize(self):
        if self.audio:
            while True:
                data = self.audio.readframes(4000)
                if len(data) == 0:
                    break
                if self.recording.AcceptWaveform(data):
                    part_result = json.loads(self.recording.Result())
                    self.results.append(part_result)
            part_result = json.loads(self.recording.FinalResult())
            self.results.append(part_result)
        else:
            print("No audio file loaded")

    def getWords(self):
        list_of_words = []

        for sentence in self.results:
            if len(sentence) == 1:
                continue

            for obj in sentence['result']:
                w = Word(obj)  # create custom Word object
                list_of_words.append(w)  # and add it to list
        
        return list_of_words

    def openAudio(self, audio_filename="audio/audio1.wav"):
        self.audio = wave.open(audio_filename, "rb")
        self.recording = KaldiRecognizer(self.model, self.audio.getframerate())
        self.recording.SetWords(True)

    def closeAudio(self):
        self.audio.close()

    def split(self, start:float, end:float) -> list:

        # works in ms
        start *= 1000
        end *= 1000 
        gap = 0
        # get and split the segmentd
        newAudio = AudioSegment.from_wav("audio/audio1.wav")
        newAudio = newAudio[int(start)-gap:int(end)+gap]

        return newAudio

    def join(self, audio:AudioSegment=AudioSegment.empty()) -> AudioSegment:
        self.segment += audio

    def save(self, name:str) -> None:
        self.segment.export(name+".wav", format="wav")

        