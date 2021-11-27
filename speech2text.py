#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import wave
import json
import csv
import pathlib

SetLogLevel(0)

Model_PATH = "../vosk-model-en-us-0.22"


# Load all speeches
speeches = []
with open('aliases.csv', newline='') as f:
    speech_reader = csv.reader(f)
    # skip first header line
    speech_reader.__next__()
    for line in speech_reader:
        speech = line[-1].split('|')
        speeches.extend(speech)


wf_filename = input("Please input pacenotes audio filename:")
wf = wave.open(wf_filename, "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model(Model_PATH)
rec = KaldiRecognizer(model, wf.getframerate(), json.dumps(speeches))
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
    pacenotes.append([start, start, content])

p_filename = pathlib.Path(wf_filename).with_suffix('.csv')
with open(p_filename, "w", newline="") as f:
    f_csv = csv.writer(f, delimiter='\t')
    f_csv.writerows(pacenotes)
# print(rec.FinalResult())
