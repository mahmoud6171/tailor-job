# Job Application Assistant

This Streamlit app leverages [CrewAI](https://crewai.com/) to help users refine their resumes and prepare for interviews based on specific job postings. By analyzing job requirements and personal profiles, the app generates tailored resumes and interview materials to enhance job application success.

---

## Table of Contents

- [Job Application Assistant](#job-application-assistant)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
  - [Usage](#usage)
  - [Output Files](#output-files)
  - [CrewAI Setup](#crewai-setup)
  - [Troubleshooting](#troubleshooting)
  - [Known Limitations](#known-limitations)
  - [Contributing](#contributing)

---

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.10 or higher**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **API Keys**:
    - [OpenAI API Key](https://platform.openai.com/signup)
    - [Serper API Key](https://serper.dev/)

---

## Installation

1. **Clone the repository**:
        ```bash
        git clone https://github.com/mahmoud6171/tailor-job.git
        cd tailor-job
        ```
2. **Set up a virtual environment**:
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        ```
3. **Install the required dependencies**:
        ```bash
        pip install -r requirements.txt
        ```

## Running the App

**Run the Streamlit app**:
```bash
streamlit run app.py
```

## Usage

1. **Enter the job posting URL**: Provide the URL of the job you're applying for.
2. **Enter your GitHub URL**: Link to your GitHub profile for project and contribution analysis.
3. **Write a personal write-up**: Describe your experience, skills, and career goals.
4. **Upload your resume**: Upload your current resume in Markdown (.md) format.
5. **Click "Generate"**: The app will process your inputs and generate a tailored resume and interview materials.

## Output Files

The app generates two key files:

- `tailored_resume.md`: An updated resume that highlights your qualifications and experiences relevant to the job posting.
- `interview_materials.md`: A set of potential interview questions and talking points based on the job requirements and your profile.

These files can be viewed directly in the app and downloaded for further use.

## CrewAI Setup

The app utilizes four CrewAI agents to achieve its functionality. These agents work together to provide a comprehensive toolkit for job applications.

## Troubleshooting

- **Missing API keys**: Ensure you have set the `OPENAI_API_KEY` and `SERPER_API_KEY` environment variables correctly.
    Dependency conflicts: Verify that all required libraries are installed by running pip install -r requirements.txt.
    Incorrect Python version: The app requires Python 3.10 or higher. Check your version with python --version.
- **Dependency conflicts**: Verify that all required libraries are installed by running `pip install -r requirements.txt`.
- **Incorrect Python version**: The app requires Python 3.10 or higher. Check your version with `python --version`.
- **File not found errors**: Ensure the uploaded resume is in Markdown format and correctly processed.
Known Limitations

: The app currently supports only Markdown (.md) resumes. Future updates may include support for other formats like PDF or DOCX.
## Known Limitations
- **Processing Time** : Depending on the complexity of the inputs and API response times, generating the outputs may take a few minutes.
- **Resume Format**: The app currently supports only Markdown (.md) resumes. Future updates may include support for other formats like PDF or DOCX.

- **API Dependencies**: The app relies on external APIs (OpenAI and Serper), so ensure your API keys are valid and have sufficient usage limits.Contributing

## Contributing 

Contributions are welcome! If you'd like to improve the app, report issues, or suggest features, please:    Fork the repository.
for your feature or fix.
1. Fork the repository.on of your changes.
2. Create a new branch for your feature or fix.
3. Submit a pull request with a clear description of your changes.F