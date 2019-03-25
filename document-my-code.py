#
# Flags:
#  - "-l" -> language

import sys, re;

def main(args):
	if not validateArgs(args): return -1;

	language = args[2];

	settings = getSettingsForLanguage(language);

	file_contents = importFile(args[3]);

	for line in file_contents:
		res = re.findall(settings['regex_string'], line);
		if res:
			print(res);





def validateArgs(args):

	ret = True;

	supported_languages = ["C"];
	usage_str = "Usage: python3 document-my-code.py -l [language] [filename]";

	if len(args) != 4:
		ret = False;
		print("Invalid amount of command line arguments.\n" + usage_str);
		print("Supported languages: ", end='');
		for l in supported_languages:
			print(l, end='');
		print(".");
		return ret;

	language_tag_present = False;
	is_valid_language    = False;

	if args[1] == "-l" or args[1] == "-L":
		language_tag_present = True;

	if args[2] in supported_languages:
		is_valid_language = True;

	if not language_tag_present:
		ret = False;
		print("Invalid command line arguments. No language tag is present.\n" + usage_str);

	if not is_valid_language:
		ret = False;
		print("Invalid command line arguments. \""+ args[2]+"\" is not a supported language.");
		print("Supported languages: ", end='');
		for l in supported_languages:
			print(l, end='');
		print(".");

	return ret;


def getSettingsForLanguage(language):

	settings = {};

	if language == "C":
		settings['inline_comment']      = "// ";
		settings['start_block_comment'] = "/* ";
		settings['mid_block_comment']   = " * ";
		settings['end_block_comment']   = "*/ ";
		settings['regex_string']        = "(\\w)+[*]*\\s+(\\w)+(\\()((\\w)*[*]*(\\s)+(\\w)*(,)*)*(\\))({)*";
		

	return settings;


def importFile(fn):
	with open(fn) as f:
		content = f.readlines();
		content = [x.strip() for x in content]; 
		return content;

	return [];


main(sys.argv);