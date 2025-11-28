# 5-Stage Pipelined RISC-V Processor Design

## Pipeline Stages

### 1. IF (Instruction Fetch)
- **Input**: Program Counter (PC)
- **Operations**: 
  - Fetch instruction from instruction memory at address PC
  - Increment PC by 4 (PC = PC + 4)
- **Output**: Instruction, PC+4
- **Register**: IF/ID Pipeline Register

### 2. ID (Instruction Decode)
- **Input**: Instruction from IF/ID register
- **Operations**:
  - Decode instruction (opcode, rs1, rs2, rd, immediate)
  - Read register file (rs1, rs2)
  - Generate control signals
- **Output**: Register values, control signals, immediate
- **Register**: ID/EX Pipeline Register

### 3. EX (Execute)
- **Input**: Operands and control signals from ID/EX register
- **Operations**:
  - ALU computation (add, sub, compare)
  - Branch target calculation
  - Address calculation for memory operations
- **Output**: ALU result, branch decision
- **Register**: EX/MEM Pipeline Register

### 4. MEM (Memory Access)
- **Input**: ALU result from EX/MEM register
- **Operations**:
  - Read from data memory (LW)
  - Write to data memory (SW)
  - Pass through for non-memory instructions
- **Output**: Memory data or ALU result
- **Register**: MEM/WB Pipeline Register

### 5. WB (Write Back)
- **Input**: Data from MEM/WB register
- **Operations**:
  - Write result to register file (if needed)
- **Output**: Updates register file
