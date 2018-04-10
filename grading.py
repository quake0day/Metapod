import zipfile
import subprocess
import csv
from optparse import OptionParser

FILENAME = "./Homework3 Download Apr 10, 2018 956 AM.zip"
CSV_FILE_NAME = "./2018 Spring-CSC141-03 Computer Sci I_GradesExport_2018-04-10-09-41.csv"
GRADE_ITEM = "Homework3 Points Grade <Numeric MaxPoints:6 Category:Homework>"
TMP_FILE = "./pos.tmp"
GRADING_POLICY = '0'
#MAXPOINTS = str(6)
# save last status .. just in case
def saveLastPosition(tmp_file, num):
    f = open(tmp_file, 'w')
    f.write(str(num))
    f.close()

# read last status
def readLastPosition(tmp_file):
    f = open(tmp_file, 'r')
    num = f.read()
    return int(num)

def readZipFile(filename):
    archive = zipfile.ZipFile(filename, 'r')
    source_file_list = archive.namelist()
    num = 0
    try:
        num = readLastPosition(TMP_FILE)
    except:
        pass
    for i in xrange(num, len(source_file_list)):
        sf = source_file_list[i]
        if sf != 'index.html': # ignore the annoying html file
            try:
                # split the filename
                # sample filename
                # 522062-838799 - Emily McDevitt - Sep 10, 2016 552 PM - Homework_one_EM.java
                #print sf.split(' - ')
                unused, name, date, filename = sf.split(' - ')
                filename = filename.strip()
                name = name.strip()
                name = name.split(' ')
            except Exception, e:
                print e
                pass

            if getfileType(filename):
                isFilled = checkGrade(CSV_FILE_NAME, GRADE_ITEM, name)
                if (isFilled and GRADING_POLICY == '1') or (GRADING_POLICY == '0'):
                    source_code =  readfile(sf, archive)
                    print '--------------SOURCE CODE BEGIN--------'
                    print source_code
                    print '--------------SOURCE CODE END--------'
                    print '--------------RUNNING RESULT BEGIN--------'
                    output = None
                    try:
                        output = runJava(filename, source_code)
                        print output
                    except Exception, e:
                        print e
                        pass
                    print '--------------RUNNING RESULT END--------'

                    grade = raw_input('Grade it (?/6) + Bonues 1: ')
                    enterGrade(CSV_FILE_NAME, GRADE_ITEM, name, grade)
                    saveLastPosition(TMP_FILE,i)
        #source_file = archive.read('')

def getfileType(filename):
    if filename.split(".")[1] != 'java':
        return False
    return True

def readfile(full_filename, archive):
    source_code = archive.read(full_filename)
    return source_code

def runJava(filename, source_code):
    class_file_name = filename.split(".")[0]
    # save the source code
    f = open(filename,'w')
    f.write(source_code)
    f.close()

    # run program
    subprocess.call(['javac', '-g', filename])
    output = subprocess.check_output(['java', class_file_name])
    return output

def getName(name):
    firstname, lastname = "", ""
    if len(name) == 2:
        firstname, lastname = name[0], name[1]
    else:
        lastname = name[-1]
        firstname = " ".join(fn for fn in name[:-1])  
    return firstname, lastname

def checkGrade(csv_file_name, grade_item, name):
    # if len(name) == 2:
    #     firstname, lastname = name[0], name[1]
    # else:
    #     lastname = name[-1]
    #     firstname = " ".join(fn for fn in name[:-1])  
    firstname, lastname = getName(name)
    print "Student Name: " + firstname +" "+ lastname

    r = csv.reader(open(csv_file_name))
    lines = [l for l in r]
    col_num = lines[0].index(grade_item)
    last_name_col_num = lines[0].index('Last Name')
    first_name_col_num = lines[0].index('First Name')
    for row in lines:
        print row[last_name_col_num], lastname
        print row[first_name_col_num], firstname
        if row[last_name_col_num] == lastname and row[first_name_col_num] == firstname:
            if row[col_num] == '':
                print "TRUE"
                return True
            else:
                print "FALSE"
                return False
    return False


def enterGrade(csv_file_name, grade_item, name, grade):
    firstname, lastname = getName(name)
    r = csv.reader(open(csv_file_name))
    lines = [l for l in r]
    col_num = lines[0].index(grade_item)
    last_name_col_num = lines[0].index('Last Name')
    first_name_col_num = lines[0].index('First Name')
    for row in lines:
        if row[last_name_col_num] == lastname and row[first_name_col_num] == firstname:
            print "Find it!"
            # update the grade
            row[col_num] = grade
            print "Done"
    writer = csv.writer(open(csv_file_name, 'w'))
    writer.writerows(lines)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-g", help="grading policy. 0 for regrade all students, 1 for grade new students", dest="num", default=0)
    options, args = parser.parse_args()
    GRADING_POLICY = options.num
    #checkGrade(CSV_FILE_NAME, GRADE_ITEM, ['ELIZABETH','LEGG'])
    readZipFile(FILENAME)
#enterGrade(CSV_FILE_NAME, GRADE_ITEM, ['LEGG', 'ELIZABETH'] , 6)
