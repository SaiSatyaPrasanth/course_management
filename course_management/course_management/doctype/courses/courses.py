# Copyright (c) 2024, Prasanth and contributors
# For license information, please see license.txt

import frappe,requests
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


@frappe.whitelist()
def generate_course_payment_link(course_id):
    try:
        # Fetch the course record
        course = frappe.get_doc("Courses", course_id)
        
        if not course:
            frappe.throw(f"Course with ID {course_id} not found")

        # Ensure the course has a price
        if not course.price or course.price <= 0:
            frappe.throw(f"Course price must be greater than 0")

        # Razorpay credentials
        key_id = "rzp_test_e664V0FP0zQy7N"
        key_secret = "QdnuRxUHrPGeiJc9lDTXYPO7"
        
        # Razorpay API endpoint
        url = "https://api.razorpay.com/v1/payment_links"
        
        # Payment link data
        data = {
            "amount": int(course.price * 100),  # Convert to paise
            "currency": "INR",
            "description": f"Payment for course: {course.name}",
            "callback_url": frappe.utils.get_url(),  # Replace with your callback URL if needed
            "callback_method": "get",
        }


        data = {
  "amount": 1000,
  "currency": "INR",
  "accept_partial": True,
  "first_min_partial_amount": 100,
  "expire_by": 1735128000,
  "reference_id": "TSsd1725",
  "description": f"Payment for course: {course.name}",
  "customer": {
    "name": "Gaurav Kumar",
    "contact": "+919000090000",
    "email": "gaurav.kumar@example.com"
  },
  "notify": {
    "sms": True,
    "email": True
  },
  "reminder_enable": True,
  "notes": {
    "policy_name": "Jeevan Bima"
  },
  "callback_url": frappe.utils.get_url(),
  "callback_method": "get"
}
        
        # Make the API request to Razorpay
        response = requests.post(url, json=data, auth=(key_id, key_secret))
        response.raise_for_status()
        payment_data = response.json()

        # Update the course record
        course.id = payment_data.get("id")
        course.short_url = payment_data.get("short_url")
        course.status = payment_data.get("status")
        course.save()

        # Return the short URL
        return {"short_url": course.short_url}
    
    except frappe.DoesNotExistError:
        frappe.throw(f"Course with ID {course_id} does not exist")
    except requests.exceptions.RequestException as e:
        frappe.throw(f"Error creating payment link: {str(e)}")
    except Exception as e:
        frappe.throw(f"An unexpected error occurred: {str(e)}")
