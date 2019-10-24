
import os, sys, glob, re
import accunroll
import string


tokenize_delim = ""

def load_tokenize_delim():
	global tokenize_delim

	tokenize_delim = string.punctuation
	tokenize_delim = tokenize_delim.replace("_", " ")
	tokenize_delim = tokenize_delim + "\t\n"



def readfile(filename):
	"""
	Loading file and taking care of "\" at the end of #pragma lines	
	Input: filename
	Output: list of transformed lines
	"""
	f = open(filename, "r")
	new_lines = list()
	t = ""
	i = 0
	lines = f.readlines()
	LEN = len(lines)
	while i < LEN:
		l = lines[i]
		s = l.rstrip()
		if len(s) == 0:
			new_lines.append("")
			i += 1
			continue

		t = s
		if s[-1] == "\\" and "#pragma" in s:
			t = ""
			while s[-1] == "\\":
				t += s[:-1]
				i += 1
				s = lines[i].rstrip()
			t += s

		new_lines.append(t)

		i += 1

	f.close()

	return new_lines


def generate_temp_variables(var_type, var_name, spaces):
	new_var_name = var_name.replace("->", "_")
	new_var_name = new_var_name.replace(".", "_")
	new_var_name = new_var_name.replace("[", "_")
	new_var_name = new_var_name.replace("]", "_")
	new_var_name = "__" + new_var_name + "__"
	final_decl = ""
	if "restrictconst" in var_type:
		var_type = var_type.split(":")[0].strip()
		final_decl = "%s%s restrict const %s = %s;" % (spaces, var_type, new_var_name, var_name)
	elif "restrict" in var_type:
		var_type = var_type.split(":")[0].strip()
		final_decl = "%s%s restrict %s = %s;" % (spaces, var_type, new_var_name, var_name)
	else:
		final_decl = "%s%s %s = %s;" % (spaces, var_type, new_var_name, var_name)
	return final_decl, new_var_name


def count_tab_space_from_begining(line):
	count = ""
	for c in line:
		if c == ' ' or c == '\t':
			count += c
		else:
			break
	return count

def print_usage():
	print "\t\t\tThe correct method to declare is following:"
	print "\t\t\t#pragma pointerchain declare(<variable_name>{variable_type},...)"
	print "\t\t\tExample:"
	print "\t\t\t#pragma pointerchain declare(t->arr{double}, t->arr2{int})"
	exit(0)


def find_declares(lines):
	i = 0
	converted_lines = list()
	LEN = len(lines)
	map_of_variables = dict()
	map_varname_vartype = dict()

	while i < LEN:
		l = lines[i]
		matches = re.finditer(r"#pragma[ ]+pointerchain[ ]+declare\((?P<declare_def>.+)\)", l)
		len_matches = 0
		list_of_temp = list()

		for m in matches:
			len_matches += 1
			def_list = m.group("declare_def").split(",")

			for d in def_list:
				d = d.strip()
				if "{" not in d or "}" not in d:
					print "\t===Variable name/type is incorrect."
					print_usage()

				variables = re.finditer(r"\s*(?P<var_name>.*)\{(?P<var_type>.*)\}\s*", d)
				for v in variables:
					var_name = v.group("var_name")
					var_type = v.group("var_type")

					if var_name == "":
						print "No variable name for Line %d\n%s\n" % (i+1, l)
						exit(0)
					if var_type == "":
						print "No variable type for Line %d\n%s\n" % (i+1, l)
						exit(0)

					final_decl, new_var_name = generate_temp_variables(var_type, var_name, count_tab_space_from_begining(l))
					list_of_temp.append(final_decl)
					map_of_variables[var_name] = new_var_name
					map_varname_vartype[var_name] = var_type



		if len_matches > 0:
			converted_lines.append("//" + l)
			for tmp in list_of_temp:
				converted_lines.append(tmp)
		else:
			converted_lines.append(l)

		i += 1


	return converted_lines, map_of_variables, map_varname_vartype


def is_alpha_numeric(input_string):
	for ch in input_string:
		b1 = ch >= '0' and ch <= '9'
		b2 = ch >= 'a' and ch <= 'z'
		b3 = ch >= 'A' and ch <= 'Z'
		b4 = ch == '_'
		if b1 or b2 or b3 or b4:
			continue
		return False
	return True

