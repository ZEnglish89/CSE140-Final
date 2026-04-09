Simulation of a RISC-V CPU in Python(C++ was considered by Python is being used as of writing).

Takes in RISC-V instructions via .txt file or similar, uses files of its own to simulate registers, PC values, and similar components of the Assembly language.

When complete, capable of handling `lw, sw, add, addi, sub, and, andi, or, ori, beq, jal, jalr`.

Optionally handles five-stage pipelining, using stages `if, id, ex, mem, wb` and stalling properly when necessary data is unavailable/there are conflicts.
Does not handle data forwarding or branch prediction, though stage register files to potentially include forwarding at some future point are included.
