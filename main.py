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
from twilio.rest import Client

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

class WhatsappMessageSenderTool:
    def __init__(self):
        # Get whatsapp credentials from environment variables
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.whatsapp_from = os.getenv("WHATSAPP_FROM_NUMBER")

        if not all([twilio_account_sid, twilio_auth_token, self.whatsapp_from]):
            raise ValueError("Missing required WhatsApp configuration in environment variables")

        self.client = Client(twilio_account_sid, twilio_auth_token)

    def send_message(self, phone_number: str, message_body: str) -> str:
        """Send a WhatsApp message to the specified phone number.
        
        Args:
            phone_number (str): The recipient's phone number in international format (e.g., +2348012345678)
            message_body (str): The message to send
        
        Returns:
            str: Status message indicating whether the message was sent successfully
        """
        try:
            message = self.client.messages.create(
                from_=f"whatsapp:{self.whatsapp_from}",
                body=message_body,
                to=f"whatsapp:{phone_number}"
            )
            return f"✅ WhatsApp message sent to {phone_number}"
        except Exception as e:
            return f"❌ Error sending WhatsApp message: {str(e)}"


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

@tool("Whatsapp Message")
def send_whatsapp_message(onboarding_data: str) -> str:
    """Send onboarding whatsapp message to the newly appointed teacher.
    
    Args:
        onboarding_data (str): JSON string containing teacher's phone number and message body
    
    Returns:
        str: Status message indicating whether the message was sent successfully
    """
    try:
        # Parse the onboarding data
        import json
        data = json.loads(onboarding_data)
        
        # Send the WhatsApp message
        whatsapp_sender = WhatsappMessageSenderTool()
        result = whatsapp_sender.send_message(
            phone_number=data['phone_number'],
            message_body=data['message_body']
        )
        
        return result
    except Exception as e:
        return f"❌ Error in WhatsApp message sending process: {str(e)}"


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
    goal="Send final onboarding communications to the teacher",
    backstory="""You are responsible for finalizing the onboarding process by sending welcome communications to the teacher.
    You craft personalized messages that are professional and welcoming.""",
    llm=llm,
    tools=[send_emails, send_whatsapp_message],
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
    - Phone Number
    Return this information in a clear, structured format.""",
    agent=recruitment_agent,
    expected_output="Structured teacher details including name, subject expertise, email, phone number and experience"
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
    description="""Using the collected and verified teacher information, send the final onboarding communications:
    
    1. Send a detailed welcome email containing:
       - A warm welcome message
       - Their assigned role and responsibilities
       - Important school policies
       - Next steps and orientation details
       - Contact information for their department head
       The email should be signed by:
       Boluwatife Lambe
       Principal
       Glorylink Schools
    
    2. Send a WhatsApp message with the following format:
       "🎉 Congratulations [Teacher Name]! Your onboarding to Glorylink Schools is complete. We've sent a detailed welcome package to your email ([Email Address]). Please check it for important information about your role and next steps. We're excited to have you join our team! 🌟"
    
    For both communications:
    1. Use the teacher's information from the gather_info_task output
    2. Use the send_emails tool for email (pass a JSON with 'email' and 'email_body')
    3. Use the send_whatsapp_message tool for WhatsApp (pass a JSON with 'phone_number' and 'message_body')
    
    Ensure ALL placeholder text is replaced with actual information from the previous tasks.""",
    context=[gather_info_task, assign_role_task, provide_resources_task],
    agent=finalization_agent,
    expected_output="Confirmation of completed onboarding with detailed welcome email and WhatsApp message sent"
)

# Create Crew with workflow
onboarding_crew = Crew(
    agents=[recruitment_agent, role_assignment_agent, resources_agent, finalization_agent],
    tasks=[gather_info_task, assign_role_task, provide_resources_task, finalize_onboarding_task]
)

# Execute the workflow with teacher info
teacher_info = {
    "teacher_info": "Name: Lambe Boluwatife, Subject: Mathematics, Experience: 5 years, Email: danibholie@gmail.com, Phone Number: +2348083647531"
}
result = onboarding_crew.kickoff(inputs=teacher_info)
print("\nOnboarding Result:", result)
