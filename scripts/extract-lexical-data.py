# extract CHI-MLU, CHI-tokens, CHI-types, File-name, MOT-MLU, MOT-tokens, MOT-types, shared-types
# export to .csv

from os import chdir as cd
import pandas as pd
import glob

path_func = 'PATH/functions'
cd(path_func)
import MLU
import get_types_tokens

transcripts = []
chi_mlu = []
mot_mlu = []
mot_types = []
chi_types = []
shared_types = []
mot_tokens = []
chi_tokens = []


pathin = 'PATH'
pathout = 'PATH'

cd(pathin)

for file in glob.glob('*.txt'):
    f = MLU.CHI(file)
    transcripts.append(file)
    chi_mlu.append(f)
    f = MLU.MOT(file)
    mot_mlu.append(f)
    h = get_types_tokens.get_types_tokens(file)
    mot_types.append(h[0])
    chi_types.append(h[1])
    shared_types.append(h[2])
    mot_tokens.append(h[3])
    chi_tokens.append(h[4])
    

df = pd.DataFrame(
    {'File-name': transcripts,
     'CHI-MLU': chi_mlu,
     'MOT-MLU': mot_mlu,
     'MOT-types': mot_types,
     'CHI-types': chi_types,
     'shared-types': shared_types,
     'MOT-tokens': mot_tokens,
     'CHI-tokens': chi_tokens
    })

#re-arrange column order
cols = ['File-name', 'CHI-MLU', 'CHI-tokens', 'CHI-types', 'MOT-MLU', 'MOT-tokens', 'MOT-types', 'shared-types']
df = df[cols]

#write data to csv
cd(pathout)
df.to_csv('data.csv', sep=',', encoding='utf-8')