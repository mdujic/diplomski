import uuid

class Consts():
    EPSILON = "$"

priority = {'*': 3, '?': 2, '+': 1}

def is_alphabet(c):
    return c not in priority.keys() and c not in ['(', ')']

def add_concat_symbol(reg_exp):
    '''
    Replace 'and' operation with ? symbol
    '''
    new_reg_exp = ""
    for current_char in reg_exp:
        if(len(new_reg_exp)>0):
            prev_char = new_reg_exp[len(new_reg_exp)-1]
            if (prev_char == ')' or is_alphabet(prev_char) or prev_char == '*') and (current_char == '('  or is_alphabet(current_char)):
                new_reg_exp += "?"
        new_reg_exp += current_char
    return new_reg_exp

def regex_to_postfix(reg_exp):
    postfix_exp=""
    operator_stack = []

    reg_exp = add_concat_symbol(reg_exp)
    
    # shunting yard algorithm
    for current_char in reg_exp:
        if is_alphabet(current_char):
            postfix_exp += current_char
        elif current_char == '(':
            operator_stack.append(current_char)
        elif current_char == ')':
            top = operator_stack.pop()
            while top != '(':
                postfix_exp += top
                top = operator_stack.pop()
        else:
            if len(operator_stack) == 0:
                operator_stack.append(current_char)
            else:
                top = operator_stack[len(operator_stack)-1]
                while top!='(' and priority[top] >= priority[current_char]:
                    postfix_exp += top 
                    operator_stack.pop()
                    if len(operator_stack) > 0:
                        top = operator_stack[len(operator_stack)-1]
                    else:
                        break
                operator_stack.append(current_char)
    while len(operator_stack) != 0:
        postfix_exp += operator_stack.pop()

    return postfix_exp


def get_alphabet_nfa(character, alphabets):
    nfa = {}
    nfa["states"] = [uuid.uuid4(), uuid.uuid4()]
    nfa["initial_state"] = nfa["states"][0]
    nfa["final_states"] = [nfa["states"][1]]
    nfa["alphabets"] = alphabets
    nfa["transition_function"]= {}
    for state in nfa["states"]:
        nfa["transition_function"][state] = {}
        for alphabet in nfa["alphabets"]:
            nfa["transition_function"][state][alphabet] = []
    nfa["transition_function"][nfa["initial_state"]][character] = nfa["final_states"] 
    return nfa

def concat_nfa(nfa1, nfa2):
    nfa = {}

    nfa["states"] = []
    nfa["states"].extend(nfa1["states"])
    nfa["states"].extend(nfa2["states"])

    nfa["initial_state"] = nfa1["initial_state"]
    nfa["final_states"] = nfa2["final_states"]
    nfa["alphabets"] = list(set(nfa1["alphabets"]) | set(nfa2["alphabets"]))

    nfa["transition_function"]= {}
    for state in nfa["states"]:
        if state in nfa1["states"]:
            nfa["transition_function"][state] = nfa1["transition_function"][state]
        elif state in nfa2["states"]:
            nfa["transition_function"][state] = nfa2["transition_function"][state]

    # connect final states of nfa1 with start state of nfa2 using epsilon transition
    for state in nfa1["final_states"]:
        nfa["transition_function"][state][Consts.EPSILON].append(nfa2["initial_state"])

    return nfa

def union_nfa(nfa1, nfa2):
    nfa = {}

    nfa["states"] = [uuid.uuid4()]
    nfa["states"].extend(nfa1["states"])
    nfa["states"].extend(nfa2["states"])

    nfa["initial_state"] = nfa["states"][0]
    nfa["final_states"] = []
    nfa["final_states"].extend(nfa1["final_states"])
    nfa["final_states"].extend(nfa2["final_states"])
    nfa["alphabets"] = list(set(nfa1["alphabets"]) | set(nfa2["alphabets"]))

    nfa["transition_function"]= {}
    for state in nfa["states"]:
        if state in nfa1["states"]:
            nfa["transition_function"][state] = nfa1["transition_function"][state]
        elif state in nfa2["states"]:
            nfa["transition_function"][state] = nfa2["transition_function"][state]
        else:
            nfa["transition_function"][state] = {}
            for alphabet in nfa["alphabets"]:
                nfa["transition_function"][state][alphabet] = []
    
    # connecting start state to start state of nfa 1 and nfa 2 through epsilon move
    nfa["transition_function"][nfa["initial_state"]][Consts.EPSILON].extend([nfa1["initial_state"], nfa2["initial_state"]])
    return nfa

def cleene_star_nfa(nfa1):
    nfa = {}

    nfa["states"] = [uuid.uuid4()]
    nfa["states"].extend(nfa1["states"])
    nfa["states"].append(uuid.uuid4())

    nfa["initial_state"] = nfa["states"][0]
    nfa["final_states"] = [nfa["states"][  len(nfa["states"])-1 ]]
    nfa["alphabets"] =  nfa1["alphabets"]
    
    nfa["transition_function"]= {}
    for state in nfa["states"]:
        if state in nfa1["states"]:
            nfa["transition_function"][state] = nfa1["transition_function"][state]
        else:
            nfa["transition_function"][state] = {}
            for alphabet in nfa["alphabets"]:
                nfa["transition_function"][state][alphabet] = []

    # connecting start state to start state of nfa 1 through epsilon move
    nfa["transition_function"][nfa["initial_state"]][Consts.EPSILON].append(nfa1["initial_state"])

    for final_state in nfa1["final_states"]:
        # connecting final states of nfa1 to start state of nfa1 through epsilon move
        nfa["transition_function"][final_state][Consts.EPSILON].append(nfa1["initial_state"])
        # connecting final states of nfa1 to final states of nfa through epsilon move
        nfa["transition_function"][final_state][Consts.EPSILON].extend(nfa["final_states"])

    # connecting start state to final state of nfa through epsilon move
    nfa["transition_function"][nfa["initial_state"]][Consts.EPSILON].extend(nfa["final_states"])
    return nfa
    
def regex_to_nfa(reg_exp):
    postfix_exp = regex_to_postfix(reg_exp)
    
    nfa_stack = []
    alphabets = []
    for character in postfix_exp:
        if is_alphabet(character):
            if character not in alphabets:
                alphabets.append(character)
    if Consts.EPSILON not in alphabets:
        alphabets.append(Consts.EPSILON)
    for character in postfix_exp:
        if is_alphabet(character):
            nfa_stack.append(get_alphabet_nfa(character, alphabets))
        elif character == "?": # concat
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa_stack.append(concat_nfa(nfa1, nfa2))
        elif character == "+": # union
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa_stack.append(union_nfa(nfa1, nfa2))
        elif character == "*": # cleene star
            nfa1 = nfa_stack.pop()
            nfa_stack.append(cleene_star_nfa(nfa1))
    nfa = nfa_stack.pop()
    return nfa