
import os, sys

class ForLoopDesc:
	def __init__(self, t="", n="", l=0, u=0):
		self.var_type = t
		self.var_name = n
		self.var_lower_bound = l
		self.var_upper_bound = u

	def reset(self):
		self.var_type = ""
		self.var_name = ""
		self.var_lower_bound = 0
		self.var_upper_bound = 0


def apply_unrolling(unroll_region, desc):
	final_unrolled_code = []

	if len(unroll_region) == 0:
		return

	white_space = ""
	for c in unroll_region[1]:
		if c == ' ' or c == '\t':
			white_space += c
		else:
			break

	for i in range(desc.var_lower_bound, desc.var_upper_bound):
		final_unrolled_code.append(unroll_region[0])
		final_unrolled_code.append("%s%s %s = %d;\n" % (white_space, desc.var_type, desc.var_name, i))
		for x in range(len(unroll_region[1:])):
			final_unrolled_code.append(unroll_region[x+1])

	return final_unrolled_code


def unroll(filename_src, filename_dest):
	f = open(filename_src, "r")
	unroll_region = []
	begin_adding = False

	normal_lines = []

	desc = ForLoopDesc()

	for l in f.readlines():
		tokens = l.split()
		if len(tokens) > 0 and tokens[0] != "\\\\":
			if len(tokens) >= 3 and tokens[0] == "#pragma" and tokens[1] == "accunroll" and tokens[2] == "begin":
				desc = ForLoopDesc(tokens[3], tokens[4], int(tokens[5]), int(tokens[6]))
				begin_adding = True
				continue
			elif len(tokens) >= 3 and tokens[0] == "#pragma" and tokens[1] == "accunroll" and tokens[2] == "end":
				if not begin_adding:
					print "An end statement is found without a begin statement!"
					exit(1)
				final_unrolled_code = apply_unrolling(unroll_region, desc)
				for l in final_unrolled_code:
					normal_lines.append(l)
				desc.reset()
				begin_adding = False
				continue

		if begin_adding:
			unroll_region.append(l)
		else:
			normal_lines.append(l)

	f.close()

	f = open(filename_dest, "w")
	for l in normal_lines:
		f.write(l)
	f.close()


def main():
	unroll(sys.argv[1])

if __name__ == '__main__':
	main()
