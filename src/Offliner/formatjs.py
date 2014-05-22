'''
Created on Oct 20, 2012

@author: joseph
'''
#!coding=utf-8
lines = open("unformated.js").readlines()[0].split(";")
indent = 0
formatted = []
for line in lines:
    newline = []
    for char in line:
        newline.append(char)
        if char=='{': 
            indent+=1
            newline.append("\n")
            newline.append("\t"*indent)
        if char=="}":
            indent-=1
            newline.append("\n")
            newline.append("\t"*indent)
    formatted.append("\t"*indent+"".join(newline))
print formatted
#open("formated.js","w").writelines(";\n".join(formatted))