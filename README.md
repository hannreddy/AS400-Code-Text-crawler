# AS400-Code-Text-crawler

Project   : AS400 Code Analyzer
Author    : Hanumanth Reddy Aredla
Contact   : hannreddy@gmail.com
Platform  : Python 2.7


Overview:
      I was working on a requirement were all the AS400 program were in .txt files. To understand the call stack using .txt was hectic. To get these details sorted i have written this utility, which crawls through each text file and creates the call stack.
      
Usage:
    Copy all the sources in one single folder and create a text file named '#ABC.txt' with the details of the Program names for which the call stack is needed to be created. Typically these programs are the starting points to batch jobs.
   ** The reason for sources to be in the same folder is to reduce the performance and #ABC file is used to reduce the manual intervention.
   
   Parameters the utility requires:
            1. Path of the sources folder
 
 This utility gives information about the following:
 1. List of all programs called in the process
 2. If any program source not found
 3. List of CL,RPG,COBOL and Copybooks used
 4. Each program called program list
   
   
