# I/O Strategy Comparison: Programmed I/O vs DMA

class IOStrategy:
    def __init__(self, strategy_type):
        self.strategy_type = strategy_type
        self.total_cycles = 0
        self.cpu_busy_cycles = 0
        self.io_operations = 0
    
    def read_sensor(self, sensor_name):
        """Simulate reading a sensor"""
        self.io_operations += 1
        
        if self.strategy_type == "Programmed_IO":
            # CPU polls status, then reads data
            self.total_cycles += 5  # Status check cycles
            self.total_cycles += 10  # Data read cycles
            self.cpu_busy_cycles += 15  # CPU busy entire time
            print(f"  [PIO] Read {sensor_name}: 15 cycles (CPU busy)")
        
        elif self.strategy_type == "DMA":
            # CPU initiates DMA, continues execution
            self.total_cycles += 2  # DMA setup
            self.cpu_busy_cycles += 2  # CPU only busy during setup
            self.total_cycles += 10  # DMA transfer (CPU can do other work)
            print(f"  [DMA] Read {sensor_name}: 12 cycles (CPU busy: 2)")
    
    def write_log(self, data_size_words):
        """Simulate writing log data"""
        self.io_operations += 1
        
        if self.strategy_type == "Programmed_IO":
            # CPU writes each word individually
            cycles_per_word = 8
            total = data_size_words * cycles_per_word
            self.total_cycles += total
            self.cpu_busy_cycles += total
            print(f"  [PIO] Write log ({data_size_words} words): {total} cycles (CPU busy)")
        
        elif self.strategy_type == "DMA":
            # DMA handles bulk transfer
            self.total_cycles += 3  # DMA setup
            self.cpu_busy_cycles += 3
            transfer_cycles = data_size_words * 2  # DMA is faster
            self.total_cycles += transfer_cycles
            print(f"  [DMA] Write log ({data_size_words} words): {transfer_cycles + 3} cycles (CPU busy: 3)")
    
    def get_stats(self):
        return {
            'strategy': self.strategy_type,
            'total_cycles': self.total_cycles,
            'cpu_busy_cycles': self.cpu_busy_cycles,
            'cpu_idle_cycles': self.total_cycles - self.cpu_busy_cycles,
            'io_operations': self.io_operations,
            'cpu_utilization': (self.cpu_busy_cycles / self.total_cycles * 100) if self.total_cycles > 0 else 0
        }


def simulate_traffic_controller():
    """Simulate one iteration of traffic controller with both I/O strategies"""
    
    print("="*60)
    print("PROGRAMMED I/O STRATEGY")
    print("="*60)
    
    pio = IOStrategy("Programmed_IO")
    
    # One control loop iteration
    pio.read_sensor("NS Vehicle Count")
    pio.read_sensor("EW Vehicle Count")
    pio.read_sensor("Emergency Button")
    pio.write_log(3)  # Log 3 words: NS count, EW count, light state
    
    pio_stats = pio.get_stats()
    
    print("\n" + "="*60)
    print("DMA STRATEGY")
    print("="*60)
    
    dma = IOStrategy("DMA")
    
    # One control loop iteration
    dma.read_sensor("NS Vehicle Count")
    dma.read_sensor("EW Vehicle Count")
    dma.read_sensor("Emergency Button")
    dma.write_log(3)  # Log 3 words
    
    dma_stats = dma.get_stats()
    
    # Print comparison
    print("\n" + "="*60)
    print("COMPARISON RESULTS")
    print("="*60)
    print(f"\n{'Metric':<30} {'Programmed I/O':<20} {'DMA':<20}")
    print("-"*70)
    print(f"{'Total Cycles':<30} {pio_stats['total_cycles']:<20} {dma_stats['total_cycles']:<20}")
    print(f"{'CPU Busy Cycles':<30} {pio_stats['cpu_busy_cycles']:<20} {dma_stats['cpu_busy_cycles']:<20}")
    print(f"{'CPU Idle Cycles':<30} {pio_stats['cpu_idle_cycles']:<20} {dma_stats['cpu_idle_cycles']:<20}")
    print(f"{'I/O Operations':<30} {pio_stats['io_operations']:<20} {dma_stats['io_operations']:<20}")
    print(f"{'CPU Utilization':<30} {pio_stats['cpu_utilization']:.1f}%{' '*15} {dma_stats['cpu_utilization']:.1f}%")
    
    speedup = pio_stats['total_cycles'] / dma_stats['total_cycles']
    cpu_efficiency = (pio_stats['cpu_busy_cycles'] - dma_stats['cpu_busy_cycles']) / pio_stats['cpu_busy_cycles'] * 100
    
    print(f"\n{'Speedup (DMA vs PIO):':<30} {speedup:.2f}x")
    print(f"{'CPU Time Saved:':<30} {cpu_efficiency:.1f}%")

if __name__ == "__main__":
    simulate_traffic_controller()
