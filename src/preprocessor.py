from elftools.elf.elffile import ELFFile
from elftools.elf.sections import NoteSection

class PreProcessor():
	def __init__(self):
		pass

	def extract(self, file):
		# List to hold sections of code
		sections = list()

		with open(file, 'rb') as file_handle:
			# Load file into elf parser
			elffile = ELFFile(file_handle)

			# Iterate ELF sections
			for section in elffile.iter_sections():

				print(section.name)
				# Extract executable code sections.
				if section.header['sh_type'] == "SHT_PROGBITS":
					name = section.name
					sections.append(section.name)

		return sections