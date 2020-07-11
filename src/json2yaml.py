
import json as js
import yaml as ym

def convertJson2Yaml(ifname):
	fp = open(ifname, 'r')
	res = fp.read()
	fp.close()

	res = js.loads(res)
	res = ym.dump(res)
	
	return(res)

if __name__ == "__main__":
	import argparse
	## source: https://docs.python.org/2/howto/argparse.html
	parser = argparse.ArgumentParser()

	parser.add_argument("-c", '--convert', help="convert", action="store_true")
	parser.add_argument("-f",  '--ifname',  help="input file")
	parser.add_argument("-o",  '--ofname',  help="output file")

	args = parser.parse_args()
	
	if args.convert:

		ifname = str(args.ifname)
		res = convertJson2Yaml(ifname)
		
		fp = open(args.ofname, 'w')
		fp.write(res)
		fp.close()
		
		

