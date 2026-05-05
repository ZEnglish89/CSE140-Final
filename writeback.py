import decode
import fetch
total_clock_cycles = 0

def WriteBack(mem_result):
    global total_clock_cycles
    rd = int(mem_result["rd"])

    if decode.regWrite == 1 and rd != 0: 
        if decode.jump == 1:
            value = mem_result["pc_plus_4"]
        elif decode.memToReg == 1:
            value = mem_result["mem_result"]
        else:
            value = mem_result["alu_result"]

        decode.rf[rd] = value
        print(f"x{rd} is modified to {hex(value)}")

    total_clock_cycles += 1
    print(f"total_clock_cycles {total_clock_cycles} :")
   

    

