import csv

with open('students.csv', 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    names = {row['id']: (row['name']) for row in reader }

with open('courses.csv', 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    courses = {row['id']: (row['name'], row['teacher']) for row in reader }

with open('tests.csv', 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    tests = {row['id']: (row['course_id'], row['weight']) for row in reader }

with open('marks.csv', 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    marks = {(row['test_id'], row['student_id'], row['mark']) for row in reader}

PERCENTAGE = 0.01
lines = []
         
def getStudentsRecords():
    student_records = {}

    for test in marks:

        test_id = test[0]
        student_id = test[1]
        mark_percentage = test[2]

        course = getCourseAndWeight(test_id)[0]
        weight = getCourseAndWeight(test_id)[1]
        mark_tally = float(weight) * PERCENTAGE * float(mark_percentage)

        if student_records.get(student_id) == None:
            student_records[student_id] = {course: mark_tally}
        else:
            if student_records.get(student_id).get(course) == None:
                student_records[student_id].update({course: mark_tally})
            else:
                current_mark_tally = student_records.get(student_id).get(course)
                new_mark_tally = current_mark_tally + mark_tally
                student_records[student_id].update({course: new_mark_tally})

    return student_records

def getCourseAndWeight(test_id):
    return (tests.get(test_id)[0], tests.get(test_id)[1])

def getAverage(course_ids, student_record_list):
    grade = 0
    counter = 0
    for cid in course_ids:
        grade += student_record_list[cid]
        counter += 1
    average = grade / counter
   
    return "%.2f" % average


records = getStudentsRecords()
student_id_list = records.keys()
student_id_list.sort(key = int)

for sid in student_id_list :

    line_string = "Student Id: %s, name: %s  " % (sid, names[sid])
    lines.append(line_string)
    if records[sid] != None:
        student_record = records[sid]
        course_id_list = records[sid].keys()
        course_id_list.sort(key = int)

        average = getAverage(course_id_list, student_record)
        line_string = "Total Average:       %s \n" % (average)
        lines.append(line_string)

        for cid in course_id_list:
            
            grade = "%.2f" % student_record[cid]
            course_name = courses[cid][0]
            course_teacher = courses[cid][1]
            line_string1 = "    Course: %s, Teacher: %s" % (course_name, course_teacher)
            line_string2 = "    Final Grade:   %s \n " % (grade) 
            lines.append(line_string1)
            lines.append(line_string2)
               
    else:
        line_string = "Total Average:       0% \n"
        lines.append(line_string)

with open('output.txt', 'w') as f:
    f.writelines("%s\n" % l for l in lines)

f.close()