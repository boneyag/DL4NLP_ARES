
def find_collacation_senses(input_sense):
    """
    Find collacated senese for a given sense.
    """
    # process input to a format that can be searched in syntagnet
    (lemma, sense_id_pos) = input_sense.split(' ')
    
    # syntagnet sense id has 
    if len(sense_id_pos) <10:
        padding = '0' * (10 - len(sense_id_pos))
        sense_id_pos = padding + sense_id_pos
        
    syntag_senseid = sense_id_pos.replace('-', '')
    
    # print('{} {}'.format(syntag_senseid, lemma))
    
    # find matches in syntagnet
    
    collocated_senses = []
    with open('../data/resources/SYNTAGNET_1.0.txt') as syntagnet:
        
        # skip the top two lines of the text file
        # line 1 is the description and licensing
        # line 2 is blank
        
        next(syntagnet)
        next(syntagnet)
        
        lines = syntagnet.readlines()
        
        for line in lines:
            (s_id1, s_id2, l1, pos1, l2, pos2) = line.split('\t')
            # print('{} {} {} {} {} {}'.format(s_id1, s_id2, l1, pos1, l2, pos2))
            if syntag_senseid == s_id1:
                wn_sense_id = int(s_id2[:-1])
                wn_word_type = s_id2[-1]
                collocated_senses.append((wn_sense_id, wn_word_type, l2))
                # print('{} {}'.format(temp_sense_id, l2))
                
            elif syntag_senseid == s_id2:
                wn_sense_id = int(s_id1[:-1])
                wn_word_type = s_id1[-1]
                collocated_senses.append((wn_sense_id, wn_word_type, l1))
                # print('{} {}'.format(temp_sense_id, l1))
    
    collocated_senses = list(set(collocated_senses))
    return collocated_senses        

def main():
    collocated_senses = find_collacation_senses('glass 14881303-n')
    
    with open('../data/glass_14881303n_syntag_senses.txt', 'w') as f:
            f.write('\n'.join('%d %s %s' % x for x in collocated_senses))
    
if __name__ == '__main__':
    main()