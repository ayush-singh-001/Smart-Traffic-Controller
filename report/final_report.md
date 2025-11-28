# Smart Traffic Signal Controller
## Computer Architecture Design Project

**Course**: Computer Organization and Architecture  
**Student**: [Your Name]  
**Roll Number**: 2301201086  
**Institution**: K.R. Mangalam University  
**Date**: November 28, 2025

---

## Abstract

This project presents a complete embedded system design for a Smart Traffic Signal Controller using RISC-V architecture. The system integrates four critical computer architecture components: (1) a custom instruction set architecture with 9 RISC-V instructions, (2) a 5-stage pipelined processor with hazard handling, (3) a two-level cache hierarchy simulator, and (4) I/O strategy comparison between Programmed I/O and DMA. The final system achieves an 18.6× performance improvement over a non-optimized baseline through pipeline parallelism (CPI=1.24), cache optimization (85.71% hit rate), and DMA-based I/O (1.53× speedup).

---

## Table of Contents
1. Introduction
2. Phase 1: ISA Design
3. Phase 2: Pipeline Design
4. Phase 3: Cache Simulator
5. Phase 4: I/O Strategy
6. System Integration
7. Results and Analysis
8. Conclusion
9. References

---

## 1. Introduction

### 1.1 Project Motivation
Traffic congestion is a critical urban problem. Smart traffic controllers dynamically adjust signal timing based on real-time vehicle density, improving traffic flow and reducing wait times. This project explores the computer architecture design challenges of such a real-time embedded system.

### 1.2 System Requirements
- **Real-time Processing**: Control loop must execute in <100ms
- **Multiple I/O Sources**: North-South sensors, East-West sensors, emergency override
- **Data Logging**: Store traffic statistics for analysis
- **Low Power**: Embedded system constraints

### 1.3 Design Approach
The project follows a bottom-up design methodology:
1. Define minimal instruction set for control logic
2. Design pipelined processor for performance
3. Optimize memory hierarchy for sensor/log access patterns
4. Select appropriate I/O strategy for responsiveness

---

## 2. Phase 1: ISA Design

### 2.1 Instruction Selection
A minimal subset of 9 RISC-V instructions was selected based on control flow requirements:

| Category | Instructions | Purpose |
|----------|-------------|---------|
| Memory | LW, SW | Sensor reads, log writes |
| Arithmetic | ADD, SUB, ADDI | Comparisons, address calculation |
| Control | BEQ, BLT, JAL | Conditional logic, loops |
| Utility | NOP | Pipeline testing |

### 2.2 Assembly Implementation
The traffic controller logic (`traffic_logic.asm`) implements:
- **Sensor polling**: Read NS/EW vehicle counts, emergency status
- **Decision logic**: Compare densities, select priority direction
- **Output control**: Set traffic lights (GREEN/YELLOW/RED)
- **Data logging**: Store traffic snapshots for analysis

**Key Code Segment**:
```
control_loop:
    lw x1, 0(x10)           # Read NS sensor
    lw x2, 0(x11)           # Read EW sensor
    lw x3, 0(x12)           # Read emergency
    beq x3, x4, emergency_mode
    blt x1, x2, ew_priority
    jal x0, ns_priority
```

### 2.3 Memory Map
| Address | Purpose | Access Type |
|---------|---------|-------------|
| 0x1000 | NS sensor | Read |
| 0x1004 | EW sensor | Read |
| 0x1008 | Emergency | Read |
| 0x2000 | Light control | Write |
| 0x3000+ | Log memory | Write |

### 2.4 Instruction Trace Analysis
One control loop iteration executes **21 instructions** with the following breakdown:
- Memory operations: 6 (3 loads, 3 stores)
- Arithmetic: 8 (address calculations, comparisons)
- Control flow: 3 (branches, jumps)
- Initialization: 4

---

## 3. Phase 2: Pipeline Design

### 3.1 Five-Stage Pipeline Architecture

| Stage | Function | Operations | Pipeline Register |
|-------|----------|------------|-------------------|
| IF | Instruction Fetch | Read I-cache, PC+4 | IF/ID |
| ID | Instruction Decode | Decode, register read, control signals | ID/EX |
| EX | Execute | ALU operations, branch resolution | EX/MEM |
| MEM | Memory Access | D-cache read/write | MEM/WB |
| WB | Write Back | Register file update | - |

### 3.2 Hazard Analysis

#### Data Hazards (RAW)
**Problem**: Instruction needs data before previous instruction writes it

**Solutions Implemented**:
1. **Forwarding/Bypassing**: Forward ALU results from EX/MEM and MEM/WB registers
   - Eliminates most RAW stalls
   - Example: `addi x1, x0, 5` → `add x2, x1, x3` (forwarded, no stall)

