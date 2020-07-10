
#import subprocess
#import yaml 
import pandas as p
import json as js
import os, sys

#cmd = "ls pageyml"
#res = os.system(cmd)
#res = subprocess.check_output(cmd.split(' ')).strip()
#print (res)
#sys.exit()

def mkspc(x, maxsp, sep=' '):
	return(''.join([sep]*(maxsp-len(x))))

def view(fname):
	fp = open(fname, 'r') 
	res = fp.read()
	fp.close()
	res = js.loads(res)
	
	def mkhdr(res, nsep=60):
		keys = ''
		try:
			keys = sorted(res.keys())
			#print('\n--------------------------------------------------------------------------------\n')
			#print(keys)
			for i in keys:
				print('%s: %s %s' % (i, mkspc(i, nsep), type(res[i])))
			#print('\n++++++++++++++++++++++++++++++++++++++++\n')
			print('\n%s\n' % mkspc('', 40, sep='+'))
		except AttributeError as e:
			#print(e)
			try:
				for i in range(len(res)): print('%s: %s %s' % (i, mkspc(i, 20), type(res[i])))
			except:
				''
		return keys

	def mkall(o, title='Global', nsep=150):
		#print('\n--------------------------------------------------------------------------------\n')
		print('\n---- %s %s %s\n' % (title, str(type(o)), mkspc('', (nsep-len(title)), sep='-')))
		#print(': %s %s' % (mkspc(o, 20), ))
		keys = mkhdr(o)
		df = p.DataFrame(o)
		df = df.fillna('')
		with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
			try:    print(df.loc[:, keys])
			except: print(df)
	
	mkall(res)
	mkall(res['template'],             'template')
	mkall(res['template']['children'], 'template children')
	
	o = res['template']['children']
	for oi in range(len(o)):
		mkall(o[oi]['children'],       'template children children %s' % oi)

	#print('\n================================================================================================================================================================\n')
	print('\n%s\n' % mkspc('', 160, sep='='))
	
	mkall(res['stylesheets'],            'stylesheets',         nsep=150)
	mkall(res['stylesheets']['mobile'],  'stylesheets mobile')
	mkall(res['stylesheets']['tablet'],  'stylesheets tablet')
	mkall(res['stylesheets']['desktop'], 'stylesheets desktop')

if __name__ == "__main__":
	import argparse
	## source: https://docs.python.org/2/howto/argparse.html
	parser = argparse.ArgumentParser()

	parser.add_argument("-v", '--view', help="viewjson", action="store_true")
	parser.add_argument("-f",  '--file', help="filter index by")

	args = parser.parse_args()
	
	if args.view:
		view(args.file)

