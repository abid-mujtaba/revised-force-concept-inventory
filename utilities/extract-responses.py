"""
Extract the responses from the scanned in MCQ answer sheets.
"""

import csv
import sys


def main(raw_file, out_file, qid_file=None):

	# Read the qid_file and store the provided qids in a dictionary for later use
	Q = {}

	if qid_file:
		
		with open(qid_file, newline='') as fin:
			
			reader = csv.DictReader(fin)

			for row in reader:

				Q[int(row['q'])] = row['qid']

	

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
					D['qid'] = row['questionnaire_id'][3:]		# Remove the 'FCI' substring at the start

					if row['questionnaire_id'] == 'None':

						if count in Q:

							D['qid'] = Q[count]

						else:
							raise ValidationError("Questionnaire ID is missing for row {}".format(count))

					# Construct Student Registration ID
					semester = extract_single(count, row, '1_2', ['SP', 'FA'])
					D['rid'] = semester

					# Write extracted dictionary to output csv file
					writer.writerow(D)
				
				except ValidationError as e:
					print("ValidationError: " + str(e))

				# TODO Remove to iterate over all rows
				# break


def extract_single(id, row, prefix, entries, checkZero = True):
	"""
	Extract an entry which appears singly in answer-sheet.tex (such as BEL/BPH or SP/FA).
	"""
	return extract(id, row, prefix, entries, checkZero, True)


def extract_group(id, row, prefix, entries, checkZero = True):
	"""
	Extract an entry which appears in a group such as A/B/C/D/E.
	"""
	return extract(id, row, prefix, entries, checkZero, False)


def extract(id, row, prefix, entries, checkZero = True, single = False):
	"""
	Extract the passed in row dictionary to check that at most one entry is filled.
	If checkZero is set we also confirm that at least one entry is filled.
	The prefix provides the common starting string of the entries (the remainder is generated based on the length of the list 'entries').

	The list entries maps the index to the actual value represented by the box e.g. 1/2 -> FA/SP
	"""

	fmt_str = "{prefix}_{index}_0" if single else "{prefix}_{index}"

	count = 0
	result = None

	for i in range(1, len(entries) + 1):

		# Construct the dictionary key to access the value in the dictionary
		key = fmt_str.format(prefix=prefix, index=i)

		if int(row[key]) != 0:
			count += 1
			result = entries[i - 1]
	
	if count > 1:
		raise ValidationError("More than one box is checked in Q. {prefix} in row {id}".format(id=id, prefix=prefix))

	if checkZero and count == 0:
		raise ValidationError("No box is checked in Q. {prefix} in row {id}".format(id=id, prefix=prefix))

	return result


class ValidationError(Exception):
	pass
			


if __name__ == '__main__':

	if len(sys.argv) == 3:
		
		main(sys.argv[1], sys.argv[2])

	elif len(sys.argv) == 4:

		main(sys.argv[1], sys.argv[2], sys.argv[3])
	
	else:
		print("Error - Correct command usage is: python3 extract-respones.py <raw csv> <output csv>")