def find_regions(lines, map_of_variables, map_varname_vartype):
	i = 0
	converted_lines = list()
	LEN = len(lines)

	list_of_old_vars = map_of_variables.keys()

	used_variables = list()
	scalar_lines = list()

	start_converting = False
	while i < LEN:
		l = lines[i]

		res = re.search(r"#pragma[ ]+pointerchain[ ]+region[ ]+begin", l)
		if res is not None:
			start_converting = True
			used_variables = list()
			l = "//" + l
			converted_lines.append(l)
			i += 1
			continue

		res = re.search(r"#pragma[ ]+pointerchain[ ]+region[ ]+end", l)
		if res is not None:
			start_converting = False
			for k in used_variables:
				var_type = map_varname_vartype[k]
				if "*" not in var_type:
					s = "%s%s = %s;" % (count_tab_space_from_begining(l), k, map_of_variables[k])
					scalar_lines.append(s)
			used_variables = list()
			l = "//" + l
			converted_lines.append(l)
			i += 1
			continue


		if start_converting:

			for k in list_of_old_vars:
				starting_index = 0
				while True:
					ind = l.find(k, starting_index)
					if ind == -1:
						break

					# make sure we are replace a variable and not a subset of its name
					b1 = True
					if ind+len(k)<len(l):
						b1 = b1 and not is_alpha_numeric(l[ind+len(k)])
					if ind-1>=0:
						b1 = b1 and not is_alpha_numeric(l[ind-1])

					if b1:
						l = l[:ind] + map_of_variables[k] + l[ind+len(k):]
						if k not in used_variables:
							used_variables.append(k)
						starting_index += len(map_of_variables[k])
					else:
						starting_index += len(k)

			converted_lines.append(l)

		else:
			converted_lines.append(l)
			for sl in scalar_lines:
				converted_lines.append(sl)
			scalar_lines = list()

		i += 1

	return converted_lines


def generate_tmp_name(filename):
	return "__%s.tmp" % (filename)


def generate_original_name(filename):
	return "__%s.orig" % (filename)


def copy_files(file_from, file_to):
	file1 = open(file_from, "r")
	file2 = open(file_to, "w")
	for l in file1.readlines():
		file2.write(l)
	file1.close()
	file2.close()


def save_in_file(filename, lines):
	f = open(filename, "w")
	for l in lines:
		f.write("%s\n" % (l))
	f.close()




def convert_forward(filename):
	lines = readfile(filename)
	lines, map_of_variables, map_varname_vartype = find_declares(lines)
	lines = find_regions(lines, map_of_variables, map_varname_vartype)

	tmp_filename = generate_tmp_name(filename)
	save_in_file(tmp_filename, lines)

	accunroll.unroll(tmp_filename, tmp_filename)

	orig_filename = generate_original_name(filename)
	copy_files(filename, orig_filename)

	copy_files(tmp_filename, filename)




def convert_backward(filename):
	orig_filename = generate_original_name(filename)
	if not os.path.exists(orig_filename):
		return

	copy_files(orig_filename, filename)
	os.remove(orig_filename)
	os.remove(generate_tmp_name(filename))




def get_all_source_files(folder):
	ext_list = ["h", "hpp", "c", "cpp"]
	file_list = list()
	for ext in ext_list:
		file_list += glob.glob("*.%s" % (ext))

	final_list = list()
	for filename in file_list:
		lines = readfile(filename)
		for l in lines:
			res1 = re.search(r"#pragma[ ]+pointerchain[ ]+region[ ]+begin", l)
			res2 = re.search(r"#pragma[ ]+pointerchain[ ]+region[ ]+end", l)
			res3 = re.search(r"#pragma[ ]+pointerchain[ ]+declare[\s*]", l)
			if res1 is not None or res2 is not None or res3 is not None:
				final_list.append(filename)
				break


	return final_list


def find_direction(argv):
	direction = ""
	if len(argv) >= 2:
		if argv[1] == "forward":
			direction = "forward"
		elif argv[1] == "backward":
			direction = "backward"

	if direction == "":
		print "Choose direction: forward, backward."
		exit(0)

	return direction


def check_previous_forwarding(file_list):
	# guarding duplicate changes
	for filename in file_list:
		tmp_filename = generate_tmp_name(filename)
		if os.path.exists(tmp_filename):
			print "Temporary file for %s already exists (%s). It means we have the forwared already. Please try again.\n" % (filename, tmp_filename)
			exit(0)


def check_previous_backwarding(file_list):
	# check to see whether all the files exists or not
	list_of_files_to_convert = list()
	for filename in file_list:
		tmp_filename = generate_tmp_name(filename)
		if os.path.exists(tmp_filename):
			list_of_files_to_convert.append(tmp_filename)
	if len(list_of_files_to_convert) == 0:
		print "No files to convert! Probably you need to do 'forward' operation first!\n"
		exit(0)


def main():
	load_tokenize_delim()

	direction = find_direction(sys.argv)


	current_folder = os.path.abspath(".")
	file_list = get_all_source_files(current_folder)


	if direction == "forward":
		check_previous_forwarding(file_list)
	elif direction == "backward":
		check_previous_backwarding(file_list)


	for filename in file_list:
		if direction == "forward":
			print "Converting forward:", filename
			convert_forward(filename)
		elif direction == "backward":
			print "Converting backward:", filename
			convert_backward(filename)


if __name__ == '__main__':
	main()
