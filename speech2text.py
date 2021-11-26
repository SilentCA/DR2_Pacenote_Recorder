#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json

SetLogLevel(0)

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

results = []
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        results.append(rec.Result())
        # print(rec.Result())
    else:
        # print(rec.PartialResult())
        pass
results.append(rec.FinalResult())

pacenotes = []
for res in results:
    jres = json.loads(res)
    if not 'result' in jres:
        continue
    words = jres['result']
    content = " ".join([w['word'] for w in words])
    start = words[0]['start']
    pacenotes.append([start, content])

# print(rec.FinalResult())
