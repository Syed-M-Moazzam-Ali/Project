# AI Application Generator

A Streamlit web app that converts basic user information into a formal application/letter. It can use the OpenAI API for AI generation or run in Template mode without an API key.

## Features

- Country and province/state input
- Concerned department/organization input
- Applicant name input
- Issue description input
- Formal, polite, firm, or urgent tone
- AI mode with safe fallback to Template mode
- TXT download
- DOCX download
- GitHub + Streamlit Community Cloud ready

## Project Structure

```text
AI-Application-Generator/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
└── .streamlit/
    └── secrets.toml.example
```

## Run Locally

1. Install Python 3.10 or newer.
2. Clone the repository.
3. Create and activate a virtual environment (recommended).
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. For AI mode, create a `.env` file:

```text
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5-mini
```

6. Start the app:

```bash
streamlit run app.py
```

Template mode works even if no API key is configured.

## Upload to GitHub

From the project folder:

```bash
git init
git add .
git commit -m "Initial AI Application Generator"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Do **not** upload `.env` or `.streamlit/secrets.toml`. They are already excluded by `.gitignore`.

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Sign in to Streamlit Community Cloud.
3. Create a new app and select your GitHub repository.
4. Set the main file path to:

```text
app.py
```

5. Open the app's **Secrets** settings and add:

```toml
OPENAI_API_KEY = "your_openai_api_key_here"
```

6. Deploy the app.

If the API key is missing or an AI request fails, the app automatically produces a template-based application instead.

## Security

Never commit your API key to GitHub. Use Streamlit Secrets for deployment and environment variables or a local `.env` file during development.

## Technologies

- Python
- Streamlit
- OpenAI Responses API
- python-docx
- python-dotenv
