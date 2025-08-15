import re

TESTSUITE = '../tables/functionstestsuite.txt'

FUNCTION_STRING = r'[A-Z][^|":\s]+'
TRANSCRIPTION_STRING = r'[\U00013000-\U000143FF\s/]*'
DESCRIPTION_STRING = r'[^\|"]+'
TRANSLITERATION_STRING = r'[^|":\[\];]*'
TRANSLATION_STRING = r'[^|":\[\];]*'

def join_spaced(*args):
	return ' '.join(' '.join([str(a) for a in args]).split())

class UniTranscriptions:
	def __init__(self, transcriptions):
		for t in transcriptions:
			if not re.fullmatch(rf'{TRANSCRIPTION_STRING}', t):
				print('Not allowable transcription:', t)
		self.transcriptions = transcriptions

	@classmethod
	def from_string(cls, s):
		return UniTranscriptions([part.strip() for part in s.strip().split('/') if part.strip()] \
				if s is not None else [])

	def __str__(self):
		return ' / '.join(self.transcriptions)

class UniDescriptions:
	def __init__(self, descriptions):
		for d in descriptions:
			if not re.fullmatch(rf'{DESCRIPTION_STRING}', d):
				print('Not allowable description:', d)
		self.descriptions = descriptions

	@classmethod
	def from_string(cls, s):
		return UniDescriptions(re.findall(r'"(.*?)"\s*(?:/\s*|$)', s) if s is not None else [])

	def __str__(self):
		return ' / '.join(['"' + d + '"' for d in self.descriptions])

class UniTransliterations:
	def __init__(self, transliterations):
		if not re.fullmatch(rf'{TRANSLITERATION_STRING}', transliterations):
			print('Not allowable transliterations:', transliterations)
		self.transliterations = transliterations

	@classmethod
	def from_string(cls, s):
		return UniTransliterations(s.strip() if s is not None else '')

	def __str__(self):
		return self.transliterations

class UniTranslations:
	def __init__(self, translations):
		if not re.fullmatch(rf'{TRANSLATION_STRING}', translations):
			print('Not allowable translations:', translations)
		self.translations = translations

	@classmethod
	def from_string(cls, s):
		return UniTranslations(s.strip() if s is not None else '')

	def __str__(self):
		return ': ' + self.translations if self.translations != '' else ''

class UniExample:
	def __init__(self, transcriptions, transliterations, translations):
		self.transcriptions = transcriptions
		self.transliterations = transliterations
		self.translations = translations

	@classmethod
	def from_string(cls, s):
		result = re.search( \
			rf'^({TRANSCRIPTION_STRING})' # transcriptions
			r'([^:]*)' # transliterations
			r'(?::(.*))?$' # translations
			, s.strip())
		if result:
			transcriptions = UniTranscriptions.from_string(result.group(1))
			transliterations = UniTransliterations.from_string(result.group(2))
			translations = UniTranslations.from_string(result.group(3))
			return UniExample(transcriptions, transliterations, translations)
		else:
			print('Could not parse example:', s)
			return None

	def __str__(self):
		return join_spaced(self.transcriptions, self.transliterations) + str(self.translations)

class UniExamples:
	def __init__(self, examples):
		self.examples = examples

	@classmethod
	def from_string(cls, s):
		return UniExamples([UniExample.from_string(part) for part in s.split(';') if part.strip()] \
				if s is not None else [])

	def __str__(self):
		return (' [' + '; '.join([str(e) for e in self.examples]) + ']') if len(self.examples) > 0 else ''

class UniFunction:
	def __init__(self, transcriptions, function_name, descriptions, transliterations, translations, examples):
		if not re.fullmatch(rf'{FUNCTION_STRING}', function_name):
			print('Not allowable function name:', "X" + function_name + "Y")
		self.transcriptions = transcriptions
		self.function_name = function_name
		self.descriptions = descriptions
		self.transliterations = transliterations
		self.translations = translations
		self.examples = examples

	@classmethod
	def from_string(cls, s):
		result = re.search( \
			rf'^({TRANSCRIPTION_STRING})' # transcriptions
			rf'({FUNCTION_STRING})' # function name
			r'(\s+"[^"]+"(?:\s*/\s*"[^"]+")*)?' # descriptions
			r'(\s+[^:\[]+)?' # transliterations
			r'(?:\s*:([^:\[]+))?' # translations
			r'(?:\s*\[([^\]]*)\])?\s*$' # examples
			, s.strip())
		if result:
			transcriptions = UniTranscriptions.from_string(result.group(1))
			function_name = result.group(2)
			descriptions = UniDescriptions.from_string(result.group(3))
			transliterations = UniTransliterations.from_string(result.group(4))
			translations = UniTranslations.from_string(result.group(5))
			examples = UniExamples.from_string(result.group(6))
			return UniFunction(transcriptions, function_name, descriptions,
				transliterations, translations, examples)
		else:
			print('Could not parse function:', s)
			return None

	def __str__(self):
		return join_spaced(join_spaced(self.transcriptions, self.function_name, \
			self.descriptions, self.transliterations) + str(self.translations), self.examples)

class UniFunctions:
	def __init__(self, functions):
		self.functions = functions

	@classmethod
	def from_string(cls, s):
		return UniFunctions([UniFunction.from_string(part) for part in s.split('|') if part.strip()])

	def __str__(self):
		return ' | '.join([str(f) for f in self.functions])

def test_parsing(filename):
	with open(filename, 'r') as f:
		for line in f:
			converted = str(UniFunctions.from_string(line))
			line = line.strip()
			if line != converted:
				print('Parsing does not preserve string')
				print(line)
				print(converted)

FUNCTION_NAME = rf'{FUNCTION_STRING}\s*'
DESCRIPTION = rf'"{DESCRIPTION_STRING}"\s*'
DESCRIPTIONS_OPT = rf'(|{DESCRIPTION}(/\s*{DESCRIPTION})*)'
TRANSLITERATION = rf'{TRANSLITERATION_STRING}\s*'
TRANSLITERATIONS_OPT = rf'(|{TRANSLITERATION}(/\s*{TRANSLITERATION})*)'
TRANSLATION = rf'{TRANSLATION_STRING}+\s*'
TRANSLATIONS_OPT = rf'(|:\s*{TRANSLATION}(/\s*{TRANSLATION})*)'
EXAMPLE = rf'{TRANSCRIPTION_STRING}{TRANSLITERATIONS_OPT}{TRANSLATIONS_OPT}'
EXAMPLES_OPT = rf'(\[\s*{EXAMPLE}(;\s*{EXAMPLE})*\]\s*)?'
FUNCTION = rf'{TRANSCRIPTION_STRING}{FUNCTION_NAME}{DESCRIPTIONS_OPT}{TRANSLITERATIONS_OPT}{TRANSLATIONS_OPT}{EXAMPLES_OPT}'
FUNCTIONS_OPT = rf'\s*(|{FUNCTION}(\|\s*{FUNCTION})*)'

def is_functions(s):
	return re.fullmatch(FUNCTIONS_OPT, s)

def test_regex(filename):
	with open(filename, 'r') as f:
		for line in f:
			if not is_functions(line):
				print('Cannot parse:', line)

if __name__ == '__main__':
	test_parsing(TESTSUITE)
	test_regex(TESTSUITE)
	print(FUNCTIONS_OPT)
