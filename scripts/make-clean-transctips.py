# make "clean" transcripts
# do not replace "FAT", "AUN", etc.

from os import chdir as cd
import glob

path_func = 'PATH/functions'
cd(path_func)
import getmotchi

pathin = 'PATH'
pathout = 'PATH'

cd(pathin)

for file in glob.glob('*.txt'):
    f = '\n'.join(getmotchi.getmotchi(file))
    cd(pathout)
    with open('c_'+file, 'a+') as newfile:
        newfile.write(f)
        cd(pathin)
    