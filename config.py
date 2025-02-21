# Predefined teacher roles and their requirements
TEACHER_ROLES = {
    "Principal Software Engineer": {
        "requirements": {
            "subject": ["Software Engineering"],
            "min_experience": 8,
            "responsibilities": [
                "Lead system architecture design",
                "Mentor senior engineers",
                "Drive technical decisions and innovation"
            ]
        }
    },
    "Senior Software Engineer": {
        "requirements": {
            "subject": ["Software Engineering"],
            "min_experience": 5,
            "responsibilities": [
                "Design and implement complex features",
                "Code review and technical mentorship",
                "Lead project implementations"
            ]
        }
    },
    "Software Engineer": {
        "requirements": {
            "subject": ["Software Engineering"],
            "min_experience": 0,
            "responsibilities": [
                "Develop and maintain software features",
                "Write clean, testable code",
                "Participate in code reviews"
            ]
        }
    }
}

# Predefined resources for each role
ROLE_RESOURCES = {
    "Principal Software Engineer": [
        {
            "type": "Software",
            "items": [
                "Enterprise Architecture Tools",
                "Cloud Platform Admin Access",
                "Advanced Development Tools"
            ]
        },
        {
            "type": "Materials",
            "items": [
                "System Design Documentation",
                "Architecture Decision Records",
                "Technical Leadership Guidelines"
            ]
        },
        {
            "type": "Access",
            "items": [
                "All Production Systems",
                "Technical Strategy Platform",
                "Enterprise Resource Planning"
            ]
        }
    ],
    "Senior Software Engineer": [
        {
            "type": "Software",
            "items": [
                "Full Development Suite",
                "CI/CD Pipeline Access",
                "Testing Frameworks"
            ]
        },
        {
            "type": "Materials",
            "items": [
                "Technical Documentation",
                "Design Patterns Guide",
                "Code Review Guidelines"
            ]
        },
        {
            "type": "Access",
            "items": [
                "Development Environment",
                "Code Repository",
                "Project Management Tools"
            ]
        }
    ],
    "Software Engineer": [
        {
            "type": "Software",
            "items": [
                "IDE and Dev Tools",
                "Version Control System",
                "Bug Tracking System"
            ]
        },
        {
            "type": "Materials",
            "items": [
                "Coding Standards Guide",
                "Development Tutorials",
                "API Documentation"
            ]
        },
        {
            "type": "Access",
            "items": [
                "Development Portal",
                "Learning Resources",
                "Team Collaboration Tools"
            ]
        }
    ]
}

# Company Information
SCHOOL_INFO = {
    "name": "TechFlow Solutions",
    "principal": {
        "name": "Boluwatife Lambe",
        "position": "CTO",
        "email": "cto@techflow.com",
        "office": "Executive Floor, Tech Hub",
        "phone": "ext. 1001"
    }
}

# Management structure and contact information
MANAGEMENT_STRUCTURE = {
    "Principal Software Engineer": {
        "school": SCHOOL_INFO,
        "direct_supervisor": {
            "name": "Dr. Sarah Johnson",
            "role": "VP of Engineering",
            "email": "sarah.johnson@techflow.com",
            "office": "Floor 4, Tech Hub",
            "office_hours": "Monday-Friday, 9:00 AM - 4:00 PM"
        },
        "department_admin": {
            "name": "Michael Chen",
            "email": "m.chen@techflow.com",
            "office": "Floor 4, Tech Hub",
            "phone": "ext. 4001"
        },
        "team_meetings": "Every Monday at 2:00 PM in Conference Room A"
    },
    "Senior Software Engineer": {
        "school": SCHOOL_INFO,
        "direct_supervisor": {
            "name": "Prof. Robert Martinez",
            "role": "Engineering Manager",
            "email": "r.martinez@techflow.com",
            "office": "Floor 3, Tech Hub",
            "office_hours": "Monday-Friday, 10:00 AM - 3:00 PM"
        },
        "department_admin": {
            "name": "Michael Chen",
            "email": "m.chen@techflow.com",
            "office": "Floor 4, Tech Hub",
            "phone": "ext. 4001"
        },
        "team_meetings": "Every Wednesday at 3:00 PM in Conference Room B"
    },
    "Software Engineer": {
        "school": SCHOOL_INFO,
        "direct_supervisor": {
            "name": "Emily Wong",
            "role": "Team Lead",
            "email": "e.wong@techflow.com",
            "office": "Floor 2, Tech Hub",
            "office_hours": "Monday-Friday, 9:30 AM - 4:30 PM"
        },
        "department_admin": {
            "name": "Michael Chen",
            "email": "m.chen@techflow.com",
            "office": "Floor 4, Tech Hub",
            "phone": "ext. 4001"
        },
        "team_meetings": "Every Tuesday at 1:00 PM in Conference Room C",
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
    if subject.lower() != "software engineering":
        return None
    
    if experience >= 8:
        return "Principal Software Engineer"
    elif experience >= 5:
        return "Senior Software Engineer"
    else:
        return "Software Engineer"

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
