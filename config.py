# Predefined teacher roles and their requirements
TEACHER_ROLES = {
    "Senior Mathematics Teacher": {
        "requirements": {
            "subject": ["Mathematics"],
            "min_experience": 5,
            "responsibilities": [
                "Lead curriculum development",
                "Mentor junior teachers",
                "Conduct advanced mathematics classes"
            ]
        }
    },
    "Mathematics Teacher": {
        "requirements": {
            "subject": ["Mathematics"],
            "min_experience": 2,
            "responsibilities": [
                "Teach regular mathematics classes",
                "Participate in curriculum planning",
                "Provide student support"
            ]
        }
    },
    "Junior Mathematics Teacher": {
        "requirements": {
            "subject": ["Mathematics"],
            "min_experience": 0,
            "responsibilities": [
                "Assist in mathematics classes",
                "Provide tutoring support",
                "Learn from senior teachers"
            ]
        }
    }
}

# Predefined resources for each role
ROLE_RESOURCES = {
    "Senior Mathematics Teacher": [
        {
            "type": "Software",
            "items": [
                "Advanced Mathematical Modeling Software",
                "Online Assessment Platform",
                "Curriculum Planning Tools"
            ]
        },
        {
            "type": "Materials",
            "items": [
                "Senior Mathematics Curriculum Guide",
                "Advanced Problem Sets",
                "Teacher Mentoring Guidelines"
            ]
        },
        {
            "type": "Access",
            "items": [
                "Department Head Portal",
                "Curriculum Development Platform",
                "Teacher Training Resources"
            ]
        }
    ],
    "Mathematics Teacher": [
        {
            "type": "Software",
            "items": [
                "Basic Mathematical Software",
                "Student Progress Tracking Tool",
                "Interactive Learning Platform"
            ]
        },
        {
            "type": "Materials",
            "items": [
                "Mathematics Curriculum Guide",
                "Standard Problem Sets",
                "Teaching Resources"
            ]
        },
        {
            "type": "Access",
            "items": [
                "Teacher Portal",
                "Learning Management System",
                "Digital Library"
            ]
        }
    ],
    "Junior Mathematics Teacher": [
        {
            "type": "Software",
            "items": [
                "Basic Mathematical Software",
                "Student Management System",
                "Learning Resources Platform"
            ]
        },
        {
            "type": "Materials",
            "items": [
                "Basic Mathematics Teaching Guide",
                "Beginner Problem Sets",
                "Teaching Assistant Resources"
            ]
        },
        {
            "type": "Access",
            "items": [
                "Teaching Assistant Portal",
                "Learning Resources Library",
                "Training Materials"
            ]
        }
    ]
}

# School Information
SCHOOL_INFO = {
    "name": "Glorylink Schools",
    "principal": {
        "name": "Boluwatife Lambe",
        "position": "Principal",
        "email": "principal@glorylinkschools.edu",
        "office": "Principal's Office, Main Building",
        "phone": "ext. 1001"
    }
}

# Management structure and contact information
MANAGEMENT_STRUCTURE = {
    "Senior Mathematics Teacher": {
        "school": SCHOOL_INFO,
        "direct_supervisor": {
            "name": "Dr. Sarah Johnson",
            "role": "Head of Mathematics Department",
            "email": "sarah.johnson@glorylinkschools.edu",
            "office": "Room 401, Academic Building",
            "office_hours": "Monday-Friday, 9:00 AM - 4:00 PM"
        },
        "department_admin": {
            "name": "Michael Chen",
            "email": "m.chen@glorylinkschools.edu",
            "office": "Room 400, Academic Building",
            "phone": "ext. 4001"
        },
        "team_meetings": "Every Monday at 2:00 PM in Room 405"
    },
    "Mathematics Teacher": {
        "school": SCHOOL_INFO,
        "direct_supervisor": {
            "name": "Prof. Robert Martinez",
            "role": "Senior Mathematics Coordinator",
            "email": "r.martinez@glorylinkschools.edu",
            "office": "Room 302, Academic Building",
            "office_hours": "Monday-Friday, 10:00 AM - 3:00 PM"
        },
        "department_admin": {
            "name": "Michael Chen",
            "email": "m.chen@glorylinkschools.edu",
            "office": "Room 400, Academic Building",
            "phone": "ext. 4001"
        },
        "team_meetings": "Every Wednesday at 3:00 PM in Room 303"
    },
    "Junior Mathematics Teacher": {
        "school": SCHOOL_INFO,
        "direct_supervisor": {
            "name": "Prof. Emily Wong",
            "role": "Junior Faculty Coordinator",
            "email": "e.wong@glorylinkschools.edu",
            "office": "Room 201, Academic Building",
            "office_hours": "Monday-Friday, 9:30 AM - 4:30 PM"
        },
        "department_admin": {
            "name": "Michael Chen",
            "email": "m.chen@glorylinkschools.edu",
            "office": "Room 400, Academic Building",
            "phone": "ext. 4001"
        },
        "team_meetings": "Every Tuesday at 1:00 PM in Room 205",
        "mentor_program": {
            "mentor": "Will be assigned during first team meeting",
            "mentoring_sessions": "Weekly, schedule to be determined with assigned mentor"
        }
    }
}

def get_suitable_role(subject, experience):
    """
    Determine the most suitable role based on subject and experience.
    """
    if subject.lower() != "mathematics":
        return None
    
    if experience >= 5:
        return "Senior Mathematics Teacher"
    elif experience >= 2:
        return "Mathematics Teacher"
    else:
        return "Junior Mathematics Teacher"

def get_role_resources(role):
    """
    Get the resources associated with a specific role.
    """
    return ROLE_RESOURCES.get(role, [])

def get_management_info(role):
    """
    Get the management information for a specific role.
    """
    return MANAGEMENT_STRUCTURE.get(role, {})
