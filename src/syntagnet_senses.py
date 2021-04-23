
def get_collocated_senses(input_offset):
    """
    Find collacated senese for a given offset.
    """
    
    
    # syntagnet sense id length is 9. Add paddings to the front
    if len(input_offset) <9:
        padding = '0' * (9 - len(input_offset))
        sense_id_pos = padding + input_offset
        
    syntag_senseid = input_offset.replace('-', '')
    
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
            if syntag_senseid == s_id1:
                wn_sense_id = int(s_id2[:-1])
                wn_word_type = s_id2[-1]
                collocated_senses.append((wn_sense_id, wn_word_type, l2))
                
            elif syntag_senseid == s_id2:
                wn_sense_id = int(s_id1[:-1])
                wn_word_type = s_id1[-1]
                collocated_senses.append((wn_sense_id, wn_word_type, l1))
    
    collocated_senses = list(set(collocated_senses))
    return collocated_senses 