"""
AI Application Generator
Run locally: streamlit run app.py
Deploy: push to GitHub and connect to Streamlit Community Cloud.
"""

from __future__ import annotations

import os
from datetime import date
from io import BytesIO
from typing import Optional

import streamlit as st
from docx import Document
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

APP_TITLE = "AI Application Generator"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")


def get_api_key() -> Optional[str]:
    """Read API key from Streamlit secrets or environment variables."""
    try:
        key = st.secrets.get("OPENAI_API_KEY")
        if key:
            return str(key)
    except Exception:
        pass
    return os.getenv("OPENAI_API_KEY")


def clean_text(value: str) -> str:
    return " ".join(value.strip().split())


def validate_inputs(country: str, province: str, department: str, person_name: str, issue: str) -> list[str]:
    errors: list[str] = []
    if not clean_text(country):
        errors.append("Country is required.")
    if not clean_text(province):
        errors.append("Province/State is required.")
    if not clean_text(department):
        errors.append("Concerned department is required.")
    if not clean_text(person_name):
        errors.append("Applicant/person name is required.")
    if len(clean_text(issue)) < 20:
        errors.append("Issue description should contain at least 20 characters.")
    return errors


def build_prompt(country: str, province: str, department: str, person_name: str, issue: str, tone: str) -> str:
    return f"""
You are a professional formal application writing assistant.

Prepare a complete official application using only the information provided by the user.

Input data:
- Country: {country}
- Province/State: {province}
- Concerned Department/Organization: {department}
- Applicant Name: {person_name}
- Issue Description: {issue}
- Tone: {tone}

Output requirements:
1. Create a suitable subject line.
2. Use a formal application format.
3. Address the concerned authority respectfully.
4. Explain the issue clearly and professionally.
5. Mention the impact only if it is supported by the user's issue description.
6. Request practical action from the department.
7. Do not invent laws, case numbers, addresses, officers, phone numbers, CNIC numbers, or dates.
8. Keep the application concise, polite, and ready for submission.
9. Include closing with the applicant's name.

Return only the final application text.
""".strip()


def template_application(country: str, province: str, department: str, person_name: str, issue: str, tone: str) -> str:
    """Offline fallback when no API key is available."""
    issue_clean = issue.strip()
    tone_line = "respectfully" if tone.lower() != "firm" else "formally and firmly"
    return f"""Date: {date.today().strftime('%B %d, %Y')}

To,
The Concerned Authority,
{department},
{province}, {country}.

Subject: Request for Necessary Action Regarding the Reported Issue

Respected Sir/Madam,

I, {person_name}, would like to {tone_line} bring to your attention the following matter:

{issue_clean}

This issue requires the attention of your department. I therefore request your good office to kindly review the matter and take the necessary action as per applicable procedure.

I shall be grateful for your prompt consideration and support.

Yours faithfully,

{person_name}
""".strip()


def generate_with_openai(prompt: str, model: str) -> str:
    client = OpenAI(api_key=get_api_key())
    response = client.responses.create(model=model, input=prompt)
    return response.output_text.strip()


def make_docx(application_text: str) -> BytesIO:
    document = Document()
    for paragraph in application_text.split("\n"):
        document.add_paragraph(paragraph)
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    return buffer


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="📝", layout="centered")

    st.title("📝 AI Application Generator")
    st.write("Generate a formal application from basic user information.")

    with st.sidebar:
        st.header("Settings")
        mode = st.radio("Generation mode", ["AI mode", "Template mode"], help="Template mode works without an API key.")
        model = st.text_input("OpenAI model", value=DEFAULT_MODEL)
        tone = st.selectbox("Tone", ["Formal", "Polite", "Firm", "Urgent"])
        st.caption("Do not upload API keys to GitHub. Use Streamlit Secrets or environment variables.")

    st.subheader("Input Details")
    country = st.text_input("Country", placeholder="Pakistan")
    province = st.text_input("Province / State", placeholder="Sindh")
    department = st.text_input("Department of Concern", placeholder="Water and Sewerage Department")
    person_name = st.text_input("Name of Person / Applicant", placeholder="Muhammad Ali")
    issue = st.text_area("Brief write-up about the issue", height=180, placeholder="Describe the issue, affected area, duration, and requested action.")

    if st.button("Generate Application", type="primary", use_container_width=True):
        errors = validate_inputs(country, province, department, person_name, issue)
        if errors:
            for error in errors:
                st.error(error)
            return

        with st.spinner("Generating application..."):
            try:
                if mode == "AI mode":
                    if not get_api_key():
                        st.warning("OPENAI_API_KEY not found. Using Template mode instead.")
                        application = template_application(country, province, department, person_name, issue, tone)
                    else:
                        prompt = build_prompt(country, province, department, person_name, issue, tone)
                        application = generate_with_openai(prompt, model)
                else:
                    application = template_application(country, province, department, person_name, issue, tone)
            except Exception as exc:
                st.error(f"AI generation failed: {exc}")
                st.info("Fallback template generated below.")
                application = template_application(country, province, department, person_name, issue, tone)

        st.success("Application generated successfully.")
        st.subheader("Generated Application")
        st.text_area("Application text", value=application, height=460)

        docx_buffer = make_docx(application)
        st.download_button(
            label="Download Application as DOCX",
            data=docx_buffer,
            file_name="generated_application.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )

    st.divider()
    st.caption("Built with Python, Streamlit, OpenAI API, and python-docx.")


if __name__ == "__main__":
    main()
