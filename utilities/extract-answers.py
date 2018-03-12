"""
A script for extracting answers from the specified test file (LaTeX) and storing it in the specified .csv file.
"""

import csv
import re
import sys

re_ans = re.compile(r"\\answer{(\d+)}{(\w)}")


def main(latex_file, csv_file):

	with open(csv_file, 'w', newline='') as fout:

		fieldnames = ['question', 'answer']

		writer = csv.DictWriter(fout, fieldnames=fieldnames)
		writer.writeheader()

		with open(latex_file) as fin:

			for lin in fin.readlines():

				m = re_ans.match(lin.strip())

				if m:
					writer.writerow({'question': m.group(1), 'answer': m.group(2)})



if __name__ == '__main__':

	if len(sys.argv) != 3:
		print("Error - Command should be used as: utilities.py <latex file> <output csv>")

	else:
		main(sys.argv[1], sys.argv[2])
