import matplotlib.pyplot as plt

# Components in the disaster management system
components = [
    "IoT Sensors",
    "Data Processing",
    "Cloud Computing",
    "Communication",
    "Relief Logistics"
]

# Hypothetical energy usage in watts (W) for each component
# Before optimization
traditional_energy = [100, 120, 150, 90, 200]
# After implementing solutions
optimized_energy = [60, 70, 90, 50, 120]

# Plotting
x = range(len(components))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
bar1 = ax.bar([i - width/2 for i in x], traditional_energy, width, label="Traditional System", color='tomato')
bar2 = ax.bar([i + width/2 for i in x], optimized_energy, width, label="Optimized System", color='mediumseagreen')

# Labels and titles
ax.set_xlabel('System Components')
ax.set_ylabel('Energy Consumption (Watts)')
ax.set_title('Energy Consumption Comparison: Traditional vs Optimized System')
ax.set_xticks(list(x))
ax.set_xticklabels(components)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
