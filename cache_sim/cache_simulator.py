import json
import math

class Cache:
    def __init__(self, size_kb, block_size, associativity, replacement_policy):
        self.size = size_kb * 1024  # Convert to bytes
        self.block_size = block_size
        self.associativity = associativity
        self.replacement_policy = replacement_policy
        
        # Calculate cache parameters
        self.num_blocks = self.size // self.block_size
        self.num_sets = self.num_blocks // self.associativity
        
        # Initialize cache structure: list of sets, each set has list of blocks
        # Each block: {'valid': bool, 'tag': int, 'dirty': bool, 'lru_counter': int}
        self.cache = [[{'valid': False, 'tag': None, 'dirty': False, 'lru_counter': 0} 
                       for _ in range(self.associativity)] 
                      for _ in range(self.num_sets)]
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.reads = 0
        self.writes = 0
        self.writebacks = 0
    
    def parse_address(self, address):
        """Parse address into tag, set index, and block offset"""
        block_offset_bits = int(math.log2(self.block_size))
        set_index_bits = int(math.log2(self.num_sets))
        
        block_offset = address & ((1 << block_offset_bits) - 1)
        set_index = (address >> block_offset_bits) & ((1 << set_index_bits) - 1)
        tag = address >> (block_offset_bits + set_index_bits)
        
        return tag, set_index, block_offset
    
    def access(self, address, operation):
        """Access cache (operation: 'R' for read, 'W' for write)"""
        tag, set_index, block_offset = self.parse_address(address)
        cache_set = self.cache[set_index]
        
        if operation == 'R':
            self.reads += 1
        else:
            self.writes += 1
        
        # Check for hit
        hit_index = -1
        for i, block in enumerate(cache_set):
            if block['valid'] and block['tag'] == tag:
                hit_index = i
                break
        
        if hit_index != -1:
            # Cache hit
            self.hits += 1
            self.update_lru(cache_set, hit_index)
            if operation == 'W':
                cache_set[hit_index]['dirty'] = True
            return True
        else:
            # Cache miss
            self.misses += 1
            self.handle_miss(cache_set, tag, operation)
            return False
    
    def update_lru(self, cache_set, accessed_index):
        """Update LRU counters"""
        for i, block in enumerate(cache_set):
            if block['valid']:
                block['lru_counter'] += 1
        cache_set[accessed_index]['lru_counter'] = 0
    
    def handle_miss(self, cache_set, tag, operation):
        """Handle cache miss - find victim and replace"""
        # Find invalid block first
        victim_index = -1
        for i, block in enumerate(cache_set):
            if not block['valid']:
                victim_index = i
                break
        
        # If no invalid block, use LRU
        if victim_index == -1:
            max_lru = -1
            for i, block in enumerate(cache_set):
                if block['lru_counter'] > max_lru:
                    max_lru = block['lru_counter']
                    victim_index = i
        
        # Check if victim is dirty (needs writeback)
        if cache_set[victim_index]['valid'] and cache_set[victim_index]['dirty']:
            self.writebacks += 1
        
        # Replace block
        cache_set[victim_index]['valid'] = True
        cache_set[victim_index]['tag'] = tag
        cache_set[victim_index]['dirty'] = (operation == 'W')
        self.update_lru(cache_set, victim_index)
    
    def get_stats(self):
        """Return cache statistics"""
        total_accesses = self.hits + self.misses
        hit_rate = self.hits / total_accesses if total_accesses > 0 else 0
        miss_rate = self.misses / total_accesses if total_accesses > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'total_accesses': total_accesses,
            'hit_rate': hit_rate,
            'miss_rate': miss_rate,
            'reads': self.reads,
            'writes': self.writes,
            'writebacks': self.writebacks
        }


def simulate():
    """Main simulation function"""
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Initialize L1 cache
    l1 = Cache(
        config['L1_cache']['size_kb'],
        config['L1_cache']['block_size_bytes'],
        config['L1_cache']['associativity'],
        config['L1_cache']['replacement_policy']
    )
    
    # Load memory trace
    with open('memory_trace.txt', 'r') as f:
        trace_lines = f.readlines()
    
    print("=== Cache Simulation Started ===\n")
    
    # Process each memory access
    for line in trace_lines:
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        
        parts = line.split()
        operation = parts[0]  # 'R' or 'W'
        address = int(parts[1], 16)  # Convert hex to int
        
        l1.access(address, operation)
    
    # Get statistics
    stats = l1.get_stats()
    
    # Calculate AMAT
    l1_hit_time = config['timing']['L1_hit_time']
    l1_miss_penalty = config['timing']['L1_miss_penalty']
    amat = l1_hit_time + (stats['miss_rate'] * l1_miss_penalty)
    
    # Print results
    print(f"L1 Cache Statistics:")
    print(f"  Total Accesses: {stats['total_accesses']}")
    print(f"  Hits: {stats['hits']}")
    print(f"  Misses: {stats['misses']}")
    print(f"  Hit Rate: {stats['hit_rate']:.2%}")
    print(f"  Miss Rate: {stats['miss_rate']:.2%}")
    print(f"  Reads: {stats['reads']}")
    print(f"  Writes: {stats['writes']}")
    print(f"  Writebacks: {stats['writebacks']}")
    print(f"\nAMAT (Average Memory Access Time): {amat:.2f} cycles")

if __name__ == "__main__":
    simulate()
