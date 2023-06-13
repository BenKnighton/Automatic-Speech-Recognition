"""
In this code, I have made some changes to the typical Vosk Models, https://alphacephei.com/vosk/models
so that the result, which has the preface final: now instead has some "got" which receive a better answer (better than the partial)
much faster than waiting for the final. if the final and the last got are not the same, then the final is used.
If the code starts running from the got, and the final is the same as the got, then there is no need to re-start the entire code,
 it has already been running from the last received correct "got”.
"""



import pyaudio
from vosk import Model, KaldiRecognizer
import ast
# import queue

print("Loading Flies")

model = Model("vosk-model-en-us-0.22")
print("Ready!")
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


import time
import threading




def write_answer(speech):
    with open("history.txt", "w", encoding='utf-8') as f:
        f.write(str(speech))
        f.close()


def read_answer():
    with open("history.txt", "r", encoding='utf-8') as f:
        data = f.readlines()
        f.close()
        return data





class MainEvent(threading.Thread):
    
    def __init__(self, name="MainEvent"):
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        threading.Thread.__init__(self, name=name)

    def predict(self):
        # print("started")

        # print("queue:", read_answer())
        # time.sleep(1)
        return read_answer()

    def inference_loop(self):
        pass
        # print(self.predict())


    def run(self):
        self.inference_loop()
        while not self._stopevent.is_set():
            self._stopevent.wait(self._sleepperiod)

    def end(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)










def end_threads():
    try:
        for i in threading.enumerate():
            if str(i.name) == "MainEvent":
                i.end()
    except Exception:
        pass
    return








asr_engine = MainEvent()
results = []
got = ""
ending = False
happen = False
while True:
    data = stream.read(3000, exception_on_overflow = False) #makes is faster the  #2000
    if len(data) == 0:
        break

    #deep learning speech recognition
    if rec.AcceptWaveform(data):
        final = ast.literal_eval(rec.Result())["text"] #instead of this i think i can put google sr here?
        if len(final) != 0:
            print("final", final)
            results.append(final)
            ending = True

    else:
        partial = ast.literal_eval(rec.PartialResult())["partial"]
        if len(str(partial)) > 3:
            # print(partial)
            results.append(partial)


    #conditions
    if len(results) > 1:
        if results[-1] == results[-2]:
            # print("yes going")
            if got != results[-1]:
                got = results[-1]
                write_answer(results[-1])
                print("got:", got)
                end_threads()
                asr_engine = MainEvent()
                asr_engine.start()
            
            happen = False

        else:
            # print("no, ending")
            happen = True
            end_threads()

    if ending:
        if happen:
            write_answer(results[-1])
            print("got:", results[-1])
            end_threads()
            asr_engine = MainEvent()
            asr_engine.start()
            happen = False

        results.clear()
        ending = False

