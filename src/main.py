# Memory mapping
import cle

# Simulation
from unicorn import *
from unicorn.x86_const import *

# Helper Classes
from preprocessor import *


FILE_1 = '../bin/bash'

ld = cle.Loader(FILE_1)

# Get lowest and highest address of total program memory
memory = ld.memory
min_addr = memory.min_addr
max_addr = memory.max_addr
layout = memory.load(min_addr, max_addr)

# Calculate amount of bytes to allocate for simulation
length = max_addr - min_addr
power = 0
while 2**power < length:
	power += 1
total_mem = 2**power

# Init Emulator
mu = Uc(UC_ARCH_X86, UC_MODE_32)
mu.mem_map(min_addr, total_mem)

main_objects = list()

# Write loaded bytes to memory
main = ld.main_object

# Get Amount of memory allocated for main object
length = (main.memory.max_addr - main.memory.min_addr)  
		
# Get mapped addresses
mapped_min_addr = main.mapped_base
mapped_max_addr = mapped_min_addr + length - 1

# Get program bytes
main_bytes = main.memory.load(main.memory.min_addr, main.memory.max_addr)	

# Write binary to emulator memory
mu.mem_write(mapped_min_addr, main_bytes)
print('Written to memory.', main)

mu.reg_write(UC_X86_REG_ECX, 0x1234)
mu.reg_write(UC_X86_REG_EDX, 0x7890)

# print(mu.mem_regions)

mu.emu_start(mapped_min_addr + 1, mapped_min_addr + 4)




# SIMULATE