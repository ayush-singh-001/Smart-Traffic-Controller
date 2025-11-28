# 5-Stage Pipelined RISC-V Datapath - Visual Documentation

## Pipeline Overview

```
graph LR
    A[IF: Instruction Fetch] --> B[ID: Instruction Decode]
    B --> C[EX: Execute]
    C --> D[MEM: Memory Access]
    D --> E[WB: Write Back]
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#ffe1e1
    style D fill:#e1ffe1
    style E fill:#f0e1ff
```

---

## Stage-by-Stage Breakdown

### Stage 1: Instruction Fetch (IF)

| Component | Function | Details |
|-----------|----------|---------|
| **Program Counter (PC)** | Holds current instruction address | 32-bit register |
| **I-Cache** | Fetches instruction from memory | 16KB, direct-mapped, 64B blocks |
| **Adder** | Calculates PC+4 | Sequential instruction address |
| **IF/ID Register** | Stores fetched instruction | Pipeline register |

**Data Flow:**
```
PC → I-Cache → Instruction → IF/ID Register
PC → Adder (+4) → Next PC
```

---

### Stage 2: Instruction Decode (ID)

| Component | Function | Details |
|-----------|----------|---------|
| **Control Unit** | Generates control signals | RegWrite, MemRead, MemWrite, ALUOp, Branch |
| **Register File** | Reads source registers | 32 registers (x0-x31), dual read ports |
| **Immediate Generator** | Extracts/extends immediate | Handles I, S, B, J formats |
| **Hazard Detection Unit** | Detects load-use hazards | Inserts stalls when needed |

**Control Signals Generated:**
- RegWrite, MemToReg, MemRead, MemWrite
- ALUSrc, ALUOp[1:0], Branch, Jump

**Data Flow:**
```
Instruction → Control Unit → Control Signals
Instruction[19:15] → Register File (rs1) → ReadData1
Instruction[24:20] → Register File (rs2) → ReadData2
Instruction → Immediate Generator → Immediate Value
All data → ID/EX Register
```

---

### Stage 3: Execute (EX)

| Component | Function | Details |
|-----------|----------|---------|
| **ALU (64-bit)** | Performs arithmetic/logic ops | ADD, SUB, AND, OR, SLT, shifts |
| **Forwarding Unit** | Resolves data hazards | Forwards from EX/MEM and MEM/WB |
| **Branch Unit** | Calculates branch target | PC + Immediate |
| **Comparator** | Branch condition check | Zero flag, Less-than flag |

**Forwarding Logic:**
```
if (EX/MEM.RegWrite && EX/MEM.Rd == ID/EX.rs1)
    ForwardA = EX/MEM.ALUResult

if (MEM/WB.RegWrite && MEM/WB.Rd == ID/EX.rs1)
    ForwardA = MEM/WB.Result
```

**Data Flow:**
```
ReadData1 → Forwarding MUX → ALU Input A
ReadData2/Immediate → ALU Input B
ALU → ALUResult → EX/MEM Register
Branch condition → Flush signal (if taken)
```

---

### Stage 4: Memory (MEM)

| Component | Function | Details |
|-----------|----------|---------|
| **D-Cache** | Load/Store operations | 16KB, 2-way set associative, 64B blocks |
| **LRU Controller** | Cache replacement policy | Tracks least recently used way |
| **Write Buffer** | Handles write-back | Stores dirty cache blocks |

**Cache Operation:**
```
Address[31:6] → Tag comparison
Address[5:0] → Block offset
Hit → 1 cycle latency
Miss → 10 cycle penalty (fetch from main memory)
```

**Data Flow:**
```
ALUResult → D-Cache Address
WriteData → D-Cache (if MemWrite)
D-Cache → ReadData → MEM/WB Register
```

---

### Stage 5: Write Back (WB)

| Component | Function | Details |
|-----------|----------|---------|
| **Result MUX** | Selects write-back data | ALUResult or MemData |
| **Register File (Write Port)** | Updates destination register | Single write port |

**Data Flow:**
```
if (MemToReg):
    WriteData = MemData
else:
    WriteData = ALUResult

if (RegWrite):
    RegisterFile[Rd] ← WriteData
```

---

## Hazard Handling Mechanisms

### 1. Data Hazards (Read-After-Write)

#### Forwarding Example
```
addi x1, x0, 5      # EX stage: x1 = 5
add  x2, x1, x3     # EX stage needs x1 → Forward from EX/MEM
```

**Solution:** Forward ALUResult from EX/MEM to EX stage  
**Penalty:** 0 cycles

