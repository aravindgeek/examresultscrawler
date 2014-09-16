#!/usr/bin/python2

comm = raw_input("Enter the common part of Register No: ")
start = int(raw_input("Enter the starting number: "))
end = int(raw_input("Enter the last number: "))
file_name = raw_input("Enter the file_name: ")
mode = raw_input("Enter 0 to create file or 1 to append to file: ")
if mode  == '0':
    mode = 'w'
elif mode == '1':
    mode = 'wa'
else:
    print('Please give 0 or 1 to FileWrite mode')
try:
    fout = open(file_name,mode)
    for i in range(start,end+1):
        fout.write('%s%02d\n'% (comm,i))
    fout.close()
except:
    print ('Some Error has occured in writing to file')
