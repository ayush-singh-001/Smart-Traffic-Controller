# RISC-V ISA Specification for Smart Traffic Signal Controller

## Traffic Controller Algorithm (High-Level)

1. Read vehicle count from sensor (North-South direction)
2. Read vehicle count from sensor (East-West direction)
3. Check emergency override button
4. If emergency: Set all lights to RED
5. Else: Compare traffic density and set priority direction
6. Execute light sequence for priority direction
7. Log traffic data to memory
8. Repeat

## Required Instructions (Minimal Subset)

### Memory Access
- **LW** (Load Word): `lw rd, offset(rs1)` - Read sensor data or memory
- **SW** (Store Word): `sw rs2, offset(rs1)` - Write to output or log

### Arithmetic & Logic
- **ADDI** (Add Immediate): `addi rd, rs1, imm` - Increment counters, compute addresses
- **ADD** (Add): `add rd, rs1, rs2` - Arithmetic operations
- **SUB** (Subtract): `sub rd, rs1, rs2` - Compare values

### Branching
- **BEQ** (Branch if Equal): `beq rs1, rs2, label` - Conditional logic
- **BLT** (Branch if Less Than): `blt rs1, rs2, label` - Compare traffic density
- **JAL** (Jump and Link): `jal rd, label` - Function calls, loops

### Special
- **NOP** (No Operation): For pipeline testing

## Instruction Formats

### R-Type (Register)
```
| funct7 (7) | rs2 (5) | rs1 (5) | funct3 (3) | rd (5) | opcode (7) |
```
- Used by: ADD, SUB

### I-Type (Immediate)
```
| imm[11:0] (12) | rs1 (5) | funct3 (3) | rd (5) | opcode (7) |
```
- Used by: ADDI, LW

### S-Type (Store)
```
| imm[11:5] (7) | rs2 (5) | rs1 (5) | funct3 (3) | imm[4:0] (5) | opcode (7) |
```
- Used by: SW

### B-Type (Branch)
```
| imm[12,10:5] (7) | rs2 (5) | rs1 (5) | funct3 (3) | imm[4:1,11] (5) | opcode (7) |
```
- Used by: BEQ, BLT

### J-Type (Jump)
```
| imm[20,10:1,11,19:12] (20) | rd (5) | opcode (7) |
```
- Used by: JAL

## Performance Characteristics
- Total Instructions: 9 unique opcodes
- Memory Operations: LW, SW (2)
- Control Flow: BEQ, BLT, JAL (3)
- Arithmetic: ADD, SUB, ADDI (3)
