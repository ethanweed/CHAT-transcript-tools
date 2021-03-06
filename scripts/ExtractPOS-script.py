import os
import glob

pathin = '/path/to/data/'
pathout = '/path/to/output/folder'



os.chdir(pathin)

removelist = ['\t', '\r']

for file in glob.glob('*.txt'):
    try:

        with open(file,'r') as f:
            text = f.read()
            for item in removelist:
                text = text.replace(item, '')
            text = text.split('@')


            for line in text:
                if line.startswith('Participants:'):
                    p = line.replace('Participants:', '')
                    p = p.split(',')

                    p1 = []
                    for i, val in enumerate(p):
                        v1 = val.replace(' ','')
                        v2 = v1.replace('\n', '')
                        p1.append(v2[0:3])
            people = p1


        with open(file,'r') as f:
            text = f.read()
            for item in removelist:
                text = text.replace(item, '')
            text = text.split('\n')

            trans = []
            for line in text:
                label = line[1:4]
                if label in people:
                    trans.append(line)
                elif label == 'mor':
                    trans.append(line)

        grouped = [trans[n:n+2] for n in range(0, len(trans), 2)]


        p = '.!?'

        turn = []
        speaker = []
        mor = []
        for i, val in enumerate(grouped):
            turn.append(i+1)

        for i in grouped:
            s = i[0]
            m = i[1]
            for c in p:
                m = m.replace(c, '')
                m = m.strip()
                m = m.replace('%mor:', '')
            speaker.append(s[1:4])
            mor.append(m)

        z = list(zip(turn, speaker, mor))


        turn = []
        speaker = []
        pss = []
        wds = []
        for i, val in enumerate(z):
            x = z[i]
            t = x[0]
            s = x[1]
            m = x[2]
            m = m.split(' ')
            p = []
            w = []
            for n in m:
                temp = n.split('|')
                p.append(temp[0])
                w.append(temp[1])
            turn.append(t)
            speaker.append(s)
            pss.append(p)
            wds.append(w) 

        pw = list(zip(turn,speaker,pss,wds))


        lines = []
        for i in pw:
            num = str(i[0])
            speaker = i[1]
            wds = i[3]
            pss = i[2]
            for j, val in enumerate(pss):
                p = pss[j]
                w = wds[j]
                temp = num + ',' + speaker + ',' + w + ',' + p + '\n'
                lines.append(temp)  


        lines2 = []
        sep = '-~&'
        for i in lines:
            s = i.split(',')
            w1 = s[2]
            for c in sep:
                w1 = w1.replace(c, '$')
            w1 = w1.split('$')
            w1 = w1[0]
            num = s[0]
            speaker = s[1]
            word = w1
            wordplus = s[2]
            pos = s[3]
            temp = num + ',' + speaker + ',' + word + ',' + wordplus + ',' + pos
            lines2.append(temp)




        header = 'Turn,' + 'Speaker,' + 'Word,' + 'WordPlus,' + 'POS' + '\n'
        data = ''.join(lines2)
        output = header + data


        filename = pathout + file[:-4] + '.csv'
        with open(filename, 'a+') as newfile:
            newfile.write(output)
            newfile.close()
    except Exception as e:
        print(str(e) + ' in ' + file)
        
print('All done!')