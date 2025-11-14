from m5.objects import *
import m5

# User configuration
num_cpus = 4

binary_paths = [
    "/bin/ls",
    "/bin/echo",
    "/bin/date",
    "/bin/uname"
]

# System setup
system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

# Create CPUs
system.cpu = [TimingSimpleCPU(cpu_id=i) for i in range(num_cpus)]

# Create a system crossbar
system.membus = SystemXBar()

# Connect CPUs to membus
for cpu in system.cpu:
    cpu.icache_port = system.membus.cpu_side_ports
    cpu.dcache_port = system.membus.cpu_side_ports

# System port connection
system.system_port = system.membus.cpu_side_ports

# Memory controller
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.mem_side_ports = system.membus.mem_side_ports

# Interrupt controller
for cpu in system.cpu:
    cpu.createInterruptController()

# Workloads (assign 1 binary per CPU)
for i, cpu in enumerate(system.cpu):
    proc = Process()
    proc.cmd = [binary_paths[i]]
    cpu.workload = proc
    cpu.createThreads()

# Run simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print(f"Starting multicore simulation with {num_cpus} CPUs...")
exit_event = m5.simulate()
print(f"Exiting @ tick {m5.curTick()} because: {exit_event.getCause()}")
