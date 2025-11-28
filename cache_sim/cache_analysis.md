# Cache Simulator Analysis

## Configuration
- **L1 Cache**: 16 KB, 2-way set associative, 64B blocks, LRU replacement, write-back
- **L1 Hit Time**: 1 cycle
- **L1 Miss Penalty**: 10 cycles

## Simulation Results (Traffic Controller - 3 Iterations)

### Performance Metrics
| Metric | Value |
|--------|-------|
| Total Memory Accesses | 21 |
| Cache Hits | 18 |
| Cache Misses | 3 |
| Hit Rate | **85.71%** |
| Miss Rate | 14.29% |
| Read Operations | 9 |
| Write Operations | 12 |
| Writebacks | 0 |
| **AMAT** | **2.43 cycles** |

### Analysis

**Why High Hit Rate?**
- Sensor addresses (0x1000, 0x1004, 0x1008) are repeatedly accessed → temporal locality
- Log writes (0x3000-0x3020) are sequential → spatial locality within cache blocks
- Traffic light control (0x2000) accessed every iteration → high temporal locality

**Cold Start Misses:**
- First access to 0x1000 (sensor NS) → miss
- First access to 0x2000 (light control) → miss  
- First access to 0x3000 (log base) → miss
- All subsequent accesses hit in cache

**Memory Traffic Reduction:**
- Without cache: 21 memory accesses = 2100 cycles (21 × 100)
- With cache: 18 hits + 3 misses = 18(1) + 3(10) = **48 cycles**
- **Speedup: 43.75× improvement**
