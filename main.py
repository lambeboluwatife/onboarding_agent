import sys
import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from task_output import TaskOutput
from config import get_suitable_role, get_role_resources, get_management_info, TEACHER_ROLES

import os
import emails
from utils import get_openai_ap_key
from dotenv import load_dotenv

load_dotenv()

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Set OpenAI configuration
os.environ["OPENAI_API_KEY"] = api_key

# Configure CrewAI to use OpenAI
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)


from crewai.tools import tool
class MailSenderTool:
    def __init__(self):
        # Get email credentials from environment variables
        email_user = os.getenv("EMAIL_USER")
        email_password = os.getenv("EMAIL_PASSWORD")
        
        if not email_user or not email_password:
            raise ValueError("Email credentials not found in environment variables")
            
        self.smtp_settings = {
            "host": "smtp.gmail.com",
            "port": 587,
            "tls": True,
            "user": email_user,
            "password": email_password,
        }

    def send_email(self, recipient, subject, body):
        message = emails.Message(
            subject=subject,
            text=body,
            mail_from=("Boluwatife Lambe", self.smtp_settings["user"]),
        )
        
        response = message.send(to=recipient, smtp=self.smtp_settings)
        
        if response.status_code == 250:
            return f"✅ Email sent to {recipient}"
        else:
            return f"❌ Failed to send email. Status: {response.status_code}"

# Tools
@tool("Email Sender")
def send_emails(onboarding_data: str) -> str:
    """Send onboarding email to the newly appointed teacher.
    
    Args:
        onboarding_data (str): JSON string containing teacher's email and the email body
    
    Returns:
        str: Status message indicating whether the email was sent successfully
    """
    try:
        # Parse the onboarding data
        import json
        data = json.loads(onboarding_data)
        
        # Send the email using the exact body from the finalization agent
        mail_sender = MailSenderTool()
        result = mail_sender.send_email(
            recipient=data['email'],
            subject=f"Welcome to Glorylink Schools - Your Onboarding Information",
            body=data['email_body']
        )
        
        return result
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"

