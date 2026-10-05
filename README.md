# AI University Admission Advisor

A modular multi-agent university admission advisory system built with:

- Streamlit
- CrewAI
- Groq GPT-OSS 120B
- Official Groq Python SDK

## Agents

1. Requirements Analyst
2. Eligibility Evaluator
3. Program Recommendation Specialist
4. Senior Admission Advisor

Workflow:

Requirements → Eligibility → Program Recommendation → Final Advisor

## Important design choice

The application does not invent current university requirements.

The user pastes the university's official requirements into the app. The agents analyze only that supplied information. This makes the first version safer and easier to deploy.

## Project structure

```text
university-admission-ai/
├── app.py
├── admission_crew.py
├── config.py
├── llm.py
├── requirements.txt
├── .gitignore
├── README.md
├── agents/
│   ├── __init__.py
│   ├── requirements_agent.py
│   ├── eligibility_agent.py
│   ├── program_agent.py
│   └── advisor_agent.py
└── tasks/
    ├── __init__.py
    ├── requirements_task.py
    ├── eligibility_task.py
    ├── program_task.py
    └── advisor_task.py
```

## Streamlit Cloud secret

Add this in Streamlit Cloud → App settings → Secrets:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

Optional model override:

```toml
GROQ_MODEL = "openai/gpt-oss-120b"
```

The API key is never stored in GitHub.

## GitHub deployment

1. Create a new GitHub repository.
2. Upload all files while preserving the folders.
3. Open Streamlit Community Cloud.
4. Create a new app.
5. Select the GitHub repository and branch.
6. Select `app.py` as the main file.
7. Open Advanced settings.
8. Select Python 3.12.
9. Add the `GROQ_API_KEY` secret.
10. Deploy.

## Disclaimer

This is an AI advisory system, not an official university admissions decision system. Applicants should verify final requirements, deadlines, merit, and eligibility with the university.
