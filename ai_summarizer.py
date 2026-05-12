"""
AI Summarizer Module
Uses Google Gemini API for text summarization and study plan generation.
"""

import google.genai as genai
import re
from datetime import datetime

# Configure Gemini API
client = genai.Client(api_key="AIzaSyDIA37hxcxXlSr1fKIn2cQJBaYcxSupjsY")


def _convert_markdown_to_html(text):
    """Convert simple markdown-like formatting to HTML."""
    if not text:
        return ""
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    html = re.sub(r"(?m)^\*\s*", "• ", html)
    html = html.replace("\n", "<br/>")
    return html


def summarize_text(text):
    """
    Summarizes extracted PDF text using Google Gemini API.
    Returns the summary string, or a fallback message on failure.
    """
    if not text or len(text.strip()) == 0:
        return "No text provided for summarization."
    
    if not client:
        return "AI summarization not available. Please set GEMINI_API_KEY environment variable."
    
    try:
        # Truncate text to reasonable length for API
        truncated = text[:10000]  # Gemini can handle more, but limit for safety
        
        prompt = (
            "Please summarize the following text in a concise manner, and then give three actionable next steps "
            "that a student should take for this assignment.\n\n" + truncated
        )
        
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt
        )
        
        summary_text = getattr(response, 'text', None)
        if summary_text:
            return summary_text.strip()
        elif hasattr(response, 'output'):
            return str(response.output).strip()
        else:
            return "Summary not available."
    
    except Exception as e:
        print(f"[AI Summarizer] Error during summarization: {e}")
        return f"Could not generate summary: {str(e)[:100]}"


def generate_study_plan(assignments, exams, stress):
    """
    Generates a personalized daily study plan based on assignments, exams, and stress level.
    Uses Google Gemini API to analyze and create recommendations.
    """
    if not client:
        return "AI study plan generation not available. Please set GEMINI_API_KEY environment variable."
    
    try:
        # Prepare input text for AI
        today = datetime.today().date()
        
        plan_input = f"Current date: {today}\n\nAssignments:\n"
        for a in assignments:
            days_left = (datetime.strptime(a["deadline"], "%Y-%m-%d").date() - today).days
            plan_input += f"- {a['title']} (due in {days_left} days, difficulty: {a['difficulty']}, size: {a['size']})\n"
        
        plan_input += "\nExams:\n"
        for e in exams:
            days_left = (datetime.strptime(e["exam_date"], "%Y-%m-%d").date() - today).days
            plan_input += f"- {e['subject']} (in {days_left} days)\n"
        
        stress_summary = "; ".join(stress.get('reasons', [])) if isinstance(stress, dict) else str(stress)
        plan_input += f"\nStress level: {stress.get('level', 'Unknown')} - {stress_summary}\n\n"
        plan_input += (
            "Generate a detailed daily study plan for the next 7 days. "
            "List each day as a separate bullet point with specific study actions, topics to cover, and time estimates. "
            "Also include one short recommendation for how to approach the most urgent assignment."
        )
        
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=plan_input
        )
        
        plan_text = getattr(response, 'text', None)
        if plan_text:
            return plan_text.strip()
        elif hasattr(response, 'output'):
            return str(response.output).strip()
        else:
            return "Could not generate study plan."
    
    except Exception as e:
        print(f"[AI Study Planner] Error: {e}")
        return f"Could not generate study plan: {str(e)[:100]}"


def parse_study_plan_text(study_plan_text):
    """Parse raw study plan text into collapsible sections."""
    if not study_plan_text or not study_plan_text.strip():
        return []

    def _clean_title(text):
        title = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        title = title.replace("#", "")
        title = title.replace("*", "")
        return title.strip()

    lines = [line.strip() for line in study_plan_text.splitlines() if line.strip()]
    sections = []
    current_title = None
    current_body = []

    def add_section():
        if current_title is not None:
            sections.append({
                "title": _clean_title(current_title),
                "details": _convert_markdown_to_html("\n".join(current_body).strip())
            })

    for line in lines:
        normalized = line.strip('*- ').strip()
        if (normalized.lower().startswith("day ") or "day" in normalized.lower() and ':' in normalized) and len(normalized) < 80:
            add_section()
            current_title = normalized
            current_body = []
        elif line.startswith("###") or (line.startswith("**") and "day" in line.lower()):
            add_section()
            current_title = line
            current_body = []
        elif current_title is None:
            current_title = "Study Plan"
            current_body.append(line)
        else:
            current_body.append(line)

    add_section()
    if not sections and study_plan_text.strip():
        sections = [{"title": "Study Plan", "details": _convert_markdown_to_html(study_plan_text.strip())}]

    return sections