# Define Agents
recruitment_agent = Agent(
    name="Recruitment Agent",
    role="Recruitment Agent",
    goal="Handles teacher onboarding by collecting and verifying necessary details.",
    backstory="You are a recruitment agent that collects and verifies information of newly appointed teachers. You ensure all required details are accurate and complete.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

role_assignment_agent = Agent(
    name="Role Assignment Agent",
    role="Role Assignment Agent",
    goal="Determines the best role for a teacher based on predefined role requirements and provides complete role details.",
    backstory="""You are a role assignment agent responsible for:
    1. Analyzing teacher qualifications against predefined role requirements
    2. Using the get_suitable_role() function to determine the appropriate role
    3. Using get_management_info() to get management details
    4. Providing a detailed response that includes:
       - Assigned Role Title
       - Justification for the role assignment
       - Management Structure Details:
      * Direct Supervisor's full name, role, email, office location, and office hours
      * Department Admin's name, email, office location, and phone number
      * Team meeting schedule
      * Any role-specific information (such as mentoring program details)

    You ensure all information is accurate and complete before passing it to the next stage.""",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

resources_agent = Agent(
    name="Resources Agent",
    role="Resources Agent",
    goal="Provides the teacher with role-specific resources and materials.",
    backstory="You are a resources agent that ensures teachers receive all necessary resources based on their assigned role. You maintain an organized system for resource distribution.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

finalization_agent = Agent(
    name="Finalization Agent",
    role="Finalization Agent",
    goal="Ensures all onboarding steps are completed and documented.",
    backstory="""You are a finalization agent that confirms all onboarding steps are properly completed and documented. 
    You ensure a smooth transition for new teachers by sending a comprehensive welcome email that includes:
    1. Their assigned role (either senior, junior, or others) and responsibilities
    2. Available resources and how to access them
    3. Management structure details (generate appropriate details for):
       - Direct supervisor's information
       - Department admin's information
       - Team meeting schedule
       - Mentoring program details (if applicable)
    4. Next steps and important dates:
       - First day orientation: Monday, February 24, 2025, 9:00 AM
       - Department meeting: Tuesday, February 25, 2025, 2:00 PM
       - IT system training: Wednesday, February 26, 2025, 10:00 AM
       - First team meeting: According to role's schedule in first week
       - Required documentation submission deadline: Friday, February 28, 2025
    
    5. The mail should be sent to the teacher's email from gather_info_task
    The email should be signed by:
    Boluwatife Lambe
    Principal
    Glorylink Schools
    
    Ensure ALL placeholder text is replaced with actual information from the previous tasks.""",
    llm=llm,
    tools=[send_emails],
    allow_delegation=False,
    verbose=True
)

# Define Tasks
gather_info_task = Task(
    description="""Collect and verify teacher details: {teacher_info}. 
    Extract and structure the following information:
    - Full Name
    - Subject
    - Years of Experience
    - Email
    Return this information in a clear, structured format.""",
    agent=recruitment_agent,
    expected_output="Structured teacher details including name, subject expertise, email and experience"
)

assign_role_task = Task(
    description="""Based on the verified teacher details, determine their role and provide complete role information.

    Process:
    1. Extract teacher's subject and experience from the input
    2. Use get_suitable_role(subject, experience) to determine the appropriate role
    3. Use get_management_info(role) to get management details
    4. Compile a complete response that includes role assignment and management details

    Your response must include:
    - Assigned Role Title
    - Justification for the role assignment
    - Management Structure Details:
      * Direct Supervisor's full name, role, email, office location, and office hours
      * Department Admin's name, email, office location, and phone number
      * Team meeting schedule
      * Any role-specific information (such as mentoring program details)

    Ensure you provide actual data from the management structure for all fields.
    Return a structured response and format your response as a clear, structured output that can be easily used by the next task.""",
    context=[gather_info_task],
    agent=role_assignment_agent,
    expected_output="Complete role assignment details including role, justification, and full management structure",
)

provide_resources_task = Task(
    description="""Using the assigned role, compile a complete list of resources to be provided.
    Use get_role_resources() to get the role-specific resources.
    
    Include specific details about:
    - Software tools and access credentials
    - Teaching materials and textbooks
    - Administrative supplies
    - Professional development resources
    
    Return a structured list of all resources with access/usage instructions.""",
    context=[assign_role_task],
    agent=resources_agent,
    expected_output="Detailed list of role-specific resources with access instructions",
)

finalize_onboarding_task = Task(
    description="""Generate a comprehensive welcome email using the information from previous tasks.
    
    1. Generate a complete welcome email that includes all onboarding information. The email content should be your complete output, formatted exactly as you want it to appear in the email.
    
    2. Get the teacher's email address from the gather_info_task output.
    
    3. Use the send_emails tool by passing it a JSON string that contains:
       - The teacher's email address
       - Your complete email content
       
    To use the send_emails tool, first create a dictionary with the email address and your email content, then convert it to JSON with json.dumps, like this:
    send_emails(json.dumps(dict(email=teacher_email, email_body=your_email_content)))
    
    Your output should be comprehensive and well-formatted, including all necessary information about:
    - Role assignment and responsibilities
    - Management structure and reporting lines
    - Available resources and how to access them
    - Important dates and next steps
    - Any other relevant onboarding information
    
    The email will be automatically signed as:
    Boluwatife Lambe
    Principal
    Glorylink Schools""",
    context=[gather_info_task, assign_role_task, provide_resources_task],
    agent=finalization_agent,
    expected_output="Confirmation of completed onboarding with detailed welcome email sent"
)

# Create Crew with workflow
onboarding_crew = Crew(
    agents=[recruitment_agent, role_assignment_agent, resources_agent, finalization_agent],
    tasks=[gather_info_task, assign_role_task, provide_resources_task, finalize_onboarding_task]
)

# Execute the workflow with teacher info
teacher_info = {
    "teacher_info": "Name: John Doe, Subject: Mathematics, Experience: 5 years, Email: danibholie@gmail.com"
}
result = onboarding_crew.kickoff(inputs=teacher_info)
print("\nOnboarding Result:", result)
