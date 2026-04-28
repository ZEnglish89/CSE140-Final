import decode
import fetch

alu_zero = 0    
branch_target = 0
jump_target = 0


def execute(decoded):
    global alu_zero
    global branch_target
    global jump_target

    r1 = decoded.get("rs1_val", 0)
    r2 = decoded.get("rs2_val", 0)
    alu_ctrl = decode.alu_ctrl
    imm = decoded.get("imm", 0)  # default to 0 if imm not present

    if decode.ALUsrc == 1:
        r2 = imm  
    else:
        r2 = decoded.get("rs2_val", 0)

    alu_operations = {
        "0000": lambda r1, r2: r1 & r2,  # AND
        "0001": lambda r1, r2: r1 | r2,  # OR
        "0010": lambda r1, r2: r1 + r2, # ADD
        "0110": lambda r1, r2: r1 - r2, # SUB
        "0111": lambda r1, r2: r1 < r2, # SLT
    }

    operation = alu_operations.get(alu_ctrl, lambda a, b: None)
    alu_result = operation(int(r1), int(r2))
    if alu_result == 0:
        alu_zero = 1
    else:
        alu_zero = 0

    branch_target = (int(imm) << 1) + (fetch.pc - 4)

    if decode.jumpReg == 1:
        jump_target = int(decoded.get("rs1_val", 0)) + int(imm)
    else:
        jump_target = (fetch.pc - 4) + int(imm)

    return {
    "alu_result": alu_result,
    "rs2_val": decoded.get("rs2_val", 0),  # mem needs this for sw
    "rd": decoded.get("rd", 0),           # writeback needs this
    "pc_plus_4": fetch.pc              # for JAL and JALR writeback
}

if __name__ == "__main__":
    instr = "00000000001100001000001010110011"
    decoded = decode.decode(instr)
    result = execute(decoded)
    print("Execute result:", result)

