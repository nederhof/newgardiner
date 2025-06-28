import re
from unikemet import read_unikemet
from unifunctions import UniTranscriptions, UniDescriptions, \
	UniTransliterations, UniTranslations, UniExamples, UniFunction, UniFunctions

# Remove leading/trailing spaces.
# Then remove one outer bracket pair if present.
def strip_all(s):
	s = s.strip()
	match = re.match('\\((.*)\\)', s)
	if match:
		s = match.group(1)
	return s

def desc(s):
	return UniDescriptions([strip_all(s)] if s.strip() != '' else [])

def al(s):
	return UniTransliterations(s)

def tr(s):
	return UniTranslations(s)

def empty_hi():
	return UniTranscriptions('')

def empty_desc():
	return UniDescriptions([])

def empty_al():
	return UniTransliterations('')

def empty_tr():
	return UniTranslations('')

def empty_ex():
	return UniExamples([])

def log_phon(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Logogram/Phonemogram', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def log_class(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Logogram/Classifier', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def log(val, sem):
	val = val.replace('|', '/')
	sem = sem.replace(';', ',')
	return UniFunctions([UniFunction(empty_hi(), 'Logogram', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def log_uncertain(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Logogram(uncertain)', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def phon_log(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Phonemogram/Logogram', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def phon_phonrep(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Phonemogram/Phono-repeater', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def phon_class(val, sem):
	val = val.replace('|', '/')
	return UniFunctions([UniFunction(empty_hi(), 'Phonemogram/Classifier', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def phon(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Phonemogram', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def phon_crypt(val, sem):
	val = val.replace(';', '/')
	return UniFunctions([UniFunction(empty_hi(), 'Phonemogram(cryptography)', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def class_log(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Classifier/Logogram', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def class_phonrep(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Classifier/Phono-repeater', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def classifier(val, sem):
	val = val.replace('|', '/')
	val = val.replace(';', ',')
	return UniFunctions([UniFunction(empty_hi(), 'Classifier', \
		desc(sem), al(val), empty_tr(), empty_ex())])

def phonrep(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Phono-repeater', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def rad(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Radicogram', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def inter(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Interpretant', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def pict(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Pictogram', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def uncertain(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Uncertain', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def substitute(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Substitute', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def number(val, sem):
	return UniFunctions([UniFunction(empty_hi(), 'Number', \
		empty_desc(), al(val), tr(sem), empty_ex())])

def gather_converted(code, old_func, old_val, new_func, gathered):
	gathered.append({'code': code, 'old_func': old_func, 'old_val': old_val, 'new_func': new_func})

def extract_functions():
	# tables = read_unikemet('../tables/Unikemet-16.0.0.txt')
	tables = read_unikemet('../tables/Unikemet16revised.txt')
	cat = tables['cat']
	func = tables['func']
	fval = tables['fval']
	converted = []
	sorted_points = sorted(func, key=func.get)
	for code in sorted_points:
		f = func[code]
		v = fval[code] if code in fval else ''
		if code == 0x133D4:
			d = UniDescriptions(['bread', 'Festival'])
			f1 = UniFunction(empty_hi(), 'Classifier', d, empty_al(), empty_tr(), empty_ex())
			f2 = UniFunction(empty_hi(), 'Phonemogram', empty_desc(), al('t'), empty_tr(), empty_ex())
			f3 = UniFunction(empty_hi(), 'Logogram', empty_desc(), al('t'), tr('bread'), empty_ex())
			f4 = UniFunction(empty_hi(), 'Phono-repeater', empty_desc(), al('sn / fḳꜣ'), empty_tr(), empty_ex())
			gather_converted(code, f, v, UniFunctions([f1,f2,f3,f4]), converted)
			continue
		match = re.match('^Logogram/[pP]honemogram(.*)$', f)
		if match:
			arg = strip_all(match.group(1))
			gather_converted(code, f, v, log_phon(v, arg), converted)
			continue
		match = re.match('^Logogram/[cC]lassifier(.*)$', f)
		if match:
			arg = strip_all(match.group(1))
			gather_converted(code, f, v, log_class(v, arg), converted)
			continue
		match = re.match('^Logogram(.*)$', f)
		if match:
			arg = strip_all(match.group(1))
			gather_converted(code, f, v, log(v, arg), converted)
			continue
		match = re.match('^\\?Logogram(.*)$', f)
		if match:
			arg = strip_all(match.group(1))
			gather_converted(code, f, v, log_uncertain(v, arg), converted)
			continue
		match = re.match('^Phonemogram/[lL]ogogram(.*)$', f)
		if match:
			arg = strip_all(match.group(1))
			gather_converted(code, f, v, phon_log(v, arg), converted)
			continue
		match = re.match('^Phonemogram/phono-repeater(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, phon_phonrep(v, arg), converted)
			continue
		match = re.match('^Phonemogram/classifier(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, phon_class(v, arg), converted)
			continue
		match = re.match('^Phonemogram or Classifier(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, phon_class(v, arg), converted)
			continue
		match = re.match('^Phonemogram \\(cryptography\\)(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, phon_crypt(v, arg), converted)
			continue
		match = re.match('^Phonemogram(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, phon(v, arg), converted)
			continue
		match = re.match('^\\(cryptography\\) Phonemogram(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, phon_crypt(v, arg), converted)
			continue
		match = re.match('^Classifier/logogram(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, class_log(v, arg), converted)
			continue
		match = re.match('^Classifier/phono-repeater(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, class_phonrep(v, arg), converted)
			continue
		match = re.match('^[cC]lasss?ifier?(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, classifier(v, arg), converted)
			continue
		match = re.match('^Phono-repeater(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, phonrep(v, arg), converted)
			continue
		match = re.match('^Radicogram(.*)$', f)
		if match:
			arg = strip_all(match.group(1))
			gather_converted(code, f, v, rad(v, arg), converted)
			continue
		match = re.match('^Interpretant(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, inter(v, arg), converted)
			continue
		match = re.match('^Pictogram(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, pict(v, arg), converted)
			continue
		match = re.match('^\\?(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, uncertain(v, arg), converted)
			continue
		match = re.match('^Uncertain(.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, uncertain(v, arg), converted)
			continue
		match = re.match('^Substitute for (.*)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, substitute(v, arg), converted)
			continue
		match = re.match('^\\\\?([0-9]+)$', f)
		if match:
			arg = match.group(1)
			gather_converted(code, f, v, number(v, arg), converted)
			continue
		match = re.match('^spindle/spinning tool$', f)
		if match:
			gather_converted(code, f, v, log('', 'spindle/spinning tool'), converted)
			continue
		print('Unexpected function:', f)
	return converted

if __name__ == '__main__':
	converted = extract_functions()
	for conv in converted:
		code = conv['code']
		print(f'U+{code:X} FUN', conv['old_func'])
		if conv['old_val']:
			print(f'U+{code:X} VAL', conv['old_val'])
		print(f'U+{code:X} NEW', conv['new_func'])
		print('--')
