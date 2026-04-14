pc = 0

def fetch(imem, branchTarget=None, branchTaken=False):
    global pc

    instruction = imem[pc // 4]
    next_pc = pc + 4
    if branchTaken and branchTarget is not None:
        pc = branchTarget
    else:
        pc = next_pc

    return instruction
    