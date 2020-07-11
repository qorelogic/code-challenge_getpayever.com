
import subprocess
import yaml 
#import pandas as p
import json as js
import os, sys

#cmd = "ls pageyml"
#res = os.system(cmd)
#res = subprocess.check_output(cmd.split(' ')).strip()
#print (res)
#sys.exit()

def convert(fname):
	with open(fname, 'r') as stream:
		try:
			res = yaml.safe_load(stream)		
			#print(res)
			#df = p.DataFrame(res)
			#with p.option_context('display.max_rows', 400, 'display.max_columns', 4000, 'display.width', 1000000):
			#	print(df)
			ofname = '%s.json' % fname
			fp = open(ofname, 'w')
			fp.write(js.dumps(res))
			print('saved to: %s' % ofname)
			fp.close()
		except yaml.YAMLError as e:
			print(e)

if __name__ == "__main__":
	import argparse
	## source: https://docs.python.org/2/howto/argparse.html
	parser = argparse.ArgumentParser()

	parser.add_argument("-c", '--convert', help="convert yaml2json", action="store_true")
	parser.add_argument("-f",  '--file', help="filter index by")

	args = parser.parse_args()
	
	if args.convert:
		convert(args.file)

