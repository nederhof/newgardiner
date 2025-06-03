import csv
import re
import csv
from collections import defaultdict

BASIC_START = 0x13000
BASIC_END = 0x1342F

def simplify_unikemet_name(name):
	name = name.replace('HJ ', '')
	match = re.match('^([A-IK-Z]?|NL|NU|AA)([0-9]{3})([A-Z]{0,2})$', name)
	if match:
		category = match.group(1).replace('AA', 'Aa')
		number = match.group(2).lstrip('0')
		suffix = match.group(3).lower()
		simplified = category + number + suffix
		return simplified
	else:
		print('Unikemet name not matching pattern', name)
	return name

def read_unikemet(filename):
	cat = {}
	core = {}
	desc = {}
	func = {}
	fval = {}
	unik = {}
	jsesh = {}
	hg = {}
	ifao = {}
	nomirror = {}
	norotate = {}
	altseq = {}
	with open(filename, 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			if not row[0].startswith('#'):
				code = int(row[0].replace('U+', ''), 16)
				kind = row[1].replace('kEH_', '')
				val = row[2]
				match kind:
					case 'Cat':
						cat[code] = val
					case 'Core':
						core[code] = val
					case 'Desc':
						desc[code] = val
					case 'Func':
						func[code] = val
					case 'FVal':
						fval[code] = val
					case 'UniK':
						unik[code] = simplify_unikemet_name(val)
					case 'JSesh':
						jsesh[code] = val
					case 'HG':
						hg[code] = val
					case 'IFAO':
						ifao[code] = val
					case 'NoMirror':
						nomirror[code] = val
					case 'NoRotate':
						norotate[code] = val
					case 'AltSeq':
						altseq[code] = val
					case _:
						print('Unrecognized kind', kind)
	return {'cat': cat,
		'core': core,
		'desc': desc,
		'func': func,
		'fval': fval,
		'unik': unik,
		'jsesh': jsesh,
		'hg': hg,
		'ifao': ifao,
		'nomirror': nomirror,
		'norotate': norotate,
		'altseq': altseq}

def read_unikemet_to_code(filename):
	code_to_unikemet = {}
	with open(filename, 'r') as f:
		datareader = csv.reader(f, delimiter=' ')
		for row in datareader:
			code_to_unikemet[int(row[1], 16)] = row[0]
	return code_to_unikemet

def read_unikemet_to_code_multiple(filenames):
	code_to_unikemet = {}
	for filename in filenames:
		code_to_unikemet.update(read_unikemet_to_code(filename))
	return code_to_unikemet

def read_codes(filename):
	codes = []
	with open(filename, 'r') as f:
		datareader = csv.reader(f)
		for row in datareader:
			codes.append(int(row[0], 16))
	return codes

def restrict_code_map_range(code_map, min_code, max_code):
	copy_map = {}
	for key, val in code_map.items():
		if key >= min_code and key <= max_code:
			copy_map[key] = val
	return copy_map

def make_core_status(tables):
	cat = tables['cat']
	core = tables['core']
	core_status = {}
	for code in cat:
		if code not in core:
			core_status[code] = 'N'
		elif core[code] == 'L':
			core_status[code] = 'L'
		elif core[code] == 'C':
			core_status[code] = 'C'
		else:
			print('Wrong core status', f'0x{code:X}', core[code])
	return core_status

def check_unikemet_unique(tables):
	unik = tables['unik']
	unik_to_codes = defaultdict(list)
	for code in unik:
		unik_to_codes[unik[code]].append(code)
	for code in sorted(unik):
		if len(unik_to_codes[unik[code]]) > 1:
			print('Name clash', f'0x{code:X}', unik[code])

def check_unikemet_basic_list(tables):
	mapping1 = read_unikemet_to_code_multiple([
		'../tables/unicode15hieroglyphs.csv',
		'../tables/unicode15opencaps.csv', 
		'../tables/unicode15closecaps.csv'])
	mapping2 = restrict_code_map_range(tables['unik'],
		BASIC_START, BASIC_END)
	if len(mapping1) != len(mapping2):
		print('Numbers of names in basic list differ')
	for code in sorted(mapping1):
		if mapping1[code] != mapping2[code]:
			print('Unikemet name mismatch', f'0x{code:X}', mapping1[code], mapping2[code])

def check_core_descriptions(tables):
	desc = tables['desc']
	core_status = make_core_status(tables)
	for code in sorted(core_status):
		if code > BASIC_END and core_status[code] == 'C' and code not in desc:
			print('Missing description', f'0x{code:X}')

def check_omitted(tables):
	core_status = make_core_status(tables)
	omitted_from_font = read_codes('../tables/omitted.csv')
	noncores = [code for code in core_status if core_status[code] == 'N']
	if len(noncores) != len(omitted_from_font):
		print('Wrong number of non-core signs omitted', len(noncores), len(omitted_from_font))
	diff1 = list(set(noncores) - set(omitted_from_font))
	diff2 = list(set(omitted_from_font) - set(noncores))
	if len(diff1) > 0:
		print('Noncores not omitted', [f'0x{code:X}' for code in diff1])
	if len(diff2) > 0:
		print('Omitted not noncores', diff2)

if __name__ == '__main__':
	tables = read_unikemet('../tables/Unikemet-16.0.0.txt')
	check_unikemet_unique(tables)
	check_unikemet_basic_list(tables)
	check_core_descriptions(tables)
	check_omitted(tables)
