# Memory mapping
import cle

# Simulation
from unicorn import *
from unicorn.x86_const import *


class Simulation():

	def __init__(self, file_name):
		# Initialize loader
		ld = cle.Loader(file_name)

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

		self.mapped_min_addr = mapped_min_addr
		self.mapped_max_addr = mapped_max_addr
		self.mu = mu

	weights = [set()] * 7

	# Accessors
	def get_rax(self):
		return self.mu.reg_read(UC_X86_REG_RAX)

	def get_emu(self):
		print(self.mu)
		return self.mu

	def get_weights(self):
		return self.weights

	def simulate(self):
		start = self.mapped_min_addr + 1
		runs = 0

		rax = set()

		while start < self.mapped_max_addr: 

			try:
				self.mu.emu_start(start, start + self.mapped_max_addr)
				rax.add(self.get_rax())
			except:
				break
			start += 1	

		return rax


FILE_1 = '../bin/bash'
s = Simulation(FILE_1)

print(s.get_emu())
print(s.get_weights())
print(s.get_rax())

steps = s.simulate()

print(steps)
exit(0)