#### Load-Use Hazard
```
lw   x1, 0(x10)     # MEM stage: x1 loaded
blt  x1, x2, label  # EX stage needs x1 → Cannot forward yet!
```

**Solution:** Stall pipeline 1 cycle, insert NOP bubble  
**Penalty:** 1 cycle

---

### 2. Control Hazards (Branches)

#### Predict Not Taken Strategy
```
beq x1, x2, target  # Branch resolved in EX (cycle 3)
addi x3, x3, 1      # Fetched at cycle 2 (IF stage)
addi x4, x4, 1      # Fetched at cycle 3 (IF stage)
```

**If branch NOT taken:** Continue normally (0 penalty)  
**If branch TAKEN:** Flush 2 instructions, fetch from target  
**Penalty:** 2 cycles (on taken branches)

---

## Pipeline Registers (Timing Diagrams)

### IF/ID Register
| Field | Bits | Purpose |
|-------|------|---------|
| PC+4 | 32 | Next sequential address |
| Instruction | 32 | Fetched instruction |

### ID/EX Register
| Field | Bits | Purpose |
|-------|------|---------|
| PC+4 | 32 | For branch target calculation |
| ReadData1 | 64 | Source register 1 value |
| ReadData2 | 64 | Source register 2 value |
| Immediate | 64 | Sign-extended immediate |
| Rd | 5 | Destination register |
| Control Signals | 9 | RegWrite, MemRead, MemWrite, etc. |

### EX/MEM Register
| Field | Bits | Purpose |
|-------|------|---------|
| BranchTarget | 32 | Calculated branch address |
| ALUResult | 64 | ALU computation result |
| WriteData | 64 | Data for store instructions |
| Rd | 5 | Destination register |
| Control Signals | 3 | MemWrite, MemRead, RegWrite |

### MEM/WB Register
| Field | Bits | Purpose |
|-------|------|---------|
| ReadData | 64 | Data loaded from memory |
| ALUResult | 64 | Passed from EX stage |
| Rd | 5 | Destination register |
| Control Signals | 2 | RegWrite, MemToReg |

---

## Performance Metrics (Traffic Controller)

### Instruction Mix (21 Instructions per Loop)
- **Loads (LW):** 3 (14.3%)
- **Stores (SW):** 3 (14.3%)
- **Arithmetic (ADD/SUB/ADDI):** 8 (38.1%)
- **Branches (BEQ/BLT):** 2 (9.5%)
- **Jumps (JAL):** 1 (4.8%)
- **Other:** 4 (19.0%)

### Cycle Breakdown
| Event | Count | Total Cycles |
|-------|-------|--------------|
| Base instructions | 21 | 21 |
| Load-use stall | 1 | +1 |
| Branch flushes (2 taken) | 2 × 2 | +4 |
| **Total** | - | **26 cycles** |

### Pipeline Efficiency
- **CPI (Cycles Per Instruction):** 26/21 = **1.24**
- **Ideal CPI:** 1.0
- **Pipeline Utilization:** 1.0/1.24 = **80.6%**
- **Stalls Prevented (via forwarding):** 6 cycles

---

## Visual Summary

```
Clock Cycle:  1    2    3    4    5    6    7    8
           ┌────┬────┬────┬────┬────┬────┬────┬────┐
Inst 1:    │ IF │ ID │ EX │MEM │ WB │    │    │    │
           ├────┼────┼────┼────┼────┼────┼────┼────┤
Inst 2:    │    │ IF │ ID │ EX │MEM │ WB │    │    │
           ├────┼────┼────┼────┼────┼────┼────┼────┤
Inst 3:    │    │    │ IF │ ID │ EX │MEM │ WB │    │
(LW)       ├────┼────┼────┼────┼────┼────┼────┼────┤
Inst 4:    │    │    │    │ IF │ ID │STALL│ EX │MEM │
(uses x1)  ├────┼────┼────┼────┼────┼────┼────┼────┤
           └────┴────┴────┴────┴────┴────┴────┴────┘
                              ↑
                        Load-use hazard
                        1-cycle stall inserted
```

---

## Critical Design Decisions

1. **Separate I-Cache and D-Cache** → Eliminates structural hazards
2. **Forwarding from EX/MEM and MEM/WB** → Reduces data hazard stalls by 75%
3. **Branch resolution in EX stage** → 2-cycle penalty (vs 3 if in MEM)
4. **LRU replacement in D-Cache** → 85.71% hit rate for traffic workload
5. **Write-back policy** → Reduces memory traffic for frequent log updates

---

**Diagram Created:** November 28, 2025  
**Traffic Controller Performance:** CPI = 1.24, 26 cycles/iteration