2. **Load-Use Stall**: LW followed by dependent instruction requires 1-cycle stall
   - Cannot forward before memory read completes
   - Example: `lw x1, 0(x10)` → `blt x1, x2, label` (1 stall)

#### Control Hazards (Branches)
**Problem**: Don't know next instruction until branch resolves in EX stage

**Solution**: Predict Not Taken + Flush on Misprediction
- Assume branch not taken, continue fetching
- If taken: flush 2 instructions (2-cycle penalty)
- Branch resolution in EX stage (cycle 3)

#### Performance Impact
- **Base instruction count**: 21
- **Load-use stall**: 1 cycle
- **Branch penalties**: 4 cycles (2 branches × 2 flushes)
- **Total cycles**: 26
- **CPI**: 26/21 = **1.24**

### 3.3 Pipeline Efficiency
- **Ideal CPI**: 1.0 (perfect pipeline)
- **Achieved CPI**: 1.24
- **Pipeline efficiency**: 81% (1.0/1.24)
- **Forwarding saved**: 6 additional stalls prevented

---

## 4. Phase 3: Cache Simulator

### 4.1 Cache Configuration
**L1 Data Cache**:
- Size: 16 KB
- Block size: 64 bytes
- Associativity: 2-way set associative
- Replacement: LRU (Least Recently Used)
- Write policy: Write-back

### 4.2 Simulator Implementation
The Python-based cache simulator (`cache_simulator.py`) implements:
- Address parsing (tag, set index, block offset)
- LRU replacement algorithm
- Hit/miss detection
- Write-back handling
- Performance metrics calculation

### 4.3 Simulation Results (3 Control Loop Iterations)

| Metric | Value |
|--------|-------|
| Total Accesses | 21 |
| Cache Hits | 18 |
| Cache Misses | 3 |
| **Hit Rate** | **85.71%** |
| Miss Rate | 14.29% |
| Reads | 9 |
| Writes | 12 |
| Writebacks | 0 |
| **AMAT** | **2.43 cycles** |

### 4.4 Locality Analysis

**Temporal Locality**:
- Sensor addresses (0x1000, 0x1004, 0x1008) accessed every iteration
- Traffic light control (0x2000) accessed every iteration
- High reuse → excellent hit rate after cold start

**Spatial Locality**:
- Log writes (0x3000-0x3020) are sequential
- Single cache block (64B) can hold multiple log entries
- Consecutive writes hit in same block

### 4.5 Performance Impact
**Without Cache**: 21 accesses × 100 cycles = 2,100 cycles  
**With Cache**: 18 hits × 1 cycle + 3 misses × 10 cycles = 48 cycles  
**Speedup**: 43.75×

### 4.6 Design Justification
- **2-way associativity**: Balances hit rate and hardware cost
- **64B blocks**: Exploits spatial locality in log writes
- **Write-back**: Reduces memory traffic for frequent log updates

---

## 5. Phase 4: I/O Strategy

### 5.1 Strategies Compared

#### Programmed I/O (Polling)
- CPU actively checks device status
- CPU performs all data transfers
- Simple implementation, high CPU overhead

#### Direct Memory Access (DMA)
- CPU initializes DMA controller
- DMA handles data transfer independently
- Complex hardware, low CPU overhead

### 5.2 Simulation Results (One Iteration)

| Metric | Programmed I/O | DMA | Improvement |
|--------|----------------|-----|-------------|
| Total Cycles | 69 | 45 | **1.53× faster** |
| CPU Busy | 69 | 9 | **87% reduction** |
| CPU Idle | 0 | 36 | +36 cycles free |
| CPU Utilization | 100% | 20% | 80% available |

### 5.3 Workload Breakdown

**Programmed I/O**:
- 3 sensor reads: 3 × 15 = 45 cycles (CPU polls + transfers)
- 1 log write (3 words): 24 cycles (CPU transfers word-by-word)
- Total: 69 cycles, CPU 100% busy

**DMA**:
- 3 sensor reads: 3 × 12 = 36 cycles (CPU busy: 6 cycles)
- 1 log write (3 words): 9 cycles (CPU busy: 3 cycles)
- Total: 45 cycles, CPU busy: 9 cycles only

### 5.4 Trade-offs

| Aspect | Programmed I/O | DMA |
|--------|----------------|-----|
| Performance | Slower | Faster |
| CPU Efficiency | Low (100% busy) | High (20% busy) |
| Hardware Complexity | Simple | Complex (DMA controller) |
| Scalability | Poor (grows linearly) | Excellent (constant overhead) |
| Best For | Small, infrequent transfers | Bulk data transfers |

### 5.5 Recommendation
**Hybrid Approach**:
- Use **Programmed I/O** for sensor reads (small, time-critical)
- Use **DMA** for log writes (bulk data, background task)
- Maximizes responsiveness while minimizing CPU overhead

---

## 6. System Integration

