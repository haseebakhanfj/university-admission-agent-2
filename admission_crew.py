from crewai import Crew, Process

from agents.requirements_agent import create_requirements_agent
from agents.eligibility_agent import create_eligibility_agent
from agents.program_agent import create_program_agent
from agents.advisor_agent import create_advisor_agent

from tasks.requirements_task import create_requirements_task
from tasks.eligibility_task import create_eligibility_task
from tasks.program_task import create_program_task
from tasks.advisor_task import create_advisor_task


def run_admission_crew(applicant: dict, requirements: str) -> dict:
    requirements_agent = create_requirements_agent()
    eligibility_agent = create_eligibility_agent()
    program_agent = create_program_agent()
    advisor_agent = create_advisor_agent()

    requirements_task = create_requirements_task(requirements_agent)
    eligibility_task = create_eligibility_task(
        eligibility_agent,
        requirements_task,
    )
    program_task = create_program_task(
        program_agent,
        requirements_task,
        eligibility_task,
    )
    advisor_task = create_advisor_task(
        advisor_agent,
        requirements_task,
        eligibility_task,
        program_task,
    )

    crew = Crew(
        agents=[
            requirements_agent,
            eligibility_agent,
            program_agent,
            advisor_agent,
        ],
        tasks=[
            requirements_task,
            eligibility_task,
            program_task,
            advisor_task,
        ],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff(
        inputs={
            "applicant": applicant,
            "requirements": requirements,
        }
    )

    outputs = crew.tasks

    return {
        "requirements_analysis": str(outputs[0].output),
        "eligibility_analysis": str(outputs[1].output),
        "program_recommendation": str(outputs[2].output),
        "final_report": str(result),
    }
