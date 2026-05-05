import decode

d_mem = [0] * 32

address = None
index = None

def Mem(executed):
    global address
    global index

    address = executed["alu_result"]
    index = address // 4

#    print("Address: ", address)

    if decode.memWrite == 1:        # sw
        d_mem[index] = executed["rs2_val"]
#        print("Saved", executed["rs2_val"], "to address", hex(address))
        return {
            "mem_result": None,
            "rd": executed["rd"],
            "alu_result": executed["alu_result"]
        }

    elif decode.memRead == 1:       # lw
        value = d_mem[index]
#        print("Loaded", value, "from address", hex(address))
        return {
            "mem_result": value,    # fixed - actually return the loaded value
            "rd": executed["rd"],
            "alu_result": executed["alu_result"]
        }

    else:                           # all other instructions
        return {
            "mem_result": None,
            "rd": executed["rd"],
            "alu_result": executed["alu_result"]
        }