### 6.1 Component Interaction Diagram
```
┌─────────────────────────────────────────────────────────┐
│                  Traffic Sensors (I/O)                  │
│              [NS: 0x1000] [EW: 0x1004] [EMG: 0x1008]    │
└────────────────────────┬────────────────────────────────┘
                         ↓ (Memory-Mapped I/O)
┌─────────────────────────────────────────────────────────┐
│              L1 Cache (16KB, 2-way, 85.71% hit)         │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│          5-Stage Pipeline (IF→ID→EX→MEM→WB)             │
│        Forwarding + Hazard Detection (CPI=1.24)         │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              RISC-V ISA (9 instructions)                │
└────────────────────────┬────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│          DMA Controller → Log Memory (0x3000+)          │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Data Flow
1. **Sensor Input**: I/O device → Memory-mapped address → Cache → Pipeline MEM stage
2. **Processing**: Register file → ALU (EX stage) → Branch decision
3. **Output Control**: Pipeline → Cache → Traffic lights (0x2000)
4. **Logging**: DMA transfer → Cache → Main memory

### 6.3 Critical Paths
- **Sensor read latency**: I/O + Cache hit (1 cycle) + Pipeline (5 stages)
- **Decision latency**: Load (MEM) → Forward (EX) → Branch (EX) = 3 cycles
- **Log write latency**: DMA setup (3 cycles) + Transfer (background)

---

## 7. Results and Analysis

### 7.1 Overall System Performance

**Baseline System** (No optimizations):
- No pipeline: 21 inst × 5 cycles = 105 cycles
- No cache: 21 accesses × 100 cycles = 2,100 cycles
- Programmed I/O: 69 cycles
- **Total: ~2,274 cycles/iteration**

**Optimized System**:
- Pipeline: 26 cycles (CPI=1.24)
- Cache: 21 accesses × 2.43 avg = 51 cycles
- DMA I/O: 45 cycles (36 CPU-free)
- **Total: ~122 cycles/iteration**

**Overall Speedup: 18.6×**

### 7.2 Component Contributions

| Component | Optimization | Impact |
|-----------|-------------|---------|
| Pipeline | 5-stage + forwarding | CPI: 5.0 → 1.24 (4× improvement) |
| Cache | 2-way, 64B blocks | Memory: 100 → 2.43 avg (41× improvement) |
| I/O | DMA vs PIO | I/O time: 69 → 45 cycles (1.53× improvement) |

### 7.3 Real-Time Performance
- **Target**: <100ms response time
- **Achieved cycle time**: 122 cycles/iteration
- **At 1 MHz clock**: 122 µs/iteration
- **Safety margin**: 820× faster than required
- **Supports**: Multiple intersections, predictive algorithms

---

## 8. Conclusion

### 8.1 Project Summary
This project successfully designed and simulated a complete Smart Traffic Signal Controller system, demonstrating how fundamental computer architecture principles—instruction set design, pipelining, memory hierarchy, and I/O management—integrate to create an efficient embedded system.

### 8.2 Key Achievements
1. **Minimal ISA**: 9-instruction RISC-V subset sufficient for complex control logic
2. **Pipeline Efficiency**: 81% efficiency (CPI=1.24) with forwarding and hazard handling
3. **Memory Optimization**: 85.71% cache hit rate through temporal/spatial locality
4. **I/O Strategy**: DMA provides 1.53× speedup and 87% CPU time savings
5. **System Integration**: 18.6× overall performance improvement

### 8.3 Design Insights
- **Forwarding is critical**: Prevented 6 additional stalls in data hazards
- **Cache blocking matters**: 64B blocks exploit sequential log writes
- **DMA for bulk transfers**: Essential for freeing CPU in real-time systems
- **Hybrid I/O strategy**: Programmed I/O for sensors, DMA for logs

### 8.4 Future Enhancements
1. **Branch Prediction**: Replace "not taken" with dynamic predictor (reduce 2-cycle penalty)
2. **L2 Cache**: Add second cache level for log storage (reduce writeback latency)
3. **Interrupt-Driven I/O**: Replace polling with interrupts (better responsiveness)
4. **Multi-Core**: Parallel processing for multiple intersections
5. **Machine Learning**: Predictive traffic flow using historical log data

### 8.5 Lessons Learned
- **Locality is powerful**: Well-designed memory access patterns yield 40× speedup
- **Hazards are expensive**: Even 1-cycle stalls accumulate in tight loops
- **I/O dominates**: In embedded systems, I/O overhead often exceeds computation
- **Integration complexity**: Component interactions create emergent performance characteristics

### 8.6 Final Remarks
This project demonstrates that modern computer architecture techniques—originally developed for high-performance computing—are equally valuable in resource-constrained embedded systems. The 18.6× performance improvement validates the design decisions and shows the cumulative impact of multiple optimizations working synergistically.

---
