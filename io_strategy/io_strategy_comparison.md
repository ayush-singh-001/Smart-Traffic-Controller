# I/O Strategy Comparison Report

## Strategies Evaluated

### 1. Programmed I/O (Polling)
- CPU actively polls device status
- CPU performs all data transfers
- CPU blocked during entire I/O operation

### 2. Direct Memory Access (DMA)
- CPU sets up DMA controller
- DMA handles data transfer independently
- CPU free to execute other instructions during transfer

## Simulation Results (One Control Loop Iteration)

| Metric | Programmed I/O | DMA | Improvement |
|--------|---------------|-----|-------------|
| **Total Cycles** | 69 | 45 | 1.53× faster |
| **CPU Busy Cycles** | 69 | 9 | 87% reduction |
| **CPU Idle Cycles** | 0 | 36 | +36 cycles free |
| **I/O Operations** | 4 | 4 | Same |
| **CPU Utilization** | 100% | 20% | 80% available |

## Analysis

### Programmed I/O Breakdown
- Sensor reads (3×): 3 × 15 = 45 cycles
- Log write (3 words): 24 cycles
- **Total: 69 cycles, CPU 100% busy**

### DMA Breakdown
- Sensor reads (3×): 3 × 12 = 36 cycles (CPU busy: 6 cycles)
- Log write (3 words): 9 cycles (CPU busy: 3 cycles)
- **Total: 45 cycles, CPU busy: 9 cycles only**

### Key Findings

1. **Performance**: DMA provides **1.53× speedup** over Programmed I/O
2. **CPU Efficiency**: DMA frees **87% of CPU time** for other tasks
3. **Scalability**: As log size increases, DMA advantage grows significantly
4. **Real-time Suitability**: DMA allows CPU to handle multiple sensors/controllers simultaneously

## Recommendation
**Use DMA for traffic log writes** (bulk data), **Programmed I/O acceptable for sensor reads** (small, frequent data).
