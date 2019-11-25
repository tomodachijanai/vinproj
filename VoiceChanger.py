import io
# from pydub import AudioSegment
# from pydub.playback import play
import pyaudio
import speech_recognition as sr
import librosa
import soundfile as sf

class Voice_changer():

    def recognize_from_micro(self, n=5):
        self.r = sr.Recognizer()
        with sr.Microphone() as source:
            self.audio = self.r.record(source, n)
        with open("microphone-results.wav", "wb") as f:
            f.write(self.audio.get_wav_data())
        # self.song = AudioSegment.from_wav(io.BytesIO(self.audio.get_wav_data()))

    def voice_effect(self, octaves=1):
        filename = 'microphone-results.wav'
        y, sr = librosa.load(filename)

        y_third = librosa.effects.pitch_shift(y, sr, n_steps=octaves)
        sf.write('m1.wav', y_third, sr, format="wav")
        return sr
        # new_sample_rate = int(self.song.frame_rate * (2.0 ** octaves))
        # self.modified_sound = self.song._spawn(self.song.raw_data, overrides={'frame_rate': new_sample_rate})
        # self.modified_sound = self.modified_sound.set_frame_rate(44100)
        # return self.modified_sound.raw_data