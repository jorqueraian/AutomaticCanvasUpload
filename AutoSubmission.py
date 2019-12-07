# Import the Canvas class
from Student import Student
from StringSimilarity import cost_of_alignment
import os
import sys

USER_PATH = 'C:\\Users\\jorqu\\'


def clean_str(input_str):
    # Remove .pdf or what ever
    # Make lowercase and remove whitespace
    # remove _ or -
    return str(input_str).split('.')[0].lower().strip().replace('_', '').replace('-', '')


def try_verify_path(local_path):
    if os.path.exists(local_path):
        return True

    split_path = local_path.split('\\')

    if split_path[0] == '..':
        new_path = os.path.abspath(local_path)  # For some reason this isn't working, it returns false
    elif split_path[0] == 'Documents' or split_path[0] == 'Downloads' or split_path[0] == 'Desktop':
        new_path = USER_PATH + local_path
    else:
        return False

    local_path = new_path

    if os.path.exists(str(local_path)):
        return True
    else:
        return False


def find_assignment(student, file_path: str):
    file_name = file_path.split('\\')[-1]
    cleaned_file_name = clean_str(file_name)

    assignments = student.get_upcoming_undated_assignments()

    best_match = None
    for a in assignments:
        combine_str = clean_str(a[2]+a[0])
        cost = cost_of_alignment(combine_str, cleaned_file_name, 1, 2, 3)
        cost_per_char = cost / (len(combine_str)+len(cleaned_file_name))
        if best_match is None or cost_per_char < best_match[1]:
            best_match = (a, cost_per_char)
    return best_match


def auto_upload(student, file_path):
    assignment = find_assignment(student, file_path)
    course_id = assignment[0][3]
    assignment_id = assignment[0][1]

    print(f'Submitting Assignment: {assignment[0][0]}\n'
          f'Course: {assignment[0][2]}\n'
          f'File: {file_path}\n'
          f'Cost per character: {assignment[1]}')

    confirmation = input('Please confirm(Y/n)').lower()
    if confirmation == 'y':
        print('Submitting assignment....')
        student.make_submission(course_id, assignment_id, file_path)
    else:
        print('No Submission made')


if __name__ == '__main__':
    # For reference: Documents\CSCI_3104_Final_Exam.zip
    # Initialize student API
    me = Student()

    # Verify that a path was provided
    if len(sys.argv) < 2:
        print('No file selected')
    else:
        path = sys.argv[1]
        # Verify correctness of path
        if try_verify_path(path):
            # Upload to canvas
            auto_upload(me, path)
        else:
            print(f'File not found: {path}')

