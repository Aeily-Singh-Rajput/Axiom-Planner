# Axiom Planner

AI-assisted academic workload scheduler.

---

## Project Structure

```
axiom_planner/
│
├── app.py                         # Flask entry point
├── requirements.txt               # Python dependencies
│
├── routes/                        # All Flask route blueprints
│   ├── dashboard_routes.py        # GET / → dashboard
│   ├── assignment_routes.py       # POST /add_assignment, /delete_assignment/<id>
│   ├── exam_routes.py             # POST /add_exam, /delete_exam/<id>
│   ├── scheduler_routes.py        # GET /get_schedule (JSON)
│   └── upload_routes.py           # GET/POST /upload, /upload_pdf
│
├── modules/                       # Core logic modules
│   ├── data_manager.py            # Read/write assignments & exams JSON
│   ├── scheduler.py               # Workload distribution across days
│   ├── stress_calculator.py       # Stress level estimation
│   ├── pdf_extractor.py           # PDF text extraction (PyPDF2)
│   ├── ai_summarizer.py           # Hugging Face API call for summary
│   └── visualizer.py              # Matplotlib workload chart
│
├── templates/                     # HTML templates (Jinja2)
│   ├── dashboard.html             # Main dashboard page
│   └── upload.html                # PDF upload page
│
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/                    # Auto-created; stores workload_chart.png
│
└── data/
    ├── assignments.json            # Stored assignments
    └── exams.json                  # Stored exams
```

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Hugging Face API token
#    Open modules/ai_summarizer.py
#    Set: HF_API_TOKEN = "your_token_here"

# 3. Run the app
python app.py
```

Open http://127.0.0.1:5000 in your browser.

---

## API Key Locations

| API            | File                         | Variable        |
|----------------|------------------------------|-----------------|
| Hugging Face   | modules/ai_summarizer.py     | HF_API_TOKEN    |

---

## Routes Summary

| Method | URL                              | Purpose                      |
|--------|----------------------------------|------------------------------|
| GET    | /                                | Dashboard page               |
| POST   | /add_assignment                  | Add new assignment           |
| POST   | /delete_assignment/<id>          | Delete assignment            |
| POST   | /add_exam                        | Add new exam                 |
| POST   | /delete_exam/<id>                | Delete exam                  |
| GET    | /upload                          | Upload page                  |
| POST   | /upload_pdf                      | Upload PDF & get summary     |
| GET    | /get_schedule                    | Schedule as JSON             |

---

## Notes

- Data is stored as plain JSON files in `/data`. No database needed.
- The workload chart is saved to `static/images/workload_chart.png`.
- Call `generate_workload_chart(schedule)` from `modules/visualizer.py`
  in `dashboard_routes.py` if you want to show the chart image.