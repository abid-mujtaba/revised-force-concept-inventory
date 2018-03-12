"""
Extract the responses from the scanned in MCQ answer sheets.
"""

import sys


def main(raw_file, out_file):

	print("Hello, World")


if __name__ == '__main__':

	if len(sys.argv) != 3:
		
		print("Error - Correct command usage is: python3 extract-respones.py <raw csv> <output csv>")

	else:

		main(sys.argv[1], sys.argv[2])
