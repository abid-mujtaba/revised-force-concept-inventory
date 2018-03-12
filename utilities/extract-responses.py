"""
Extract the responses from the scanned in MCQ answer sheets.
"""

import csv
import sys


def main(raw_file, out_file):

	with open(out_file, 'w', newline='') as fout:
		
		fieldnames = ['id', 'qid', 'rid']
		count = 0

		writer = csv.DictWriter(fout, fieldnames=fieldnames)
		writer.writeheader()

		with open(raw_file, newline='') as fin:

			reader = csv.DictReader(fin)
			# print(reader.fieldnames)

			for row in reader:		# 'row' is an OrderedDict containing the data in the csv row

				D = {}
				count += 1

				try:
					# Process row to construct dictionary for the writer
					D['id'] = count
					D['qid'] = row['questionnaire_id']

					writer.writerow(D)
				

				except ValidationError as e:
					print("ValidationError: " + str(e))



class ValidationError(Exception):

	pass
			


if __name__ == '__main__':

	if len(sys.argv) != 3:
		
		print("Error - Correct command usage is: python3 extract-respones.py <raw csv> <output csv>")

	else:

		main(sys.argv[1], sys.argv[2])
