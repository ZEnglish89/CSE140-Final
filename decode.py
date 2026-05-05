from fetch import fetch

rf = [0] * 32

#control signals
regWrite = 0
memRead = 0
memWrite = 0
ALUsrc = 0
memToReg = 0    
branch = 0
ALUop = "00"
alu_ctrl = "0000"
jump = 0        # 1 for JAL and JALR, tells fetch to always jump
jumpReg = 0     # 1 for JALR only, tells execute to use rs1+imm instead of pc+imm


def controlUnit(opcode, funct3=None, funct7=None):
    global regWrite, memRead, memWrite, ALUsrc, memToReg, branch, ALUop, alu_ctrl, jump, jumpReg

    jump = 0
    jumpReg = 0

    if opcode == "0110011":     # R-Type
        regWrite = 1
        memRead = 0
        memWrite = 0
        ALUsrc = 0
        memToReg = 0
        branch = 0
        ALUop = "10"
    elif opcode == "0010011":   # I-Type
        regWrite = 1
        memRead = 0
        memWrite = 0
        ALUsrc = 1
        memToReg = 0
        branch = 0
        ALUop = "10"
    elif opcode == "0000011":   # lw
        regWrite = 1
        memRead = 1
        memWrite = 0
        ALUsrc = 1
        memToReg = 1
        branch = 0
        ALUop = "00"
    elif opcode == "0100011":   # sw
        regWrite = 0
        memRead = 0
        memWrite = 1
        ALUsrc = 1
        memToReg = 0
        branch = 0
        ALUop = "00"
    elif opcode == "1100011":   # beq
        regWrite = 0
        memRead = 0
        memWrite = 0
        ALUsrc = 0
        memToReg = 0
        branch = 1
        ALUop = "01"
    elif opcode == "1101111":   # JAL
        regWrite = 1    # writes return address to rd
        memRead = 0
        memWrite = 0
        ALUsrc = 0
        memToReg = 0
        branch = 0
        ALUop = "00"
        jump = 1        
        jumpReg = 0     # jump target is pc + imm
    elif opcode == "1100111":   # JALR
        regWrite = 1    # writes return address to rd
        memRead = 0
        memWrite = 0
        ALUsrc = 1      # uses immediate
        memToReg = 0
        branch = 0
        ALUop = "00"
        jump = 1        
        jumpReg = 1     # jump target is rs1 + imm

    aluControl(ALUop, funct3, funct7)


def aluControl(ALUop, funct3, funct7):
    global alu_ctrl
    if ALUop == "00":
        alu_ctrl = "0010"       # lw/sw always ADD
    elif ALUop == "01":
        alu_ctrl = "0110"       # beq always SUB
    elif ALUop == "10":
        if funct7 is None:      # I-type, no funct7
            if funct3 == "000":
                alu_ctrl = "0010"   # ADDI
            elif funct3 == "111":
                alu_ctrl = "0000"   # ANDI
            elif funct3 == "110":
                alu_ctrl = "0001"   # ORI
        else:                   
            if funct3 == "000" and funct7 == "0000000":
                alu_ctrl = "0010"   # ADD
            elif funct3 == "000" and funct7 == "0100000":
                alu_ctrl = "0110"   # SUB
            elif funct3 == "111":
                alu_ctrl = "0000"   # AND
            elif funct3 == "110":
                alu_ctrl = "0001"   # OR  



def binaryToDecimal(binStr):
    decVal = int(binStr, 2) #flatly convert right away
    if binStr[0] == '1':  # If we have a negative number, we need to adjust
        decVal -= (1 << len(binStr))  # subtract 2^n to get the correct negative value
    return str(decVal)

def handleRType(binString):
    funct7 = binString[0:7]
    rs2 = str(int(binString[7:12],2))
    rs1 = str(int(binString[12:17],2))
    funct3 = binString[17:20]
    rd = str(int(binString[20:25],2))

    ROperations = {
        "0000000000" : "ADD",
        "1110000000" : "AND",
        "1100000000" : "OR",
        "0010000000" : "SLL",
        "0100000000" : "SLT",
        "0110000000" : "SLTU",
        "1010100000" : "SRA",
        "1010000000" : "SRL",
        "0000100000" : "SUB",
        "1000000000" : "XOR",
    }

    operation = ROperations.get(funct3 + funct7, "Unknown R-Type operation")

    funct3 = str(int(funct3, 2))
    funct7 = str(int(funct7, 2))

    print("Instruction Type: R")
    print("Operation: ", operation)
    print("rs1: x"+ rs1)
    print("rs2: x"+ rs2)
    print("rd: x"+ rd)
    print("funct3: "+ funct3)
    print("funct7: "+ funct7)

    rs1Val = rf[int(rs1)]
    rs2Val = rf[int(rs2)]

    return {
        "type": "R", "operation": operation,
        "rs1": rs1, "rs2": rs2, "rd": rd,
        "rs1_val": rs1Val, "rs2_val": rs2Val
    }

