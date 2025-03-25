import streamlit as st
import base64
import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool, MDXSearchTool,PDFSearchTool
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# Set up API keys (replace with your method to get keys)
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = 'gemini/gemini-2.0-flash-lite'
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")  # or get_serper_api_key()

from crewai import LLM

llm = LLM(
    model="gemini/gemini-1.5-pro-latest",
    temperature=0.7,
)
# Define tools that don't depend on the resume
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Streamlit app layout
st.title("Job Application Assistant")
st.write("Upload your resume and provide details to generate a tailored resume and interview materials.")

# Input fields
job_posting_url = st.text_input("Job Posting URL", placeholder="e.g., https://jobs.lever.co/...")
github_url = st.text_input("GitHub URL", placeholder="e.g., https://github.com/username")
personal_writeup = st.text_area("Personal Write-up", height=200, placeholder="Describe yourself and your experience...")
resume_file = st.file_uploader("Upload Your Resume (Markdown)", type=["md"])

# Process inputs when the user clicks "Generate"
if st.button("Generate"):
    if not all([job_posting_url, github_url, personal_writeup, resume_file]):
        st.error("Please provide all required inputs.")
    else:
        # Save uploaded resume to a temporary file
        with open("temp_resume.md", "wb") as f:
            f.write(resume_file.getbuffer())

        # Define resume-dependent tools
        read_resume = FileReadTool(file_path="temp_resume.md")
        semantic_search_resume = MDXSearchTool(mdx="temp_resume.md")

        # Define agents
        researcher = Agent(
            role="Tech Job Researcher",
            goal="Make sure to do amazing analysis on job posting to help job applicants",
            tools=[scrape_tool, search_tool],
            verbose=True,
            backstory=(
                "As a Job Researcher, your prowess in navigating and extracting critical "
                "information from job postings is unmatched. Your skills help pinpoint the "
                "necessary qualifications and skills sought by employers, forming the "
                "foundation for effective application tailoring."
            )
        )

        profiler = Agent(
            role="Personal Profiler for Engineers",
            goal="Do incredible research on job applicants to help them stand out in the job market",
            tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
            verbose=True,
            backstory=(
                "Equipped with analytical prowess, you dissect and synthesize information "
                "from diverse sources to craft comprehensive personal and professional profiles, "
                "laying the groundwork for personalized resume enhancements."
            )
        )

        resume_strategist = Agent(
            role="Resume Strategist for Engineers",
            goal="Find all the best ways to make a resume stand out in the job market.",
            tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
            verbose=True,
            backstory=(
                "With a strategic mind and an eye for detail, you excel at refining resumes "
                "to highlight the most relevant skills and experiences, ensuring they resonate "
                "perfectly with the job's requirements."
            )
        )

        interview_preparer = Agent(
            role="Engineering Interview Preparer",
            goal="Create interview questions and talking points based on the resume and job requirements",
            tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
            verbose=True,
            backstory=(
                "Your role is crucial in anticipating the dynamics of interviews. With your "
                "ability to formulate key questions and talking points, you prepare candidates "
                "for success, ensuring they can confidently address all aspects of the job."
            )
        )

        # Define tasks
        research_task = Task(
            description=(
                "Analyze the job posting URL provided ({job_posting_url}) to extract key skills, "
                "experiences, and qualifications required. Use the tools to gather content and "
                "identify and categorize the requirements."
            ),
            expected_output=(
                "A structured list of job requirements, including necessary skills, qualifications, "
                "and experiences."
            ),
            agent=researcher,
            async_execution=True
        )

        profile_task = Task(
            description=(
                "Compile a detailed personal and professional profile using the GitHub ({github_url}) "
                "URLs, and personal write-up ({personal_writeup}). Utilize tools to extract and "
                "synthesize information from these sources."
            ),
            expected_output=(
                "A comprehensive profile document that includes skills, project experiences, "
                "contributions, interests, and communication style."
            ),
            agent=profiler,
            async_execution=True
        )

        resume_strategy_task = Task(
            description=(
                "Using the profile and job requirements obtained from previous tasks, tailor the "
                "resume to highlight the most relevant areas. Employ tools to adjust and enhance "
                "the resume content. Make sure this is the best resume ever but don't make up any "
                "information. Update every section, including the initial summary, work experience, "
                "skills, and education, to better reflect the candidate's abilities and how it "
                "matches the job posting."
            ),
            expected_output=(
                "An updated resume that effectively highlights the candidate's qualifications and "
                "experiences relevant to the job."
            ),
            output_file="tailored_resume.md",
            context=[research_task, profile_task],
            agent=resume_strategist
        )

        interview_preparation_task = Task(
            description=(
                "Create a set of potential interview questions and talking points based on the "
                "tailored resume and job requirements. Utilize tools to generate relevant questions "
                "and discussion points. Make sure to use these questions and talking points to help "
                "the candidate highlight the main points of the resume and how it matches the job "
                "posting."
            ),
            expected_output=(
                "A document containing key questions and talking points that the candidate should "
                "prepare for the initial interview."
            ),
            output_file="interview_materials.md",
            context=[research_task, profile_task, resume_strategy_task],
            agent=interview_preparer
        )

        # Create and run the crew
        job_application_crew = Crew(
            agents=[researcher, profiler, resume_strategist, interview_preparer],
            tasks=[research_task, profile_task, resume_strategy_task, interview_preparation_task],
            verbose=True
        )

        # Input dictionary
        job_application_inputs = {
            'job_posting_url': job_posting_url,
            'github_url': github_url,
            'personal_writeup': personal_writeup
        }

        # Execute with a spinner for user feedback
        with st.spinner("Generating tailored resume and interview materials... This may take a few minutes."):
            try:
                job_application_crew.kickoff(inputs=job_application_inputs)

                # Display tailored resume
                if os.path.exists("tailored_resume.md"):
                    with open("tailored_resume.md", "r") as f:
                        tailored_resume = f.read().replace("```", "")
                    st.markdown("### Tailored Resume")
                    st.markdown(tailored_resume)
                    st.download_button(
                        label="Download Tailored Resume",
                        data=tailored_resume,
                        file_name="tailored_resume.md",
                        mime="text/markdown"
                    )
                else:
                    st.warning("Tailored resume file not found.")

                # Display interview materials
                if os.path.exists("interview_materials.md"):
                    with open("interview_materials.md", "r") as f:
                        interview_materials = f.read().replace("```", "")
                    st.markdown("### Interview Materials")
                    st.markdown(interview_materials)
                    st.download_button(
                        label="Download Interview Materials",
                        data=interview_materials,
                        file_name="interview_materials.md",
                        mime="text/markdown"
                    )
                else:
                    st.warning("Interview materials file not found.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")