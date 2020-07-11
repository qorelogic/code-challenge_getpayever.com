
#import subprocess
import yaml
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

def openfile(fname):
	fp = open(fname, 'r') 
	res = fp.read()
	fp.close()
	return(res)

def view(fname, ftype='json'):
	
	res = openfile(fname)
	
	#if ftype == 'json':
	#	res = js.loads(res)
	
	if ftype == 'yaml':
		res = yaml.safe_load(res)
	
	def mkhdr(res, nsep=60):
		keys = ''
		try:
			keys = sorted(res.keys())
			#print('\n--------------------------------------------------------------------------------\n')
			#print(keys)

			li = [x.split('-') for x in keys]
			#print(li)
			dfli = p.DataFrame(li)
			dfli['name'] = keys

			def literalSortMap(dfli, column=0, literals=''):
				vs = literals.split(' ')
				ks = list(range(0, len(vs)))
				#ks = [int(x) for x in '0 1 2 3 4 5 6 7 8 9 10'.split(' ')]
				smap  = dict(zip(ks, vs))
				rsmap = dict(zip(vs, ks))
				#print(smap)
				#print(rsmap)
				#dfli[0] = [rsmap[x] for x in dfli[0]]
				for x in dfli.index:
					try: dfli.loc[x,column] = rsmap[dfli.loc[x,column]]
					except Exception as e: '' #print(e)

				return(dfli)
			
			dfli = literalSortMap(dfli, column=0, literals='desktop tablet mobile')
			dfli = literalSortMap(dfli, column=0, literals='id name variant type master data template stylesheets context')
			dfli = literalSortMap(dfli, column=0, literals='header first second third fourth fifth sixth seventh eighth ninth footer')
			dfli = literalSortMap(dfli, column=1, literals='logo menu cart')
			dfli = literalSortMap(dfli, column=1, literals='column1 column2 column3 column4 column5')

			byl = [0,1] # list(range(0, 1))
			try: dfli = dfli.sort_values(by=byl)
			except Exception as e: '' #print(e)

			try:
				#print('        lenkeys: %s'%len(keys))
				keys = list(dfli['name'])
				#print('lenkeys[sorted]: %s'%len(keys))
			except Exception as e: print(e)

			li = []
			for i in keys:
				li.append(type(res[i]))
				#print('%s: %s %s' % (i, mkspc(i, nsep), type(res[i])))
			dfli['type'] = li
			dfli = dfli.loc[:, 'name type'.split(' ')].set_index('name')
			with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
				print(dfli)
				print('')
			#print('\n++++++++++++++++++++++++++++++++++++++++\n')
			print('\n%s\n' % mkspc('', 40, sep='+'))
		except AttributeError as e:
			#print(e)
			try:
				for i in range(len(res)): print('%s: %s %s' % (i, mkspc(i, 20), type(res[i])))
			except:
				''
		return keys

	def mkall(o, title='Global', nsep=150, transpose=False):
		#print('\n--------------------------------------------------------------------------------\n')
		print('\n---- %s %s %s\n' % (title, str(type(o)), mkspc('', (nsep-len(title)), sep='-')))
		#print(': %s %s' % (mkspc(o, 20), ))
		keys = mkhdr(o)
		try:                    df = p.DataFrame(o)
		except ValueError as e: df = p.DataFrame(o, index=[0])
		df = df.fillna('')
		try:    df = df.loc[:, keys]
		except: ''
		if transpose: df = df.transpose()
		with p.option_context('display.max_rows', 4000, 'display.max_columns', 4000, 'display.width', 1000000):
			print(df)
	
	mkall(res)
	mkall(res['template'],             'template')
	
	o = res['template']['children']
	mkall(o, 'template children')
	for oi in range(len(o)):
		o2 = o[oi]['children']
		mkall(o2,       'template children %s children' % oi)		
		for oi2 in range(len(o2)):
			try:
				o3 = o2[oi2]['data']
			except KeyError as e:
				print(e)
				#continue
				pass
				
			mkall(o3,     'template children %s children %s data'      % (oi, oi2))

			for oi3 in range(len(o3)):
				try:
					mkall(o3[oi3]['src'],  'template children %s children %s data %s src'         % (oi, oi2, oi3))
				except KeyError as e:
					#print(e)
					''

			for oi3 in range(len(o3)):
				try:
					mkall(o3[oi3]['routes'],  'template children %s children %s data %s routes'   % (oi, oi2, oi3))
				except KeyError as e:
					#print(e)
					''
 

	#print('\n================================================================================================================================================================\n')
	print('\n%s\n' % mkspc('', 160, sep='='))
	
	transpose = True
	mkall(res['stylesheets'],            'stylesheets',         nsep=150)
	mkall(res['stylesheets']['mobile'],  'stylesheets mobile',  transpose=transpose)
	mkall(res['stylesheets']['tablet'],  'stylesheets tablet',  transpose=transpose)
	mkall(res['stylesheets']['desktop'], 'stylesheets desktop', transpose=transpose)

if __name__ == "__main__":
	import argparse
	## source: https://docs.python.org/2/howto/argparse.html
	parser = argparse.ArgumentParser()

	parser.add_argument("-v", '--view', help="viewjson", action="store_true")
	parser.add_argument("-sh", '--syntaxHighlight', help="syntax highlight", action="store_true")
	parser.add_argument("-f",  '--file', help="filter index by")
	parser.add_argument("-t",  '--type', help="json | yaml")

	args = parser.parse_args()
	
	if args.view:
		view(args.file, args.type)

	if args.syntaxHighlight:
		# https://stackoverflow.com/questions/9105031/how-to-beautify-json-in-python
		import sys
		import json
		from pygments import highlight, lexers, formatters

		res = openfile(args.file)
		formatted_json = json.dumps(json.loads(res))#, indent=4))
		colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter())
		print(colorful_json)

