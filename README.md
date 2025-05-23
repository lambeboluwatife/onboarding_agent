# Teacher Onboarding System

An automated system that handles the onboarding process for new teachers using AI agents. The system collects teacher information, assigns appropriate roles, provides resources, and sends comprehensive welcome emails.

## Features

- **Automated Role Assignment**: Analyzes teacher qualifications and experience to assign the most suitable role
- **Resource Management**: Automatically compiles and provides role-specific resources
- **Email Automation**: Sends personalized welcome emails with complete onboarding information
- **Management Structure**: Provides detailed information about reporting lines and team structure

## System Components

### Agents

1. **Recruitment Agent**
   - Collects and verifies teacher details
   - Ensures accuracy of information

2. **Role Assignment Agent**
   - Determines suitable roles based on qualifications
   - Provides management structure details
   - Uses predefined role requirements

3. **Resources Agent**
   - Compiles role-specific resources
   - Manages access to teaching materials and tools

4. **Finalization Agent**
   - Generates comprehensive welcome emails
   - Ensures all onboarding steps are completed
   - Sends automated communications

## Setup

1. Clone the repository
```bash
git clone [repository-url]
cd onboarding
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file with the following:
```plaintext
OPENAI_API_KEY=your_openai_api_key
EMAIL_USER=your_email
EMAIL_PASSWORD=your_email_app_password
```

## Configuration

### Role Configuration
Roles and their requirements are defined in `config.py`:
- Senior Mathematics Teacher
- Mathematics Teacher
- Junior Mathematics Teacher

Each role includes:
- Minimum experience requirements
- Responsibilities
- Required resources

## Usage

1. Run the onboarding process:
```bash
python main.py
```

2. Input teacher information in the following format:
```python
teacher_info = {
    "teacher_info": "Name: [name], Subject: Mathematics, Experience: [years], Email: [email]"
}
```

## Email Templates

The system sends comprehensive welcome emails including:
- Role assignment and responsibilities
- Management structure details
- Resource access information
- Important dates and next steps
- Contact information for supervisors

## Security

- Sensitive credentials are stored in environment variables
- `.gitignore` configured to exclude sensitive files
- Email credentials secured using environment variables

## Dependencies

- CrewAI: For agent-based automation
- OpenAI: For language model integration
- Python-dotenv: For environment variable management
- Emails: For email automation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Here]

## Contact

[Your Contact Information]
#   o n b o a r d i n g - c r e w a i  
 