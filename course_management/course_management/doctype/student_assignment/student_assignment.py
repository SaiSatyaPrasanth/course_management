# Copyright (c) 2024, Prasanth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StudentAssignment(Document):
	pass


@frappe.whitelist(allow_guest=True)
def get_all_courses_of_student():
    # Fetch all Student Assignment records
    student_assignments = frappe.get_all("Student Assignment", fields=["name", "student_id", "status", "expiry_date"])

    for student in student_assignments:
        # Fetch the child table rows linked to this student assignment
        courses = frappe.get_all(
            "Assigned Courses",  # Replace "Course" with the actual child Doctype name
            filters={"parent": student["name"]},  # "parent" links to the parent document's name
            fields=["course_name", "course_id", "price", "status"]
        )
        
		
        
        # Add the child table data to the student object
        student["courses"] = courses

        # Print the updated student record
        print(student)

    # Return the complete list with child table data included
    return student_assignments


