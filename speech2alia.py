#!/usr/bin/env python3

import csv
import pathlib
import ahocorasick


# File paht
# pacenotes file in speech format
p_speech_filename = input("Please input pacenotes filename(in speech format):")
p_speech_filename = pathlib.Path(p_speech_filename)
# pacenotes file in alias format
p_alia_filename = p_speech_filename.with_stem(p_speech_filename.stem + '_alias')

# Load all speeches
alias = []
speeches = []
with open('aliases.csv', newline='') as f:
    speech_reader = csv.reader(f)
    # skip first header line
    speech_reader.__next__()
    for line in speech_reader:
        speech = line[-1].split('|')
        speeches.extend(speech)
        alias.extend([line[0]] * len(speech))

# Load pacenotes in speech format
pacenotes_speech = []
start_time = []
with open(p_speech_filename, 'r', newline='') as f:
    p_reader = csv.reader(f, delimiter='\t')
    for line in p_reader:
        pacenotes_speech.append(line[-1])
        start_time.append(line[0])

# Make automaton
auto = ahocorasick.Automaton()
for alia, speech in zip(alias, speeches):
    auto.add_word(speech, alia)
auto.make_automaton()

# Speech to alia
pacenotes_alia = []
for line in pacenotes_speech:
    alias_line = auto.iter_long(line)
    pacenotes_alia.append(','.join(item[-1] for item in alias_line))

# Save pacenotes in alias format
with open(p_alia_filename, 'w', newline='') as f:
    f_csv = csv.writer(f, delimiter='\t')
    f_csv.writerows(zip(start_time,start_time,pacenotes_alia))
