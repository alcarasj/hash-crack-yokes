import sys
import itertools
from argparse import ArgumentParser
from secretsharing import SecretSharer
from utils import pxor, decrypt 
import json
from secretsharing import secret_int_to_points, points_to_secret_int
import jsonpickle

parser = ArgumentParser(description="Cracks an InfernoBall with a potfile.")
parser.add_argument("-i", "--infernoball", dest="inferno_ball",
                    help="The path to the InfernoBall JSON file.", type=str)
parser.add_argument("-p", "--potfile", dest="potfile",
		    help="The path to the potfile", type=str)
parser.add_argument("-o", "--output", dest="output_path",
                    help="The output path for the resulting deciphered InfernoBall.", type=str)
args = parser.parse_args()
inferno_ball = args.inferno_ball
potfile = args.potfile
output_path = args.output_path


if not (inferno_ball or potfile or output_path):
	print("Please specify an InfernoBall JSON file, a potfile, and an output path.")
else:
	passwords = list(set(open(potfile, "r").read().splitlines()))
	current_level = json.load(open(inferno_ball))
	level_hashes = current_level["hashes"]
	level_ciphertext = current_level["ciphertext"]
	level_shares = current_level["shares"]

	shares = []

	for password in passwords:
		password = password.rstrip()
		index = level_hashes.index(password.split(":", 1)[0])
		share = level_shares[index]
		xored = pxor(password.split(":", 1)[1], share)
		shares.append(str(xored))

	secret = SecretSharer.recover_secret(shares)

	decrypted = decrypt(level_ciphertext, secret.zfill(32).decode('hex'))
	try:
		decrypted = json.loads(decrypted)
		print("Level-up success! SECRET: %s" % secret)   
	except:
		print("Level-up failed. Crack moar hashes.")
	decrypted["ciphertext"] = str(decrypted["ciphertext"])
	decrypted["hashes"] = [str(s) for s in decrypted["hashes"]]
	decrypted["shares"] = [str(s) for s in decrypted["shares"]]
	decrypted["easteregg"] = str(decrypted["easteregg"])

	output_hashes = open(output_path + ".hashes", "w")
	output_json = open(output_path + ".json", "w")
	for h in decrypted["hashes"]:
		output_hashes.write(h + "\n")
	json.dump(decrypted, output_json)
