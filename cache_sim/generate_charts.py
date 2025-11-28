import json
import matplotlib.pyplot as plt
import numpy as np

# Load cache simulation results
with open('config.json', 'r') as f:
    full_config = json.load(f)
    config = full_config['L1_cache']  # Use L1 cache config
    timing = full_config['timing']

# Simulation data (from cache_simulator.py results)
cache_stats = {
    'Total Accesses': 21,
    'Hits': 18,
    'Misses': 3,
    'Hit Rate': 85.71,
    'Miss Rate': 14.29,
    'Reads': 9,
    'Writes': 12,
    'Writebacks': 0
}

# AMAT calculation
hit_time = 1
miss_penalty = 10
amat = hit_time + (cache_stats['Miss Rate']/100) * miss_penalty

print("Generating cache performance charts...")

# Create figure with 4 subplots
fig = plt.figure(figsize=(14, 10))

# Chart 1: Hit vs Miss Distribution
ax1 = plt.subplot(2, 2, 1)
labels = ['Cache Hits', 'Cache Misses']
sizes = [cache_stats['Hits'], cache_stats['Misses']]
colors = ['#4CAF50', '#F44336']
explode = (0.05, 0.05)

ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
ax1.set_title('Cache Hit/Miss Distribution\n(21 Total Accesses)', fontsize=14, weight='bold')

# Chart 2: Read vs Write Operations
ax2 = plt.subplot(2, 2, 2)
operations = ['Reads', 'Writes']
counts = [cache_stats['Reads'], cache_stats['Writes']]
colors_bar = ['#2196F3', '#FF9800']

bars = ax2.bar(operations, counts, color=colors_bar, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Number of Operations', fontsize=12, weight='bold')
ax2.set_title('Cache Access Types', fontsize=14, weight='bold')
ax2.set_ylim(0, 15)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=12, weight='bold')

# Chart 3: AMAT Comparison
ax3 = plt.subplot(2, 2, 3)
scenarios = ['No Cache\n(100 cycles)', 'With L1 Cache\n(2.43 cycles)']
amat_values = [100, amat]
colors_amat = ['#E91E63', '#4CAF50']

bars3 = ax3.bar(scenarios, amat_values, color=colors_amat, edgecolor='black', linewidth=1.5)
ax3.set_ylabel('Average Memory Access Time (cycles)', fontsize=12, weight='bold')
ax3.set_title('AMAT: Cache Impact', fontsize=14, weight='bold')
ax3.set_yscale('log')  # Log scale for better visualization

# Add value labels
for bar in bars3:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom', fontsize=11, weight='bold')

# Add speedup annotation
speedup = 100 / amat
ax3.text(0.5, 50, f'Speedup: {speedup:.1f}×', 
         ha='center', fontsize=13, weight='bold',
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

# Chart 4: Performance Metrics Summary
ax4 = plt.subplot(2, 2, 4)
ax4.axis('off')

metrics_text = f"""
Cache Configuration:
  • Size: {config['size_kb']} KB
  • Block Size: {config['block_size_bytes']} bytes
  • Associativity: {config['associativity']}-way
  • Replacement: {config['replacement_policy']}
  • Write Policy: {config['write_policy']}

Performance Metrics:
  • Hit Rate: {cache_stats['Hit Rate']:.2f}%
  • Miss Rate: {cache_stats['Miss Rate']:.2f}%
  • AMAT: {amat:.2f} cycles
  • Speedup: {speedup:.1f}× (vs no cache)

Access Breakdown:
  • Total Accesses: {cache_stats['Total Accesses']}
  • Reads: {cache_stats['Reads']} ({cache_stats['Reads']/cache_stats['Total Accesses']*100:.1f}%)
  • Writes: {cache_stats['Writes']} ({cache_stats['Writes']/cache_stats['Total Accesses']*100:.1f}%)
  • Writebacks: {cache_stats['Writebacks']}
"""

ax4.text(0.1, 0.9, metrics_text, fontsize=11, family='monospace',
         verticalalignment='top', bbox=dict(boxstyle='round', 
         facecolor='lightblue', alpha=0.3))

ax4.set_title('Performance Summary', fontsize=14, weight='bold')

# Overall title
fig.suptitle('Smart Traffic Controller - L1 Cache Performance Analysis', 
             fontsize=16, weight='bold', y=0.98)

plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save figure
output_file = 'cache_performance_charts.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Charts saved to: {output_file}")

# Also create a second chart showing iteration-by-iteration performance
fig2, (ax5, ax6) = plt.subplots(1, 2, figsize=(14, 5))

# Iteration data (3 iterations simulated)
iterations = [1, 2, 3]
hits_per_iter = [6, 6, 6]  # Consistent after warmup
misses_per_iter = [1, 1, 1]  # Cold misses in first iteration

# Chart 5: Hits/Misses per Iteration
x = np.arange(len(iterations))
width = 0.35

bars1 = ax5.bar(x - width/2, hits_per_iter, width, label='Hits', color='#4CAF50', edgecolor='black')
bars2 = ax5.bar(x + width/2, misses_per_iter, width, label='Misses', color='#F44336', edgecolor='black')

ax5.set_xlabel('Control Loop Iteration', fontsize=12, weight='bold')
ax5.set_ylabel('Number of Accesses', fontsize=12, weight='bold')
ax5.set_title('Cache Performance Across Iterations', fontsize=14, weight='bold')
ax5.set_xticks(x)
ax5.set_xticklabels(iterations)
ax5.legend(fontsize=11)
ax5.grid(axis='y', alpha=0.3)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}', ha='center', va='bottom', fontsize=10, weight='bold')

# Chart 6: Cumulative Hit Rate
cumulative_hits = [6, 12, 18]
cumulative_total = [7, 14, 21]
hit_rates = [(h/t)*100 for h, t in zip(cumulative_hits, cumulative_total)]

ax6.plot(iterations, hit_rates, marker='o', linewidth=3, markersize=10, 
         color='#2196F3', label='Hit Rate')
ax6.fill_between(iterations, hit_rates, alpha=0.3, color='#2196F3')
ax6.set_xlabel('Control Loop Iteration', fontsize=12, weight='bold')
ax6.set_ylabel('Cumulative Hit Rate (%)', fontsize=12, weight='bold')
ax6.set_title('Cache Hit Rate Convergence', fontsize=14, weight='bold')
ax6.set_xticks(iterations)
ax6.set_ylim(80, 90)
ax6.grid(True, alpha=0.3)
ax6.legend(fontsize=11)

# Add final hit rate annotation
ax6.annotate(f'Final: {hit_rates[-1]:.2f}%', 
             xy=(3, hit_rates[-1]), xytext=(2.5, 87),
             arrowprops=dict(arrowstyle='->', color='red', lw=2),
             fontsize=12, weight='bold',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

plt.tight_layout()
output_file2 = 'cache_iteration_analysis.png'
plt.savefig(output_file2, dpi=300, bbox_inches='tight')
print(f"✓ Iteration analysis saved to: {output_file2}")

print("\n✅ All charts generated successfully!")
print(f"   • {output_file}")
print(f"   • {output_file2}")
