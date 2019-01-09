__author__ = 'Hanumanth Reddy'
__version__ = 'Python 2.7'

import os
import re 
import time

from sys import argv

script, input_file_name, root_lib = argv

# Check for the root_lib 
if not os.path.exists(root_lib):
	print "Incorrect source library"
else:
	# Create a temp library for script reports if doesn't exists
	temp_python_lib = os.path.join(root_lib, "python_work_lib") 	
	#print temp_python_lib
	if not os.path.exists(temp_python_lib):
		os.makedirs(temp_python_lib)
		#print "Library created"

fileList = os.listdir(root_lib) 
#print fileList
top_cl_list_file = os.path.join(root_lib,"#ABC.txt")
top_cl_list_file_open = open(top_cl_list_file)
for top_cl in top_cl_list_file_open:
	print "top CL", top_cl
	input_file_name = top_cl.strip()
	list_of_unique_programs = [input_file_name]
	list_of_CL_programs = []
	list_of_RPG_programs = []
	list_of_CBL_programs = []
	list_of_copybooks = [] 
	list_of_programs = [input_file_name]
	sources_not_found = []
	copybook_not_found = []
	call_tree = {}
	i = 0
	
	print list_of_unique_programs
	while i < len(list_of_unique_programs):
		#for program_name in list_of_programs:
		program_name = list_of_unique_programs[i]
		i += 1
		#for dirName, subdirList, fileList in os.walk(root_lib):
		file_name = program_name + ".txt"
		print "Start processsing of ", file_name	
		if file_name in fileList:
			file_path = os.path.join(root_lib, file_name) 
			call_tree[program_name] = []                # Dictonary of the call tree  
			print file_path
			file_open = open(file_path, 'rb')
			file_data = file_open.read()
			#print file_data
			if 'PGM' in file_data and 'ENDPGM' in file_data:
				print "CL program"
				list_of_CL_programs.append(program_name) 		
				#  Its a "CL program" remove the commented lines to make the data with valid codei.e /*...*/ 
				regex = re.compile(r'\/\*.*?\*\/', re.DOTALL)
				text = regex.sub("", file_data)
				
				# Write the new contents to temporary for easy access of the data 
				temp_dump_file = os.path.join(temp_python_lib, "dump.txt")
				file1 = open(temp_dump_file,"wb")			
				for data in text:
					if data == '\n':
						file1.write("\n")
					file1.write(data)		
				file1.close()
							
				file1 = open(temp_dump_file,'rb')

							# The possible syntax for calling a program
							#   1. CALL PGM(PGM_NAME)
							#	2. CALL PGM(Lib_Name/PGM_Name)
							#   3. CALL PGM(*LIBL/PGM_NAME)	 	
							#	4. CALL PGM_NAME
				regex1 = re.compile(r'call\s+(pgm\((.*\/)?)?([\w@#$]+)+?\)?')
				pgm_list = regex1.findall(file1.read().lower())
				print len(pgm_list)	
				for item in pgm_list:
					print item, len(item)
					if len(item) == 3:
						list_of_programs.append(item[2].upper())	
						if item[2].upper() not in list_of_unique_programs:
							list_of_unique_programs.append(item[2].upper())
						call_tree[program_name].append(item[2].upper())
						#call_tree.append((program_name, item[2].upper()))
						
				file1.close()
				file_open.close()
					
				#break					
			else:
				pgm_copybook_list = []
				while True:
						# Remove comments section
						# comments ==> 20th position of a line should be '*'
					file1_open = open(file_path,'rb')
						#print file1_open.readline()
					for file_line in file1_open:
						if len(file_line) >= 7:
							if file_line[6] != '*':
								if program_name not in list_of_RPG_programs and program_name not in list_of_CBL_programs:		
									if file_line[5].upper() in ['H','F','D','C','I', 'C','O']:
										list_of_RPG_programs.append(program_name)
									else:
										if program_name not in list_of_CBL_programs:
											list_of_CBL_programs.append(program_name)	
		
								if 'call' in file_line.lower():
									#print "Inner most"
									# Identify the type of program								
									# End of programs identification	
									regex = re.compile(r'call\s+[\"\']+([\w@#$]+)+[\"\']+')
									pgm_list = regex.findall(file_line.lower())
										#print pgm_list, len(pgm_list) 
									if len(pgm_list) != 0:
										list_of_programs.append(pgm_list[0].upper())
										if pgm_list[0].upper() not in list_of_unique_programs:
											list_of_unique_programs.append(pgm_list[0].upper())		
										call_tree[program_name].append(pgm_list[0].upper())
											#call_tree = (program_name, pgm_list[0].upper())
								elif '/copy' in file_line.lower():				# Logic for reading the copybooks 
									regex = re.compile(r'/copy\s+([\w@#$]+[,]+)?([\w@#$]+)')
									pgm_copybook = regex.findall(file_line.lower())
									if len(pgm_copybook[0]) == 2:
										pgm_copybook_list.append(pgm_copybook[0][1].upper())
										if pgm_copybook[0][1].upper() not in list_of_copybooks:
											list_of_copybooks.append(pgm_copybook[0][1].upper())
					# close the open file

					file1_open.close()
					if pgm_copybook_list != []:
						if pgm_copybook_list[0] + ".txt" in fileList:
							file_path = os.path.join(root_lib, pgm_copybook_list[0] + ".txt")
							pgm_copybook_list.remove(pgm_copybook_list[0])
						else:
							copybook_not_found.append(pgm_copybook_list[0])
							pgm_copybook_list.remove(pgm_copybook_list[0])
							break
							
					else:
						break
				
		if program_name not in call_tree:
			sources_not_found.append(program_name) 


	# Create an report file to store the complete stats data
	output_file = os.path.join(temp_python_lib,"Report_" + input_file_name + ".txt")
	output_file_open = open(output_file, "w")
	print output_file

	# Write the stats to the output file
	# Unique program list
	output_file_open.write("\n\n\t***********************************************************\n")
	output_file_open.write("\t**********           "+ input_file_name+ " Report           **********") 
	output_file_open.write("\n\t***********************************************************")
	output_file_open.write("\n\n\nList of unique programs called in the batch : %d \n " %len(list_of_unique_programs) )
	output_file_open.write("Program list : ") 
	for item in list_of_unique_programs:
		output_file_open.write("\n\t")
		output_file_open.write(item)
	print "Unique program list"		
		
	# Copy book details
	output_file_open.write("\n\n\nList of Copy books called in the batch : %d \n " %len(list_of_copybooks) )
	output_file_open.write("Copybook list : ") 
	for item in list_of_copybooks:
		output_file_open.write("\n\t")
		output_file_open.write(item) 		
	print "Copybook list"		
	
	
	# List of programs where source text files are not found
	output_file_open.write("\n\n\nList of programs with no sources available in the root directory: %d\n" %len(sources_not_found))
	output_file_open.write("Program list : ") 
	if len(sources_not_found) == 0:
		output_file_open.write("\n\t None ") 
	else:	
		for item in sources_not_found:
			output_file_open.write("\n\t")
			output_file_open.write(item)
			

	# List of copy book where source text files are not found
	output_file_open.write("\n\n\nList of copy books with no sources available in the root directory: %d\n" %len(copybook_not_found))
	output_file_open.write(" List : ") 
	if len(copybook_not_found) == 0:
		output_file_open.write("\n\t None ") 
	else:	
		for item in copybook_not_found:
			output_file_open.write("\n\t")
			output_file_open.write(item)			
	print "not found list"				

			
	# CL list
	output_file_open.write("\n\n\nList of CL programs called in the driver program : %d \n " %len(list_of_CL_programs) )
	output_file_open.write("Program list : ") 
	for item in list_of_CL_programs:
		output_file_open.write("\n\t")
		output_file_open.write(item) 	
	
	# RPG list
	output_file_open.write("\n\n\nList of RPG programs called in the driver program : %d \n " %len(list_of_RPG_programs) )
	output_file_open.write("Program list : ") 
	for item in list_of_RPG_programs:
		output_file_open.write("\n\t")
		output_file_open.write(item) 		
		
	# COBOL list
	output_file_open.write("\n\n\nList of COBOL programs called in the driver program : %d \n " %len(list_of_CBL_programs) )
	output_file_open.write("Program list : ") 
	for item in list_of_CBL_programs:
		output_file_open.write("\n\t")
		output_file_open.write(item) 		

	
	# List of all called programs
	output_file_open.write("\n\n\nList of Called programs for each program \n")
	output_file_open.write("Program list : ") 
	for item in call_tree.keys():
		output_file_open.write("\n\t")
		output_file_open.write(item + " :")
		output_file_open.write("\t")
		output_file_open.write("%r " %call_tree[item])	
		
