# returns list with: [num_types_MOT, num_types_CHI, num_types_shared, num_tokens_MOT, num_tokens_CHI]
def get_types_tokens(file):
    with open(file,'r') as f:

        removelist = ['\t', '\r']
        text = f.read()
        for item in removelist:
            text = text.replace(item, '')
            if '*FAT' in text:
                text = text.replace('*FAT', '*MOT')
                print('replaced FAT with MOT in ' + file)
            if '*AUN' in text:
                text = text.replace('*AUN', '*MOT')
                print('replaced AUN with MOT in ' + file)
        text = text.split('\n')

        # make seperate lists for MOT and CHI utterances
        utt_MOT = []
        utt_CHI = []
        for s, val in enumerate(text):
            if 'xxx' not in val:
                if val.startswith('*MOT'):
                    utt_MOT.append(val)
                if val.startswith('*CHI'):
                    utt_CHI.append(val) 

        # remove "*MOT:" and "*CHI:" and trailing punctuation
        removelist = ['*MOT', ' .', ' !', ' ?',',']
        for item in removelist:
            for s, val in enumerate(utt_MOT):
                val = val.replace(item, '')
            for s, val in enumerate(utt_CHI):
                val = val.replace(item, '')

        # join all MOT and CHI utterance into a string so we can split by words
        temp_MOT = ' '.join(utt_MOT)
        temp_CHI = ' '.join(utt_CHI)

        # find all the MOT and all the CHI tokens
        tokens_MOT = temp_MOT.split()
        tokens_CHI = temp_CHI.split()

        # find the set of MOT types and the set of CHI types
        types_MOT = set(tokens_MOT)
        types_CHI = set(tokens_CHI)

        # find the types shared by mother and child
        types_shared = types_MOT & types_CHI

        # calculate the number of types for MOT, CHI, and shared
        num_types_MOT = len(types_MOT)
        num_types_CHI = len(types_CHI)
        num_types_shared = len(types_shared)

        # calculate the number of tokens for MOT, CHI, and shared
        num_tokens_MOT = len(tokens_MOT)
        num_tokens_CHI = len(tokens_CHI)

        return[num_types_MOT, num_types_CHI, num_types_shared, num_tokens_MOT, num_tokens_CHI]


