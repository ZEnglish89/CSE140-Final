import decode
import mem
import fetch
total_clock_cycles = 0

def WriteBack(mem_result):
    global total_clock_cycles
    rd = int(mem_result["rd"])

    total_clock_cycles += 1
    print(f"\ntotal_clock_cycles {total_clock_cycles} :")

    if decode.regWrite == 1 and rd != 0: 
        if decode.jump == 1:
            value = mem_result["pc_plus_4"]
        elif decode.memToReg == 1:
            value = mem_result["mem_result"]
        else:
            value = mem_result["alu_result"]

        decode.rf[rd] = value
        print(f"{decode.rfNames[rd]} is modified to {hex(value)}")

    if decode.memWrite == 1 and mem.address != None:
        print("memory " + str(hex(mem.address)) + " is modified to " + str(hex(mem.d_mem[mem.index])))

   

    

