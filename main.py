import fetch
import decode
import execute
import mem
import writeback


def load_instruction_memory():
    # Instruction memory is a list of 32-bit binary strings.
    filename = input("Enter the program file name to run: ")
    with open(filename, "r") as f:
        imem = [line.strip() for line in f.readlines()]
    return imem

def run_cpu(imem):
    # Branch state is passed into fetch on the next cycle.
    decode.rf[1] = 0x20   # x1 = 32
    decode.rf[2] = 0x5    # x2 = 5
    decode.rf[10] = 0x70   
    decode.rf[11] = 0x4

    mem.d_mem[0x70 //4] = 0x5
    mem.d_mem[0x74 //4] = 0x10

    # decode.rf[8]  = 0x20   # s0
    # decode.rf[10] = 0x5    # a0
    # decode.rf[11] = 0x2    # a1
    # decode.rf[12] = 0xa    # a2
    # decode.rf[13] = 0xf    # a3
    # mem.d_mem = [0] * 32   # all zeros

    branch_taken = False
    branch_target = None
    jump = False
    jump_target = None


    while True:

        if fetch.pc // 4 >= len(imem) or fetch.pc < 0:
            break

        instruction = fetch.fetch(imem, branchTarget=branch_target, branchTaken=branch_taken, jumpTarget=jump_target, jump=jump)

        # Clear pending branch after it is consumed by fetch.
        branch_taken = False
        branch_target = None
        jump = False
        jump_target = None  

        print("\nFetched instruction:", instruction)

        decoded = decode.decode(instruction)
        if decoded is None:
            print("Stopping: unknown instruction")
            break

        print("Decoded output:", decoded)

        ex_result = execute.execute(decoded)
        print("DEBUG - decode.jump:", decode.jump, "jump_target:", execute.jump_target, "jump var:", jump)

        print("Execute output:", ex_result)

        if decode.memRead:
            mem_result = mem.Mem(ex_result) 
            mem_result["pc_plus_4"] = ex_result["pc_plus_4"]  
        elif decode.memWrite:
            mem_result = mem.Mem(ex_result)  # use return value directly
            mem_result["pc_plus_4"] = ex_result["pc_plus_4"]  # for JAL and JALR writeback
        else:
            mem_result = {
                "rd": ex_result["rd"],
                "alu_result": ex_result["alu_result"],
                "mem_result": None,
                "pc_plus_4": ex_result["pc_plus_4"],
            }

        writeback.WriteBack(mem_result)

        if decode.branch and execute.alu_zero:
            branch_target = execute.branch_target
            branch_taken = True
            print("Branch taken to address", branch_target)
        if decode.jump == 1:
            jump = True
            jump_target = execute.jump_target

        print("Register file after writeback:", decode.rf)

    print("\nProgram complete. final register file:", decode.rf)


if __name__ == "__main__":
    imem = load_instruction_memory()
    run_cpu(imem)
