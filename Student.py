from canvasapi import Canvas
import json
import datetime


class Student(object):
    API_URL = "https://canvas.colorado.edu/"

    def __init__(self, student_cred_file='credentials.json'):
        # Parse json
        with open(student_cred_file) as f:
            data = json.load(f)
        # Create canvas obj
        self.canvas = Canvas(self.API_URL, data['auth_token'])

        self.current_user = self.canvas.get_current_user()

    def get_current_classes(self):
        return self.current_user.get_favorite_courses()

    def get_graded_assignments(self, course=None):
        assignments = []
        if course is None:
            for c in self.get_current_classes():
                all_assignments = c.get_assignments()
                for a in all_assignments:
                    submission = a.get_submission(self.current_user)
                    if submission.workflow_state == 'graded':
                        assignments.append((a.name, a.id, c.name, c.id))
        else:
            specified_course = self.canvas.get_course(course)
            all_assignments = specified_course.get_assignments()
            for a in all_assignments:
                submission = a.get_submission(self.current_user)
                if submission.workflow_state == 'graded':
                    assignments.append((a.name, a.id, specified_course.name, specified_course.id))
        return assignments

    @staticmethod
    def try_parse_dt(datetime_str):
        if datetime_str is not None:
            # I don't know what the Z means
            dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
            return dt
        return None

    def get_upcoming_undated_assignments(self, course=None):
        assignments = []
        if course is None:
            for c in self.get_current_classes():
                all_assignments = c.get_assignments()
                for a in all_assignments:
                    due_date = self.try_parse_dt(a.due_at)
                    if due_date is None or due_date > datetime.datetime.now():
                        assignments.append((a.name, a.id, c.course_code, c.id))
        else:
            specified_course = self.canvas.get_course(course)
            all_assignments = specified_course.get_assignments()
            for a in all_assignments:
                due_date = self.try_parse_dt(a.due_at)
                if due_date is None or due_date > datetime.datetime.now():
                    assignments.append((a.name, a.id, specified_course.course_code, specified_course.id))
        return assignments

    def make_submission(self, course_id, assignment_id, submission_file):
        sub_type = {'submission_type': 'online_upload'}
        self.canvas.get_course(course_id).get_assignment(assignment_id).submit(submission=sub_type, file=submission_file)


if __name__ == '__main__':
    me = Student()
    print(me.get_upcoming_undated_assignments())
    print(me.get_graded_assignments())
