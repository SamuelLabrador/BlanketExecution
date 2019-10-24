from elftools.elf.elffile import ELFFile
from elftools.elf.sections import NoteSection

class PreProcessor():
	def __init__(self, file):
		self.file = file

	def extract(self):
		# List to hold sections of code
		sections = list()

		with open(self.file, 'rb') as file_handle:
			# Load file into elf parser
			elffile = ELFFile(file_handle)

			# Iterate ELF sections
			for section in elffile.iter_sections():

				# Extract executable code sections.
				if section.header['sh_type'] == "SHT_PROGBITS":
					secions.append(section)

		return sections


