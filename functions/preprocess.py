import os
from collections import Counter
from string import punctuation
import glob
import re
import pandas as pd


class Transcript:
    """This class is a representation of a transcript following the norm from
    the CHILDES database. The class includes methods to obtain headers, utterances, pos, comments, child age, and a method for exporting the data as a pandas dataframe. The class is intended as preprocessing tool to convert CHAT files for use in automatic speech act classification using the childes-speech-acts tool found here: https://github.com/mitjanikolaus/childes-speech-acts. 
    
Example usage:

file = "/path/to/childes_file.txt"
t = pp.Transcript(file)
df = t.to_dataframe()
df


"""

    def __init__(self, filepath):
        try:
            file = open(filepath, 'r', encoding='utf-8')
            self.filename = os.path.basename(file.name)
            self.raw_transcript = file.read()
            
            
            remove_list = ['\t', '\r']
            for item in remove_list:
                self.raw_transcript = self.raw_transcript.replace(item, '')
                
            # extract headerlines and transcriptlines
            text = self.raw_transcript.split('\n')
            self.headers = []
            self.lines = []
            self.mor = []
            self.comment = []
            for s, val in enumerate(text):
                    if val.startswith('@Comment'):
                        text[s] = val.replace('@Comment', '^^Comment')
            for line in text:
                if line.startswith('@'):
                    self.headers.append(line)
                elif line.startswith('*'):
                    self.lines.append(line)
                elif line.startswith('%'):
                    self.mor.append(line)
                elif line.startswith('^^Comment'):
                    self.comment.append(line)
                else:  # continuation of previous line
                    if not self.lines:
                        self.headers[-1] = self.headers[-1] + line
                    else:
                        self.lines[-1] = self.lines[-1] + line
                        
            self.target_child = []
            for entry in self.headers:
                if entry.startswith('@Participants'):
                    temp = entry.split(':')
                    temp = temp[1].split(',')
                    for i in temp:
                        if "Target_Child" in i:
                            c = i.replace("Target_Child", "")
                            c = c.replace("CHI ","")
                            self.target_child.append(c.strip())
            self.age = []
            for entry in self.headers:
                if entry.startswith('@Age of CHI:'):
                    temp = entry.split(':')
                    temp = temp[1].split(';')
                    m = float(temp[0])
                    d = float(temp[1])
                    months = m + (d/30)
                    self.age.append(months)
            
            self.tokens = []
            self.speaker = []
            for line in self.lines:
                temp = line.split(':')
                self.speaker.append(temp[0][1:])
                t = temp[1].split(' ')
                self.tokens.append(t)
            
            self.pos = []
            exclusions = ['','.', '!', '?']
            for line in self.mor:
                pos_line = []
                temp = line.split('mor:')
                temp = temp[1].split(' ')
                for entry in temp:
                    entry = entry.split('|')
                    if entry[0] not in exclusions:
                        pos_line.append(entry[0])
                        self.pos.append(pos_line)            
            self.fully_loaded = True  # flag that transcript is fully loaded
            
        except IOError as e:
            self.fully_loaded = False  # flag that transcript was not loaded
            print('An error occured when loading:', filepath)
            print('Error message:', e)
        if len(self.lines) > len(self.pos):
            n = len(self.lines) - len(self.pos)
            print(n, 'utterances are missing POS tags!')
        elif len(self.lines) < len(self.pos):
            print('there are POS tags that are unmatched with an utterance!')



#################################################
### methods to get individual attributes.########
### mostly for debugging and trouble-shooting ###
#################################################

    def get_headers(self):
        return self.headers

    def get_lines(self):
        return self.lines
        
    def get_mor(self):
        return self.mor

    def get_pos(self):
        return self.pos
        
    def get_comments(self):
        return self.comment

    def get_child_id(self):
        return self.target_child

    def get_transcript_file(self):
        return self.filename
        
    def get_age(self):
        return self.age
        
    def get_tokens(self):
        return self.tokens

    def get_speaker(self):
        return self.speaker

#################################################
### method to convert to pandas dataframe  ######
#################################################

    def to_dataframe(self):
        utterance_id = []
        transcript_file = []
        child_id = []
        age_months = []
        tokens = []
        pos = []
        speaker = []
        for s, val in enumerate(self.lines):
            utterance_id.append(s)
            transcript_file.append(self.filename)
            child_id = self.target_child[0]
            age_months = self.age[0]
            tokens.append(str((self.tokens[s])))
            speaker.append(self.speaker[s])
            pos.append(str(self.pos[s]))
    

        df = pd.DataFrame(
            {'utterance_id': utterance_id,
             'transcript_file': transcript_file,
             'child_id': child_id,
             'age_months': age_months,
             'speaker': speaker,
             'tokens': tokens,
             'pos': pos
            },
            dtype = 'object') 
        return df
