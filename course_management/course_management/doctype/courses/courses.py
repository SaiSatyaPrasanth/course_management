# Copyright (c) 2024, Prasanth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Courses(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_all_subject_and_chapters(course_id):
    # Fetch the course document with the given course_id
    course = frappe.get_doc("Courses", course_id)
    
    if not course:
        frappe.throw(f"No course found with ID {course_id}")
    
    # Prepare a list to store subjects and their chapters
    all_subjects_and_chapters = []

    # Iterate over the subjects child table in the course
    for subject_row in course.subjects:  # Assuming 'subjects' is the child table fieldname
        # Fetch the subject document to get its chapters
        subject = frappe.get_doc("Subject", subject_row.subject_id)

        # Prepare a dictionary to hold subject data
        subject_data = {
            "subject_id": subject_row.subject_id,
            "subject_name": subject_row.subject_name,
            "chapters": []
        }

        # Iterate over the chapters child table in the subject
        for chapter_row in subject.chapters:  # Assuming 'chapters' is the child table fieldname
            chapter_data = {
                "name": chapter_row.name1,
                "chapter_type": chapter_row.chapter,
                "youtube_id": chapter_row.youtube_id,
                "vimeo_id": chapter_row.vimeo_id
            }
            subject_data["chapters"].append(chapter_data)

        # Add the subject data to the list
        all_subjects_and_chapters.append(subject_data)

    return all_subjects_and_chapters


