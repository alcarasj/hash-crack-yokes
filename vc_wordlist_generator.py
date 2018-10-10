import sys
import itertools
from argparse import ArgumentParser

CONSONANTS = "bcdfghjklmnpqrstvwxyz"
VOWELS = "aeiou"

parser = ArgumentParser(description="Generate all possible 5-character words with a user-provided amount of vowels.")
parser.add_argument("-v", "--vowels", dest="number_of_vowels",
		    help="The number of vowels in the word.", type=int)
parser.add_argument("-o", "--output", dest="output_path",
		    help="The output path for the wordlist file.", type=str)
args = parser.parse_args()
number_of_vowels = args.number_of_vowels
output_path = args.output_path

if not number_of_vowels or not output_path:
	print("Specify an output path for the wordlist file, and the amount of vowels.")
else:
	permutations = []
	words = []
	if number_of_vowels <= 0:
		permutations = list(set(["".join(i) for i in itertools.permutations("CCCCC")]))
	elif number_of_vowels == 1:
		permutations = list(set(["".join(i) for i in itertools.permutations("VCCCC")]))
	elif number_of_vowels == 2:
		permutations = list(set(["".join(i) for i in itertools.permutations("VVCCC")]))
	elif number_of_vowels == 3:
		permutations = list(set(["".join(i) for i in itertools.permutations("VVVCC")]))
	elif number_of_vowels == 4:
		permutations = list(set(["".join(i) for i in itertools.permutations("VVVVC")]))
	elif number_of_vowels >= 5:
		permutations = list(set(["".join(i) for i in itertools.permutations("VVVVV")]))

	for permutation in permutations:
		params = []
		for char in permutation:
			if char == "C":
				params.append(CONSONANTS)
			elif char == "V":
				params.append(VOWELS)
		words_for_permutation = list("".join(i) for i in itertools.product(*params))
		words = words + words_for_permutation

	with open(output_path, "w") as wordlist_file:
		for word in words:
			wordlist_file.write(word + "\n")

