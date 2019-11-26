import io
from pydub import AudioSegment
from pydub.playback import play
import wave
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

    def voice_effect(self, tones):
        # filename = 'microphone-results.wav'
        filename = 'microphone-results.wav'
        y, sr = librosa.load(filename)
        def apply_tone(tone):
            return librosa.effects.pitch_shift(y, sr, n_steps=tone) 
        ys = list(map(apply_tone, tones))
        # ys.append(y)
        for f in range(len(ys)):
            sf.write(f'm{f}.wav', ys[f], sr, format="wav")
        # y_third = librosa.effects.pitch_shift(y, sr, n_steps=tones)
        # sf.write('m1.wav', y_third, sr, format="wav")
        # sf.write('m2.wav', y, sr, format="wav")
        # a = AudioSegment.from_wav("m2.wav")
        # a.apply_gain(0.6)
        # a.export(out_f="m2.wav", format="wav")
        infiles = [f"m{i}.wav" for i in range(len(ys))]
        outfile = "sounds.wav"
        sounds = [AudioSegment.from_file(i) for i in infiles]
        composed = sounds[0]
        for i in sounds[1:]:
            composed = composed.overlay(i)
        composed.export("sounds.wav")
        # librosa.output.write_wav("sounds.wav", *librosa.load("sounds.wav"))
        # sf.write("sounds.wav", composed.raw_data, sr, format="wav", )
        #play(composed)
        return sr
        # new_sample_rate = int(self.song.frame_rate * (2.0 ** tones))
        # self.modified_sound = self.song._spawn(self.song.raw_data, overrides={'frame_rate': new_sample_rate})
        # self.modified_sound = self.modified_sound.set_frame_rate(44100)
        # return self.modified_sound.raw_data