pc = 0

def fetch(imem, branchTarget=None, branchTaken=False, jumpTarget=None, jump=False):
    global pc
    
#    print(f"FETCH DEBUG - pc={pc}, jump={jump}, jumpTarget={jumpTarget}")
    
    if jump and jumpTarget is not None:
        pc = jumpTarget
    elif branchTaken and branchTarget is not None:
        pc = branchTarget
    
    instruction = imem[pc // 4]
    pc = pc + 4

    
    

#    print(f"FETCH DEBUG - pc after={pc}")
    return instruction
    