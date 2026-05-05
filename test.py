from fetch import fetch
from decode import decode, rf

# This is an ADDI instruction: addi x3, x1, 5
test_instructions = [
    "00000000010100001000000110010011",  # addi x3, x1, 5  (I-type)
    "00000000001100001000001010110011",  # add  x5, x1, x3 (R-type)
]

rf[1] = 0x20   # x1 = 32
rf[2] = 0x5    # x2 = 5

# Run through each instruction
for i in range(len(test_instructions)):
    print(f"\n--- Cycle {i+1} ---")
    instruction = fetch(test_instructions)
    result = decode(instruction)
    print("Decoded result:", result)