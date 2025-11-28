# Hazard Handling Report

## 1. Data Hazards (RAW - Read After Write)

### Example from Traffic Controller:
```
addi x1, x0, 5      # Instruction 1: Write to x1
add x2, x1, x3      # Instruction 2: Read x1 (hazard!)
```

### Solutions Implemented:

#### a) Forwarding (Bypassing)
- Forward ALU result from EX/MEM register to EX stage
- Forward memory data from MEM/WB register to EX stage
- **Reduces stalls from 2 cycles to 0 cycles** for ALU-to-ALU dependencies

#### b) Load-Use Stall
- If instruction needs data from a load (LW) in previous cycle, **stall 1 cycle**
```
lw x1, 0(x10)       # Load x1 from memory
add x2, x1, x3      # Needs x1: STALL 1 cycle required
```

## 2. Control Hazards (Branches)

### Example from Traffic Controller:
```
beq x3, x4, emergency_mode    # Branch decision in EX stage
addi x5, x0, 0x00             # Next instruction (may be flushed)
```

### Solutions Implemented:

#### Branch Prediction: Predict Not Taken
- Assume branch is NOT taken
- Fetch next sequential instruction
- If prediction wrong: **Flush 2 instructions, 2-cycle penalty**

#### Branch Resolution in EX Stage
- Calculate branch target and condition in EX stage (cycle 3)
- Instructions in IF and ID stages must be flushed if branch taken

## 3. Structural Hazards

### Solution: Separate Instruction and Data Memory
- Harvard architecture: separate I-cache and D-cache
- No structural hazards in our design

## 4. Hazard Impact on Traffic Controller Code

### Analysis of One Control Loop Iteration (21 instructions)

| Hazard Type | Location | Stall/Flush Cycles |
|-------------|----------|-------------------|
| Load-Use | lw x1 → blt x1, x2 | 1 stall |
| Branch Taken | blt (if taken) | 2 flushes |
| Branch Taken | jal (always) | 2 flushes |

### Performance Calculation (One Iteration):
- **Ideal CPI**: 1.0 (perfect pipeline)
- **Instruction Count**: 21 instructions
- **Stalls**: 1 (load-use) = 1 cycle
- **Flushes**: 2 + 2 (branches/jumps) = 4 cycles
- **Total Cycles**: 21 + 1 + 4 = 26 cycles
- **Real CPI**: 26 / 21 = **1.24**

### Forwarding Effectiveness:
- Without forwarding: +6 additional stalls for data dependencies
- With forwarding: Only 1 load-use stall
- **Improvement**: 6 cycles saved per iteration