def handleIType(binString):
    imm = str(int(binString[0:12], 2))
    immDec = binaryToDecimal(binString[0:12])
    rs1 = str(int(binString[12:17],2))
    funct3 = binString[17:20]
    rd = str(int(binString[20:25],2))
    opcode = binString[25:32]

    IOperations = {
        "1100111000" : "JALR",
        "0000011000" : "LB",
        "0000011001" : "LH",
        "0000011010" : "LW",
        "0010011111" : "ANDI",
        "0010011000" : "ADDI",
        "0010011110" : "ORI",
        "0010011010" : "SLTI",
        "0010011011" : "SLTIU",
        "0010011100" : "XORI",
        "0010011001" : "SLLI",
        "0010011101" : "SRLI"
    }

    operation = IOperations.get(opcode + funct3, "Unknown I-Type operation")

    #there's only one operation here where we actually need the pseudofield of funct7.
    if operation == "SRLI" and binString[0:7] == "0100000":
        operation = "SRAI"

    funct3 = str(int(funct3, 2))


    print("Instruction Type: I")
    print("Operation: ", operation)
    print("rs1: x"+ rs1)
    print("rd: x"+ rd)
    print("Immediate: "+ immDec+"(or "+ hex(int(imm)) +")")

    rs1_val = rf[int(rs1)]

    return {
        "type": "I", "operation": operation,
        "rs1": rs1, "rd": rd, "imm": imm,
        "rs1_val": rs1_val
    }
    

def handleSType(binString):
    imm = str(int(binString[0:7] + binString[20:25], 2))
    immDec = binaryToDecimal(binString[0:7] + binString[20:25])
    rs2 = str(int(binString[7:12],2))
    rs1 = str(int(binString[12:17],2))
    funct3 = binString[17:20]

    SOperations = {
        "000" : "SB",
        "001" : "SH",
        "010" : "SW",
        "011" : "SD"
    }

    operation = SOperations.get(funct3, "Unknown S-Type operation")

    funct3 = str(int(funct3, 2))

    print("Instruction Type: S")
    print("Operation: ", operation)
    print("rs1: x"+ rs1)
    print("rs2: x"+ rs2)
    print("Immediate: "+ immDec+"(or "+ hex(int(imm)) +")")

    return {
        "type": "S", "operation": operation,
        "rs1": rs1, "rs2": rs2, "imm": imm,
        "rs1_val": rf[int(rs1)], "rs2_val": rf[int(rs2)]
    }

def handleSBType(binString):
    imm = str(int(binString[0:7] + binString[20:25], 2))
    immDec = binaryToDecimal(binString[0:7] + binString[20:25])
    rs2 = str(int(binString[7:12],2))
    rs1 = str(int(binString[12:17],2))
    funct3 = binString[17:20]

    SBOperations = {
        "000" : "BEQ",
        "001" : "BNE",
        "100" : "BLT",
        "101" : "BGE"
    }

    operation = SBOperations.get(funct3, "Unknown SB-Type operation")

    funct3 = str(int(funct3, 2))

    print("Instruction Type: SB")
    print("Operation: ", operation)
    print("rs1: x"+ rs1)
    print("rs2: x"+ rs2)
    print("Immediate: "+ immDec+"(or "+ hex(int(imm)) +")")

    return {
        "type": "SB", "operation": operation,
        "rs1": rs1, "rs2": rs2, "imm": imm,
        "rs1_val": rf[int(rs1)], "rs2_val": rf[int(rs2)]
    }

def handleUJType(binString):
    #JAL is the only UJ instruction, but I figured it would be good to build out
    #the same structure regardless. It's only a few more lines, and it
    #makes this match the rest of the program.
    rd = str(int(binString[20:25],2))
    opcode = binString[25:32]

    # UJ immediate is encoded as imm[20|10:1|11|19:12] followed by a zero bit.
    imm_raw = binString[0] + binString[12:20] + binString[11] + binString[1:11] + "0"
    imm = binaryToDecimal(imm_raw)
    immDec = imm

    UJOperations = {
        "1101111" : "JAL"
    }

    operation = UJOperations.get(opcode, "Unknown UJ-Type operation")

    print("Instruction Type: UJ")
    print("Operation: ", operation)
    print("rd: x"+ rd)
    print("Immediate: "+ immDec+"(or "+ hex(int(imm)) +")")

    return {
        "type": "UJ", "operation": "JAL",
        "rd": rd, "imm": imm
    }


def decode(binString):
    global rf
    opcode = binString[25:32]
    funct3 = binString[17:20]
    funct7 = binString[0:7] if opcode == "0110011" else None

    controlUnit(opcode, funct3, funct7) 

    if opcode == "0110011":      # R-type
        return handleRType(binString)
    elif opcode in ("0010011", "1100111", "0000011"):  # I-type
        return handleIType(binString)
    elif opcode == "0100011":    # S-type
        return handleSType(binString)
    elif opcode == "1100011":    # SB-type
        return handleSBType(binString)
    elif opcode == "1101111":    # UJ-type
        return handleUJType(binString)
    else:
        print("Unknown instruction type")
        return None


# switcher = {
#     "0110011": handleRType,
#     "0010011": handleIType,
#     "0100011": handleSType,
#     "1100011": handleSBType,
#     "1101111": handleUJType,
#     "1100111": handleIType,
#     "0000011": handleIType
# }

# switcher.get(opcode, lambda: print("Unknown instruction type"))()