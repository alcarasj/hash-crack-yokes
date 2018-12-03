import sys

if len(sys.argv) < 2:
	print(“Specify an input path and an output path.”)
else:
 	input_path = sys.argv[1]
	output_path = sys.argv[2]
with open(input_path, “r”, errors=”ignore”) as wordlist:
	words = wordlist.readlines()
	eight_char_words = [w for w in words if len(w) == 9]
	with open(output_path, “w”) as reduced_wordlist:
		for word in eight_char_words:
			reduced_wordlist.write(“%s” % word)

