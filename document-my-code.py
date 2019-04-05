#
# Flags:
#  - "-l" -> language

import sys, re;

def main(args):
	if not validateArgs(args): return -1;

	language        = args[2];
	input_filename  = args[3];
	output_filename = args[4];

	settings = getSettingsForLanguage(language);

	file_contents = importFile(input_filename);

	results = [];

	for line in file_contents:
		line_result = re.search(settings['regex_string'], line);
		if line_result:
			results.append(line_result.group());
			print(line_result.group());

	function_info = parseFunctionStrings(results, language);

	comments = [];

	for info in function_info:
		comment = createBlockComment(info, settings);
		comments.append(comment);

	outputFile(output_filename, comments);






def validateArgs(args):

	ret = True;

	supported_languages = ["C", "Python"];
	usage_str = "Usage: python3 document-my-code.py -l [language] [input filename] [output filename]";

	if len(args) != 5:
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
		settings['regex_string']        = "((\\w)+[*]*\\s+(\\w)+(\\()((\\w)*[*]*(\\s)+(\\w)*(,)*)*(\\))({)*)";
	elif language == "Python":
		settings['inline_comment']      = "# ";
		settings['start_block_comment'] = "# ";
		settings['mid_block_comment']   = "# ";
		settings['end_block_comment']   = "# ";
		settings['regex_string']        = "d{1}e{1}f{1}\\s+\\w+\\(\\w*\\):{1}";


	return settings;


def parseFunctionStrings(results, language):
	
	function_info = [];

	if language == "C":
		for r in results:
			function = {};
			space_spl = r.split(" ", 1);
			function['return_type'] = space_spl[0];
			bracket_spl = space_spl[1].split("(", 1);
			function['name'] = bracket_spl[0];

			param_str = bracket_spl[1].replace(")", "");
			
			if "{" in param_str:
				param_str = param_str.replace("{", "");

			params = param_str.split(",");

			params = [x.lstrip() for x in params];

			function['parameters'] = params;

			function_info.append(function);
	elif language == "Python":
		for r in results:
			function = {};
			function['return_type'] = "";
			
			param_spl = r.split("(", 1);
			param_spl2 = param_spl[1].split(")", 1);
			param_str = param_spl2[0].split(",");
			param_str = [x.lstrip() for x in param_str];
			function['parameters'] = param_str;

			name_str = param_spl[0].split(" ");
			function['name'] = name_str[1];

			function_info.append(function);
	else:
		print("Language error.");


	return function_info;



def createBlockComment(func_info, settings):
	print("LEN: "+ str(len(func_info['parameters'])))
	comment_str  = settings['start_block_comment'] + func_info['name'] + ": \n" + settings['mid_block_comment'] + "\n";
	if len(func_info['parameters']) > 0:
		comment_str += settings['mid_block_comment']   + "Params: " + "\n";
		
		longest_param_ind = 0;
		longest_param_len = 0;
		for i in range(0, len(func_info['parameters'])):
			if len(func_info['parameters'][i]) > longest_param_len :
				longest_param_len = len(func_info['parameters'][i])
				longest_param_ind = i;

		

		for i in range(0, len(func_info['parameters'])):
			space_str = "    ";
			pre_arrow_str = "  ";
			if i != longest_param_ind:
				diff = longest_param_len - len(func_info['parameters'][i]);
				print(diff);
				for j in range (0, diff):
					pre_arrow_str += " ";
			
			comment_str += settings['mid_block_comment'] + space_str + func_info['parameters'][i] + pre_arrow_str + "->  \n";


	comment_str += settings['mid_block_comment'] + "Returns: \n" + settings['mid_block_comment'] + "    " + func_info['return_type'] + "  ->  \n";
	comment_str += settings['end_block_comment'] + "\n";

	return comment_str;



def importFile(fn):
	with open(fn) as f:
		content = f.readlines();
		content = [x.strip() for x in content]; 
		return content;

	return [];


def outputFile(fn, contents):
	fp = open(fn, "w");

	for line in contents:
		print(line);
		fp.write(line);
		fp.write("\n\n");


main(sys.argv);