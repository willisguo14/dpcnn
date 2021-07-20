import json
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

def print_json(data):
    print(json.dumps(data, indent=2))
def print_dict(my_dict):
    for key, value in my_dict.items():
        print(f"{key} => {value}\n")
    
    print("\n\n")

 
def get_token(node):

    tokens = []

    node_type = node["_label"]

    if node_type == "METHOD_PARAMETER_IN":
        tokens.append(node['typeFullName'])
        tokens.append(node['name'])

    elif node_type == "IDENTIFIER" or node_type == "LITERAL":
        tokens.append(node['typeFullName'])

    elif node_type == "CALL":
        tokens.append(node['name'])

    elif node_type == "METHOD":
        tokens.append(node['signature'])

    elif node_type == "CONTROL_STRUCTURE":
        tokens.append(node['controlStructureType'])

    elif node_type == "BLOCK":
        tokens.append(node['typeFullName'])

    elif node_type == "JUMP_TARGET":
        tokens.append(node['name'])

    return tokens

#! specific to NVD and SARD
def get_label(fname):
    if "VULN" in fname or "BAD" in fname:
        return 1
    else:
        return 0

def get_token_vec_and_freq(json_file, token_vec_dict, token_freq_dict):

    # token_vec_dict structure: key = filename, value = ([token_vec], label)
    # token_freq_dict structure: key = token, value = token_freq
    
    with open(json_file, 'r') as f:
        ast = json.load(f)
    
    
    cur_file = ""
    cur_vec = []
    cur_label = -1

    for node in ast:
        
        #* found a node with "filename" properties = start of a new 'block' 
        if "filename" in node.keys():

            #* add previous 'block'
            if cur_file and cur_vec and cur_label != -1:
                token_vec_dict[cur_file] = (cur_vec, cur_label)


            #* update cur_file, cur_vec, cur_label for new 'block'
            cur_file = node["filename"]

            # unseen source code file
            if cur_file not in token_vec_dict.keys():
                cur_vec = []
                cur_label = get_label(cur_file)
            # source code file seen before
            else:
                cur_vec, cur_label = token_vec_dict[cur_file]
        
        #* get appropriate token
        tokens = get_token(node)

        #* only if this node is 'selected' 
        if tokens:
            for token in tokens:
                #* append token
                cur_vec.append(token)

                #* update token_freq_dict
                token_freq_dict[token] = token_freq_dict.get(token, 0) + 1
    
    #* add last block after exiting for loop 
    if cur_file and cur_vec and cur_label != -1: 
        token_vec_dict[cur_file] = (cur_vec, cur_label)
    
    return token_vec_dict, token_freq_dict

def get_token_to_num_dict(token_freq_dict):

    token_to_num_dict = {}

    num = 1 

    for token, freq in token_freq_dict.items():
        
        if freq >= 3:
            token_to_num_dict[token] = num
            num += 1
    
    return token_to_num_dict, num


def token_to_num_vec(token_vec, token_to_num_dict):
    num_vec = [token_to_num_dict.get(token, 0) for token in token_vec]
    return num_vec

def get_num_vec(token_vec_dict, token_to_num_dict):

    num_vec_dict = {}

    for file, (token_vec, label) in token_vec_dict.items():
        num_vec = token_to_num_vec(token_vec, token_to_num_dict)
        num_vec_dict[file] = (num_vec, label)
    
    return num_vec_dict


def export_data(num_vec_dict, vocab_size):

    vecs = []
    labels = []

    for vec, label in num_vec_dict.values():
        vecs.append(vec)
        labels.append(label)
    
    #* pad vecs using tf 
    padded_vecs = pad_sequences(vecs, padding='post')

    #* get length of a sequence (i.e. input_length for embedding layer)
    input_len = np.shape(padded_vecs)[-1]

    #* convert labels list to np array 
    np_labels = np.asarray(labels)
    
    #* export to .npz file
    np.savez('data', vecs=padded_vecs, labels=np_labels, vocab_size=vocab_size, input_len=input_len)



if __name__ == "__main__":

    token_vec_dict = {}
    token_freq_dict = {}

    token_vec_dict, token_freq_dict = get_token_vec_and_freq('NVD.json', token_vec_dict, token_freq_dict)
    token_vec_dict, token_freq_dict = get_token_vec_and_freq('SARD_mixed.json', token_vec_dict, token_freq_dict)

    
    # print_dict(token_vec_dict)
    # print_dict(token_freq_dict)

    
    token_to_num_dict, vocab_size = get_token_to_num_dict(token_freq_dict)

    # print_dict(token_to_num_dict)
    print(f"VOCAB SIZE: {vocab_size}")

    
    num_vec_dict = get_num_vec(token_vec_dict, token_to_num_dict)

    # print_dict(num_vec_dict)
    print(f"NUMBER OF VECS: {len(num_vec_dict)}")

    export_data(num_vec_dict, vocab_size) 
