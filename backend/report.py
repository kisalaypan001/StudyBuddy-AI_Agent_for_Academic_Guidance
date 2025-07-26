import os
from dotenv import load_dotenv
from groq import Groq
from models import *
import csv
import io 
import re
from playwright.sync_api import sync_playwright
from flask import jsonify, request
from datetime import datetime
import json

# Load .env variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# File paths
html_path = "templates/report.html"
pdf_path = "templates/Report.pdf"

def html_to_pdf(html_path, pdf_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"http://127.0.0.1:5000/{html_path}", wait_until="networkidle")
        page.pdf(path=pdf_path, format="A4")
        browser.close()

def analysis_and_report_f(subject):
    try:
        # Step 1: Fetch marks
        if subject:
            marks = Marks.query.filter_by(subject=subject).all()
        else:
            marks = Marks.query.all()

        for mark in marks:
            student = Student.query.filter_by(roll_no=mark.roll_no).first()
            mark.name = student.name if student else ""

        # Step 2: Convert to CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["roll_no", "name", "quiz_1", "quiz_2", "end_term"])
        for m in marks:
            writer.writerow([m.roll_no, m.name, m.quiz_1, m.quiz_2, m.end_term])
        csv_data = output.getvalue()
        output.close()

        # Step 3: Generate HTML report using Groq
        client = Groq(api_key=GROQ_API_KEY)
        curr_date = datetime.now()
        prompt = f"""
Generate a **fully-structured and comprehensive HTML report** based on the following student performance data:

{csv_data}

The report should include the following components:
1. Header Section - Title: 'Student Performance Report - {subject}', Date: {curr_date}
2. Summary Section - Total number of students, Subject name, Class-wide averages
3. Descriptive Statistics - Mean, median, mode, and standard deviation for each assessment
4. Visualizations (using Chart.js)
5. Student-wise Performance Table
"""

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="deepseek-r1-distill-llama-70b"
        )

        html_response = chat_completion.choices[0].message.content
        match = re.search(r'<!DOCTYPE html>.*?</html>', html_response, re.DOTALL)
        summary_prompt = match.group() if match else html_response

        with open(html_path, "w", encoding="utf-8") as file:
            file.write(summary_prompt)

        # Step 4: Generate summary
        summary_prompt_text = f"""Summarize the statistics in the following HTML document in 200 words.dont mention the word HTML document.
Return output in JSON format either as:
- [{{"summary": "..."}}]
- {{"summary": "..."}}

HTML:
{summary_prompt}
"""
        summary_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": summary_prompt_text}],
            model="deepseek-r1-distill-llama-70b"
        )

        raw_summary = summary_completion.choices[0].message.content
        # print("SUMMARY RAW OUTPUT:\n", raw_summary)

        # Step 5: Extract JSON summary
        report_summary = [{"summary": "Summary could not be parsed."}]
        try:
            # Try extracting JSON in backticks first
            match = re.search(r"```(?:json)?\s*({.*?}|\[\s*\{.*?\}\s*\])\s*```", raw_summary, re.DOTALL)
            if not match:
                # Try plain JSON
                match = re.search(r"{.*?}", raw_summary, re.DOTALL) or \
                        re.search(r"\[\s*\{.*?\}\s*\]", raw_summary, re.DOTALL)
            if match:
                json_text = match.group().strip()
                json_text = re.sub(r"^```(?:json)?|```$", "", json_text.strip())
                parsed = json.loads(json_text)
                report_summary = [parsed] if isinstance(parsed, dict) else parsed
        except Exception as e:
            print("❌ JSON extraction error:", e)

        summary_text = report_summary[0].get("summary", "Summary unavailable.")

        # Step 6: Generate PDF
        html_to_pdf(html_path, pdf_path)

        # Final response
        return {
            "response": {
                "summary": str(summary_text),  # Return the summary text
                "pdf_ready": True,
                "html_report_path": str(html_path),
                "pdf_report_path": str(pdf_path)
            }
        }

    except Exception as e:
        print("❌ Full report generation failed:", e)
        return {
            "response": {
                "summary": "Summary unavailable due to internal error.",
                "pdf_ready": False,
                "html_report_path": "",
                "pdf_report_path": ""
            }
        }