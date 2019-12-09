from canvasapi import Canvas
import json
import datetime


class Student(object):
    def __init__(self, student_cred_file='credentials.json'):
        # Parse json
        with open(student_cred_file) as f:
            data = json.load(f)
        # Create canvas obj
        self.canvas = Canvas(data['api_url'], data['auth_token'])

        self.current_user = self.canvas.get_current_user()

    def get_current_classes(self):
        # There are a few other functions that could possible do this, but thus is the only that consistently works
        # Others usually throw errors as you iterate through the list
        return self.current_user.get_favorite_courses()

    def get_graded_assignments(self, course=None):
        """
        returns a list of all graded assignments. Does not return grades
        :param course: If specified, will grade assignments from that course otherwise grabs from all courses
        Must be a course ID
        :return:
        """
        if course is not None:
            courses = [self.canvas.get_course(course)]
        else:
            courses = self.get_current_classes()

        assignments = []
        for c in courses:
            for a in c.get_assignments():
                # If there exists a submission and its graded add assignment
                submission = a.get_submission(self.current_user)
                if submission is not None and submission.workflow_state == 'graded':
                    assignments.append((a.name, a.id, c.course_code, c.id))
        return assignments

    @staticmethod
    def try_parse_dt(datetime_str):
        if datetime_str is not None:
            # I don't know what the Z means, so I ignored it
            dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%SZ')
            return dt
        return None

    def get_upcoming_undated_assignments(self, course=None):
        """
        Returns a list of all upcoming assignments. Used to see which ones we can submit too.
        :param course: If specified, will grade assignments from that course otherwise grabs from all courses
        Must be a course ID
        :return:
        """
        if course is not None:
            courses = [self.canvas.get_course(course)]
        else:
            courses = self.get_current_classes()

        assignments = []
        for c in courses:
            for a in c.get_assignments():
                due_date = self.try_parse_dt(a.due_at)
                if due_date is None or due_date > datetime.datetime.now():
                    assignments.append((a.name, a.id, c.course_code, c.id))
        return assignments

    def make_submission(self, course_id, assignment_id, submission_file, submission_type='online_upload'):
        sub_type = {'submission_type': submission_type}  # There aren't really any other useful submission types
        self.canvas.get_course(course_id).get_assignment(assignment_id).submit(submission=sub_type, file=submission_file)


if __name__ == '__main__':
    me = Student()
    print(me.get_graded_assignments())
