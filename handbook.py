"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: We do not expect you to come up with a perfect solution. We are more interested
in how you would approach a problem like this.
"""
import json
import re 

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()

def is_unlocked(courses_list, target_course):
    units_done = len(courses_list) * 6
    requirements = CONDITIONS[target_course].lower()
    copy = requirements.split()
    if len(requirements) == 0:
        return True
    elif len(courses_list) == 0:
        return False

    if len(requirements) == 4:
        requirements = 'COMP' + requirements
        if requirements in courses_list:
            return True
        else:
            return False

    for i in range(len(copy)):
        if valid_course(copy[i]):
            word = copy[i].strip(' ()')
            word = word.strip()
            if word.upper() in courses_list:
                requirements = requirements.replace(word, 'True')
            else:
                requirements = requirements.replace(word, 'False')
        if copy[i].isnumeric():
            if check_unit(copy, i):
                if check_in(copy, i):
                    if check_level(copy, i):
                        print('hello')
                        level = copy[i+6]
                        units = enough_levels(courses_list, level, copy[i])
                        if units == True:
                            requirements = requirements.replace(copy[i], 'True')
                        else:
                            requirements = requirements.replace(copy[i], 'False')
                    else:
                        course = get_course(copy, i)
                        enough_units = get_units(copy[i], course, courses_list)
                        delete_section = get_string(copy, i)
                        delete_section = ' '.join(delete_section)
                        if enough_units == True:
                            requirements = requirements.replace(delete_section, 'True')
                        else:
                            requirements = requirements.replace(delete_section, 'False')
                else:
                    word = copy[i] + ' units of credit'
                    if units_done < int(copy[i]):
                        requirements = requirements.replace(word, 'False')
                    else:
                        requirements = requirements.replace(word, 'True')
    
    req = requirements.split()
    
    for i in range(len(req)):
        word = req[i]
        if check_true(word) == False and check_false(word) == False and word != 'and' and word != 'or':
            requirements = requirements.replace(word, '')
   
    return eval(requirements)


def valid_course(word):
    list = re.findall(r"[a-z]{4}\d{4}", word)
    if (len(list) == 1):
        return True
    else: 
        return False

def check_unit(copy, i):
    if copy[i+1] == 'units':
        return True
    else:
        return False

def check_in(copy, i):
    if len(copy) < i + 5:
        return False
    elif copy[i+1] == 'units' and (copy[i+2] == 'of' or copy[i+2] == 'oc') and copy[i+3] == 'credit' and copy[i+4] == 'in':
        return True
    else:
        return False

def check_true(word):
    list = re.findall("True", word)
    if (len(list) == 1):
        return True
    else:
        return False

def check_false(word):
    list = re.findall("False", word)
    if (len(list) == 1):
        return True
    else:
        return False

def get_course(copy, i):
    courses = []
    j = i + 5
    while copy[j][-1] != ')':
        word = copy[j].strip(' ()')
        courses.append(word)
        j += 1
    courses.append(copy[j].strip(' ()'))
    return courses

def get_units(val, course, courses_list):
    units = 0
    for unit in course:
        unit = unit.strip(' ,')
        if unit.upper() in courses_list:
            units += 6
    if units >= int(val):
        return True
    else:
        return False

def get_string(copy, i):
    replace_string = []
    while copy[i][-1] != ')':
        replace_string.append(copy[i])
        i += 1
    replace_string.append(copy[i])
    return replace_string

def check_level(copy, i):
    if copy[i+5] == 'level':
        return True
    else:
        return False

def enough_levels(courses_list, level, val):
    units = 0
    for course in courses_list:
        if course[4] == level:
            units += 6
    if units >= int(val):
        return True
    else:
        return False
