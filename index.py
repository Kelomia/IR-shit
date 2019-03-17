#!/usr/bin/python
# -*- coding: utf-8 -*-

# Coded by Kelomia( Zimu ) in 2019-February
# Email：
#  kelomia@sina.com | zjiao7@hawk.iit.edu

import re
import os
import collections
import time

PunNum=['`','1','2','3','4','5','6','7','8','9','0','-','=',
        '~','!','@','#','$','%','^','&','*','(',')','_','+',
       '[',']',"|",'{','}',':',';','"',"'",'<','>','?',',',
       '.','/']
# A list of pun and number, used to delete them in files
  
# Building the StopWord list, And facing a problem of working successfully
#StopWords=['a','in','on','at','the','to']

class Index:
	
	path="./collection/"	# The direction of collection
	query=[]		# For query term
	index={}      		# The Final INDEX
	DocID={}		# The Doc Id Index------will not be necessary when this is working-------
	                                #                                                               |
	def __init__(self,path):	#				           			|
		self.path=path		# Address initializate as "./collection/"                       |
		self.buildIndex()	# Build the Index                                               |
	                                #                                                               |
	def buildIndex(self):		#                                                               |
		ID=1			# For counting the ID                                           |
		fw=open("The Index.txt","w+")	#                                                       |
		start =time.time()		# To check the running time                             |
		oldindex={}			# The Origin Index which is not sorted                  |
		files = os.listdir(self.path)   # List of files that to read                            |
		# This can sort the .txt with thier number                                      <-------|
		#files.sort(key=lambda x:int(x[5:-4]))# Sort the listdir with number not string <--------
		# The end of this func                                                          <-------|
		for fileId in files:			    #                                           |
			newlines=''			    #                                           |
			self.DocID[ID]=fileId		    # The DocID record done here ----------------		
			ID +=1				    # The ID++
			count =	1			    # For counting position                     
			fr=open(self.path + fileId,'r+')    # Opening the file one by one               
			lines = fr.readlines()       	    # Read lines                                                
			for line in lines:            	    # Processing the line one by one                            
				line=line.lower()           # Turn letters into lowercase                               
				for ch in PunNum:           # Remove/Delete the pun and numbers                         
					if ch in line:	    #					                        
						line=line.replace(ch,'')            #                                   
				line = line.split()         # Remove Space and turn line into words                     
				for each in line:           # Recoding the position of each word each time And					
					value =[]           # -mark word only once                                      
					if each in oldindex:			    #			                
						value=oldindex[each]                # Recoding in TEMP-INDEX            
					value.append(list([ID,count]))    # The FileId and position           
					oldindex[each]= value                       # -is the value of each key(word)   
					count += 1                                  # Position counting                 
						
			fr.close()			# Close the Read
		# Here begin is the part of sorting index
		for word in sorted(oldindex):       # Sorted the Temp-INDEX
			flag=0                          # Using as a flag in later
			value=[]                        # Value of each key in new(Final) INDEX
			Value=[]                        # Using as a temp-value
			for first in oldindex[word]:        # When the temp-Index is not empty
				if value==[]:			    # Taking the value of each key from it
					value=first                 # Since the value is recording as [FileID,Position]
				elif value[0]==first[0]:            # -in the temp-INDEX 
					value.append(first[1])      # Now is combining the Info of Position
				elif value[0]!=first[0]:            # *************************************
					flag=1                      # Taking the value from
					Value.append(value)         # -temp INDEX to the new
					value=[]                    # -INDEX
					value=first                 # *************************************
			if flag==1:             # This flag is used to mark if the word appear in many files
				Value.append(value) # If so, the Value-temp will take them correact
				value=Value         # And seng it to value at the final
			self.index[word]=value                   # Record the value of key
			fw.write(word+str(self.index[word])+'\n')
			fw.flush()
		end = time.time()
		print (str(end-start) + " second")
		#fw.write(str(oldindex))
		fw.close()
		
    
	def and_query(self, query_terms):
		fw=open("Result of query.txt","a+")
		self.query=[]
		#function for identifying relevant docs using the index
		flag = 0	# The marker <-----------------------------------------|
		count = 0	# The number of file that retrieved                    |
		result = []	# The final result                                     |
		if isinstance(query_terms,list):		# Check the input and mark
			for each in query_terms:
				each=each.lower()
				self.query.append(each)
				flag = 1
		elif isinstance(query_terms,str):
			self.query= query_terms
		if flag==1:
			tr=[]		# Using as an other temp to record the ans
			for query in self.query:
				if query in self.index:
					for item in self.index[query]:
						tempresult = item
						while(isinstance(tempresult,list)):
							tempresult = tempresult[0]
						tr.append(tempresult)
				if result==[]:
					result=tr
					tr=[]
				elif result !=[] and tr != []:
					
					print("THE RESULT:"+str(result))
					print("THE ANOTHER:"+str(tr))
					result =[ i for i in result if i in tr]
					tr=[]
				else:
					pass
		else:
			if self.query in self.index:
				for item in self.index[self.query]:
					tempresult = item[0]
					while(isinstance(tempresult,list)):
						tempresult = tempresult[0]
					count += 1
					result.append(tempresult)
					tempresult=[]
		print("The result of "+ str(self.query)+" is:")
		fw.write("The result of " + str(self.query) + " is\n")
		fw.write(str(len(result)) + " docs retrived:\n")
		print(str(len(result))+" docs retrieved:")
		for ans in result:
			print("The "+str(self.DocID[ans-1]))
			fw.write("The "+str(self.DocID[ans-1])+"\n")
		fw.write("\n")
		fw.flush()
		fw.close()
		print("\n\n")
			
	def print_dict(self):
		#function to print the terms and posting list in the index
		print("This is the index:")
		print( self.index )
	
	def print_doc_list(self):
		# function to print the documents and their document id
		print("This is the DocID File:")
		for Doc in self.DocID:
			print("The DocID: "+ str(Doc) +" --> "+ str(self.DocID[Doc]))
			

t=Index("./collection/")				# The sample of class Index t

t.and_query(['hans','customs','talent','currently'])	# Running the func and_query() from Class
t.and_query(['with','without','yemen','yemeni'])	#
t.and_query(['trial','abrupt','undoubtedly','under'])	#
t.and_query(['gunfire','had','treatment','handed'])	#
t.and_query(['reaction','reading','reasons'])		#
print("Print the docID?")				# This is just a symbol of going to print the info of DocID
t.print_doc_list()
print("Print the Index?")				# Another symbol of going to print the info of Index just builded
t.print_dict()