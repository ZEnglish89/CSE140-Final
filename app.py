

binString = input("Enter an instruction:\n ")

d_mem = [0] * 32

total_clock_cycles = 0


opcode = binString[25:32]
print("Opcode:", opcode)

def binaryToDecimal(binStr):
    decVal = int(binStr, 2) #flatly convert right away
    if binStr[0] == '1':  # If we have a negative number, we need to adjust
        decVal -= (1 << len(binStr))  # subtract 2^n to get the correct negative value
    return str(decVal)

def handleRType():
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

def handleIType():
    imm = str(int(binString[0:12], 2))
    immDec = binaryToDecimal(binString[0:12])
    rs1 = str(int(binString[12:17],2))
    funct3 = binString[17:20]
    rd = str(int(binString[20:25],2))

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
    

def handleSType():
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

def handleSBType():
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

def handleUJType():
    #JAL is the only UJ instruction, but I figured it would be good to build out
    #the same structure regardless. It's only a few more lines, and it
    #makes this match the rest of the program.
    imm = str(int(binString[0:12], 2))
    immDec = binaryToDecimal(binString[0:12])
    rd = str(int(binString[20:25],2))

#00000000101000000000 = 10 ??

    UJOperations = {
        "1101111" : "JAL"
    }

    operation = UJOperations.get(opcode, "Unknown UJ-Type operation")

    print("Instruction Type: UJ")
    print("Operation: ", operation)
    print("rd: x"+ rd)
    print("Immediate: "+ immDec+"(or "+ hex(int(imm)) +")")

#assuming that address comes in as an int rather than as a hex string. If it does instead come in as a hex string,
#that's an easy adjustment. However, our existing decoding work from HW3 turns everything into decimal ints,
#so this is a safe bet.

#Inputs: address (int which is a multiple of 4), value (int, optional, only for store instructions)
#Outputs: For store instructions, no output. For load instructions, returns value loaded from memory (int).
def Mem(address, value = None):
    print("Memory: ", d_mem)

    print("Address: ", address)
    print("Value: ", value)

    index = int(address/4)

    if value is not None:

        d_mem[index] = value

        print("Saved value ", value, " to address ", address, "which corresponds to index ", index, "in the memory array.")
        print("Memory: ", d_mem)

        return None
    
    else:

        value = d_mem[index]

        print("Loaded value ", value, " from address ", address, "which corresponds to index ", index, "in the memory array.")
        
        return value

#inputs: register (int, as index of register file), value (int, regardless of where it came from)
#outputs: none, but register file is written into and total clock cycles is incremented.
#register is only actually written to if RegWrite is true, which is a global variable set by ControlUnit().
#rf is a global variable containing all register values.
#neither global variable exists at the time of writing.
def WriteBack(register=None, value=None):

    if RegWrite:
        print("Write Back: Register x"+ register + " gets value " + str(value))

        rf[register] = value

    total_clock_cycles += 1


switcher = {
    "0110011": handleRType,
    "0010011": handleIType,
    "0100011": handleSType,
    "1100011": handleSBType,
    "1101111": handleUJType,
    "1100111": handleIType,
    "0000011": handleIType
}

switcher.get(opcode, lambda: print("Unknown instruction type"))()