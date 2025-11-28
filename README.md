# Smart Traffic Signal Controller - Computer Architecture Project

**Student**: Ayush Singh  
**Roll Number**: 2301201086  
**Course**: Computer Organization and Architecture  
**Institution**: K.R. Mangalam University  
**Date**: November 28, 2025

---

## Project Overview

A complete embedded system design demonstrating computer architecture principles through a Smart Traffic Signal Controller. The system integrates ISA design, pipelined processor architecture, cache memory hierarchy, and I/O management strategies.

**Key Achievement**: **18.6× performance improvement** through architectural optimizations

---

## Project Structure

```
SmartTrafficController/
│
├── README.md                          # This file
│
├── isa/
│   ├── traffic_logic.asm              # RISC-V assembly code (21 instructions)
│   ├── instruction_formats.md         # 9 instruction definitions
│   ├── memory_map.md                  # I/O address mapping
│   └── execution_trace.txt            # Instruction trace analysis
│
├── pipeline/
│   ├── pipeline_design.md             # 5-stage pipeline architecture
│   ├── hazard_handling_report.md      # Data/control hazard analysis
│   └── logisim/                       # Circuit implementation folder
│
├── cache_sim/
│   ├── cache_simulator.py             # Python cache simulator
│   ├── config.json                    # Cache configuration (16KB, 2-way)
│   ├── memory_trace.txt               # Memory access trace
│   └── cache_analysis.md              # Performance analysis
│
├── io_strategy/
│   ├── io_comparison.py               # PIO vs DMA simulator
│   ├── io_strategy_comparison.md      # I/O performance comparison
│   └── integration_summary.md         # System integration overview
│
└── report/
    ├── final_report.md                # Comprehensive project report
    └── references.md                  # Academic references
```

---

## Quick Results Summary

| Component | Metric | Value |
|-----------|--------|-------|
| **ISA** | Instruction count | 21 per iteration |
| **Pipeline** | CPI (Cycles Per Instruction) | 1.24 |
| **Cache** | Hit rate | 85.71% |
| **Cache** | AMAT | 2.43 cycles |
| **I/O (DMA)** | Speedup vs PIO | 1.53× |
| **I/O (DMA)** | CPU time saved | 87% |
| **Overall** | System speedup | 18.6× |

---

## How to Run

### ISA Execution Trace
```
cd isa
# Open traffic_logic.asm in RARS (RISC-V simulator)
# Or review execution_trace.txt for manual trace
```

### Cache Simulator
```
cd cache_sim
python cache_simulator.py
```

Expected output:
```
L1 Cache Statistics:
  Hit Rate: 85.71%
  AMAT: 2.43 cycles
```

### I/O Strategy Comparison
```
cd io_strategy
python io_comparison.py
```

Expected output:
```
Speedup (DMA vs PIO): 1.53x
CPU Time Saved: 87.0%
```

---

## Key Design Decisions

1. **Minimal ISA**: 9 RISC-V instructions sufficient for control logic
2. **Forwarding**: Eliminates most data hazard stalls
3. **2-way Cache**: Balances hit rate (85.71%) and hardware cost
4. **64B Cache Blocks**: Exploits spatial locality in sequential log writes
5. **Hybrid I/O**: DMA for bulk transfers, polling for sensors

---

## Performance Breakdown

### Baseline (Unoptimized)
- Single-cycle processor: 105 cycles
- No cache: 2,100 cycles (21 × 100)
- Programmed I/O: 69 cycles
- **Total: ~2,274 cycles**

### Optimized System
- Pipelined execution: 26 cycles
- Cached memory: 51 cycles (21 × 2.43)
- DMA I/O: 45 cycles
- **Total: ~122 cycles**

**Overall Speedup: 18.6×**

---

## Technologies Used

- **Language**: RISC-V Assembly, Python 3
- **Tools**: RARS (RISC-V simulator), Logisim Evolution
- **Libraries**: Python standard library (json, math)

---

## Learning Outcomes

✅ Designed custom ISA for embedded control application  
✅ Implemented 5-stage pipeline with hazard handling  
✅ Built cache simulator with LRU replacement  
✅ Compared I/O strategies quantitatively  
✅ Integrated multiple architecture components  
✅ Achieved 18.6× performance through optimization  

---

## Documentation

📄 **Comprehensive Report**: `report/final_report.md`  
📊 **Phase Summaries**: Available in each subdirectory  
📚 **References**: `report/references.md`

---

## Contact

**Student**: Ayush Singh 
**Email**: ayush81700@gmail.com  
**Roll Number**: 2301201086

---

## Acknowledgments

- K.R. Mangalam University - Computer Architecture Course
- RISC-V Foundation - ISA Specification
- Patterson & Hennessy - Computer Architecture Textbook
