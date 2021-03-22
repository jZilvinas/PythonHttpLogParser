#!/usr/bin/env python

def spliting_method(lines):
    splited_list = []

    ip, ident, frank, rest = lines.split(" ", 3)
    date, rest = rest.split(' "', 1)
    protocol, rest = rest.split('" ', 1)
    status, rest = rest.split(" ", 1)
    size, rest = rest.split(' ', 1)
    ip1, ip2, ip3, ip4 = ip.split('.', 3)
        
    splited_list.append(ip1)
    splited_list.append(ip2)
    splited_list.append(ip3)
    splited_list.append(ip4)
    splited_list.append(ident)
    splited_list.append(frank)
    splited_list.append(date)
    splited_list.append(protocol)
    splited_list.append(status)
    splited_list.append(size)
    splited_list.append(rest)

    return splited_list

def joining_method(unsorted_list):
    d = '.'
    s = ' '
    if display == 'terminal':
        for line in unsorted_list:
            print(d.join(line[0:4])+' '+s.join(line[4:]))
            print("\n")
    elif display == 'txt':
        with open("results.txt", 'w') as output:
            for line in unsorted_list:
                output.write(d.join(line[0:4])+' '+s.join(line[4:]))

def collect(unsorted_list):
    if groupBy == 'http':
        plain_list = []
        for line in unsorted_list:
            temp_list = []
            plain_list.append(line[8])
            count_list.append(line[8])
            temp_list.append(line[8])
            temp_list.append(line[9])
            bytes_list.append(temp_list)
    elif groupBy == 'ip':
        d = '.'
        plain_list = []
        for line in unsorted_list:
            temp_list = []
            plain_list.append(d.join(line[0:4]))
            count_list.append(d.join(line[0:4]))
            temp_list.append(d.join(line[0:4]))
            temp_list.append(line[9])
            bytes_list.append(temp_list)    
    plain_list=set(plain_list)
    return plain_list

def split_print(line):
    split_list = []
    first, second = line.split(' ', 1)
    split_list.append(first)
    split_list.append(second)
    return split_list


import sys
import glob
import os

logs_in_directory = []
for file in glob.glob("*.log"):
    logs_in_directory.append(file)

print("Please select log file to use...")
print("\n")
print(logs_in_directory)

filename = input("Enter chosen log file name: ")

if filename not in logs_in_directory:
    for i in range(2):
        print("Selected file does not exist. Choose another one: ")
        filename = input("Enter file name: ")
        if filename in logs_in_directory:
            break
        else:
            exit("You have not chosen existing file to proceed for 2 times. Program is exiting..")

if os.stat(filename).st_size == 0:
    for i in range(2):
        print("Your selected file is empty. Choose another one: ")
        filename = input("Enter file name: ")
        if os.stat(filename).st_size != 0:
            break
        else:
            exit("You have not chosen file to proceed which is not empty for 2 times. Program is exiting..")
   
groupBy = input("Group logs by IP adresses or HTTP statuses? Type 'ip' or 'http': ")

if groupBy == 'ip' or groupBy == 'http':
    pass
else:
    for i in range(2):
        groupBy = input("Select was wrong. Try again 'ip' or 'http': ")
        if groupBy == 'ip' or groupBy == 'http':
            break
        else:
            exit("You have not chosen right grouping choise for 2 times. Program is exiting..")

yesno = input("Do you want to calculate request statistics by specific value? Type 'yes' / 'no': ")

if yesno == 'yes' or yesno == 'Yes':
    var = input("Input IP address or HTTP status code to calculate with: ")
else:
    var = None
print("\n")
param = input("Enter parameter for group calculation. 1 - group requests count, 2 - reques count percentage of all logged requests, 3 - total number of bytes transferred: ")

if param == '1' or param == '2' or param == '3':
    pass
else:
    for i in range(2):
        param = input("Select was wrong. Try again '1', '2' or '3': ")
        if param == '1' or param == '2' or param == '3':
            break
        else:
            exit("You have not chosen right apropriate choise for 2 times. Program is exiting..")

display = input("Display REGROUPED LOGS to terminal or text file? Type 'terminal' or 'txt': ")
limit = int(input("If you want to limit number of rows to print, enter limiter number, otherwise enter '0': "))

unsorted_list = []
count_list = []
bytes_list = []
unique_list = []

with open(filename, 'r') as logfile:
    for line in logfile:
        unsorted_list.append(spliting_method(line))

if groupBy == 'IP' or groupBy == 'ip':
    option = 0
    option2 = 1
    print("\n")
    print("Log file is going to be grouped by IP addresses..")
    print("\n")
    unsorted_list.sort(key=lambda x: (int(x[option]), int(x[option2])))

if groupBy == 'HTTP' or groupBy == 'http':
    option = 8
    print("\n")
    print("Log file is going to be grouped by HTTP status code..")
    print("\n")
    unsorted_list.sort(key=lambda x: int(x[option]))

joining_method(unsorted_list)

unique_list = list(collect(unsorted_list))
request_count_list = []
count_percentage_list = []
print_list = []
sorted_list = []
total_requests = len(count_list)
itter = 0

for line in unique_list:
    request_count_list.append(count_list.count(line))
    if param == '1':
        print_list.append(line+'  '+str(count_list.count(line)))
    if param == '2':
        print_list.append(line+'  '+str(round(float(request_count_list[itter])/total_requests * 100,2)))
        itter+=1
    if param == '3':
        bytes_sum = 0
        for j in range(len(bytes_list)):
            if bytes_list[j][0] == line and bytes_list[j][1] != '-':
                bytes_sum = bytes_sum + int(bytes_list[j][1])
        print_list.append(line+'  '+str(bytes_sum))

for lines in print_list:
    sorted_list.append(split_print(lines))

if param == '2':
    sorted_list.sort(key=lambda x: float(x[1]), reverse=True)
else:
    sorted_list.sort(key=lambda x: int(x[1]), reverse=True)

print("Groups   |   Calculations")
if limit == 0 or limit > len(sorted_list):
    limit = len(sorted_list)
if limit != 0:
    limit = limit
for i in sorted_list[:limit]:
    print(i[0]+'        '+i[1])

print("\n")
if var != None:
    bytes_sum = 0
    total_requests = len(count_list)
    request_count = count_list.count(var)
    count_percentage = round(request_count / total_requests * 100, 1)

    for i in range(len(bytes_list)):
        if bytes_list[i][0] == var and bytes_list[i][1] != '-':
            bytes_sum = bytes_sum + int(bytes_list[i][1])

    print("There are {} requests in the log file based on your calculation choice: {}.".format(request_count, var))
    print("Counted logs consists {}% of all logged requests.".format(count_percentage))
    if bytes_sum == 0:
        print("System has not found neccesary data to calculate total number of transfered bytes.")
    else:
        print("There was {} bytes transfered based on selected logs.".format(bytes_sum))

print("\n")
print("Total logs readed and parsed: {}".format(total_requests))
print("\n")
print("Program finished job. Exiting....")