#	print "start of call stack prep"
	#print call_tree
	# Write the call stack lists for each program

#	root_pgm = input_file_name
#	pgm_map = call_tree

#	final_map = [[root_pgm]]
#	calls_each_level = [1]

#	while True:
#		level_call_programs = 0	
#		no_new_entry_found = True
#		for i in range(len(final_map)):
#			try:
#				count = i
#				children = set(pgm_map[final_map[i][-1]])
#				if len(children) == 0:
#					continue
#				no_new_entry_found = False
#				append_to_this = final_map[i]
#				final_map.pop(i)
#
#				for node in children:
#					temp = append_to_this[:]
#					temp.append(node)
#					final_map.insert(count, temp)
#					count += 1
#					#level_call_programs += 1
#				# print final_map
#			except:
#				pass
#		#calls_each_level.append(level_call_programs)		
#		if no_new_entry_found:
#			break

#	output_file_open.write("\n\n\nCALL stack of the driver program :") 
#	output_file_open.write(input_file_name) 
#	print "End of call stack prep"
#	final_unique_map = [[]]
#	for i in final_map:
#		if i not in final_unique_map and i != []:
#			final_unique_map.append(i)
#			
#	for i in final_unique_map:
#		output_file_open.write("\n\t")
#		output_file_open.write("%r" %i)
#		
#	print "End of report"	
#	output_file_open.write("\n\n\t************* END OF REPORT *****************")