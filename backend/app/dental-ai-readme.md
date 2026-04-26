# DentalAI

## Setup

### Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

## Technologies

- **FastAPI** and **Uvicorn** for the web framework
- **Whisper** for Speech-to-Text
- **LangChain** for LLM orchestration
- **Pydantic** for schema validation
- **Python Multipart** for audio handling
- **Loguru** for logging

## Running the Application

### Generate Test Audio
```bash
python generate_test_audio.py
```

### Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### Start the Server
```bash
python -m uvicorn app.main:app --log-level debug --port 8001
```

### Access Points
- **Endpoint:** http://127.0.0.1:8001/
- **API Documentation:** http://localhost:8001/docs#/

---

## 🦷 Dental AI Microservice  
A FastAPI-based microservice that transforms **audio recordings** of dental consultations into:

- ✔ Whisper-based **speech-to-text**  
- ✔ Structured **clinical JSON** (teeth, diagnosis, procedures, follow-up)  
- ✔ Bilingual **PT/EN dental scribe** (clinician summary + patient explanation)  
- ✔ Ensemble-validated outputs  
- ✔ Tooth-number reasoning  

This microservice is designed as the core of a future SaaS for dentists, with future integration of authentication, patient records, and clinic management.

---

## 🚀 Features

### 🎤 **1. Whisper Transcription (Speech-to-Text)**  
High-quality transcription using OpenAI Whisper.

**Pipeline:**

- Saves uploaded audio file  
- Runs Whisper (configurable model)  
- Returns clean transcription string  

Supports: `mp3`, `wav`, `m4a`, `mpeg`.

---

### 🧠 **2. Clinical Extraction (LLM Pass 1)**  
Uses an LLM to extract **structured clinical data** from the transcript:

```json
{
  "teeth": [12, 22],
  "diagnosis": ["possible sensitivity"],
  "procedures": ["further evaluation needed"],
  "follow_up_days": 7,
  "notes": "The patient reported possible sensitivity..."
}
```

#### ✅ Ensures

- **No hallucinated teeth**  
- **Enforced Pydantic schema**  
- **Notes always filled**  
- **Proper handling of numeric ranges** (e.g., `2–4`)  
- **Sanitized + validated output**

---

### 🧪 3. Ensemble Agreement System

The system runs the clinical extraction **multiple times** (default: **5 passes**) and then:

- Groups similar outputs  
- Compares:
  - **Teeth arrays**
  - **Diagnosis**
  - **Procedures**
  - **Follow-up days**
  - **Notes** (via fuzzy similarity)
- Selects the **majority-vote result**
- Returns a **confidence score (0–1)**

This dramatically increases reliability of the final clinical JSON.

---

### 🦷 4. Tooth Number Extraction & Validation

Smart parsing of FDI-compliant tooth numbers:

- `"teeth 2–4"` → `[2, 3, 4]`  
- `"tooth 12"` → `[12]`  
- `"12 or 22"` → `[12, 22]`  
- `"pain on twenty one"` → `[21]` *(optional NLP word-to-number expansion)*

Automatic cleanup:

- Removes **invalid tooth numbers**
- Removes **out-of-range values**
- Filters out **LLM hallucinations**

---

### 📝 5. PT/EN Dental Scribe Generation (LLM Pass 2)

Generates a **bilingual, clinic-ready dental report** with clinician summaries and patient-friendly explanations.

#### Example Output Schema

```json
{
  "dentist_name": null,
  "patient_name": null,
  "appointment_date": null,
  "clinic_name": null,
  "tooth_numbering_system": "FDI",

  "reason_for_appointment": null,

  "clinical_summary_pt": "...",
  "clinical_summary_en": "...",

  "patient_explanation_pt": "...",
  "patient_explanation_en": "...",

  "recommended_treatments_pt": "...",
  "recommended_treatments_en": "...",

  "next_steps_pt": "...",
  "next_steps_en": "..."
}
```

#### Includes

✔ European Portuguese (PT-PT)  
✔ Clear, empathetic patient explanations  
✔ Concise clinician summary  
✔ Metadata-safe (never invents dentist, patient or clinic names)

---

## 📁 Project Structure

```
app/
│
├── main.py
│
├── routes/
│   └── audio_routes.py
│
├── services/
│   ├── speech_to_text.py
│   ├── llm_processing.py
│   ├── llm_analysis.py
│   ├── llm_scribe.py
│   └── validation.py
│
├── models/
│   ├── dental_output.py
│   └── dental_scribe_output.py
│
├── config/
│   └── settings.py
│
└── utils/
    ├── file_handler.py
    └── logger_file.py
```

---

## 🧩 Key Components

### Pydantic Model — Clinical Output  
`models/dental_output.py`

```python
class DentalOutput(BaseModel):
    teeth: List[int]
    diagnosis: List[str]
    procedures: List[str]
    follow_up_days: int
    notes: str
```

### Pydantic Model — PT/EN Scribe Output  
`models/dental_scribe_output.py`

```python
class DentalScribeOutput(BaseModel):
    dentist_name: Optional[str] = None
    patient_name: Optional[str] = None
    appointment_date: Optional[str] = None
    clinic_name: Optional[str] = None
    tooth_numbering_system: str = "FDI"

    reason_for_appointment: Optional[str] = None

    clinical_summary_pt: str
    clinical_summary_en: str

    patient_explanation_pt: str
    patient_explanation_en: str

    recommended_treatments_pt: str
    recommended_treatments_en: str

    next_steps_pt: str
    next_steps_en: str
```

### 🧠 Clinical Extraction (LLM Pass 1)  
`services/llm_processing.py`

```python
response = model.invoke(prompt)
parsed_output = parser.parse(response.content)
return parsed_output.dict()
```

### 🧪 Ensemble Validator  
`services/llm_analysis.py`

```python
best_bucket = max(buckets, key=lambda b: len(b["results"]))
confidence = len(best_bucket["results"]) / runs
```

### 📝 Scribe Generator (LLM Pass 2)  
`services/llm_scribe.py`

```python
parsed = scribe_parser.parse(response.content)
return parsed
```

---

## 🔥 API Endpoints

### POST /audio/process  
Returns clinical structured JSON only.

**Example:**
```json
{
  "transcription": "...",
  "dental_analysis": {...},
  "confidence": 0.82
}
```

### POST /audio/scribe  
Returns clinical JSON + PT/EN scribe.

**Example:**
```json
{
  "transcription": "...",
  "clinical": {...},
  "scribe": {...},
  "confidence": 0.87
}
```

---

## 🦷 Example Full Output

```json
{
  "transcription": "The patient might have sensitivity...",
  "clinical": {
    "teeth": [12, 22],
    "diagnosis": ["possible sensitivity"],
    "procedures": ["further evaluation needed"],
    "follow_up_days": 7,
    "notes": "The patient reported possible sensitivity..."
  },
  "scribe": {
    "dentist_name": null,
    "patient_name": null,
    "appointment_date": null,
    "clinic_name": null,
    "tooth_numbering_system": "FDI",
    "reason_for_appointment": null,
    "clinical_summary_pt": "...",
    "clinical_summary_en": "...",
    "patient_explanation_pt": "...",
    "patient_explanation_en": "...",
    "recommended_treatments_pt": "...",
    "recommended_treatments_en": "...",
    "next_steps_pt": "...",
    "next_steps_en": "..."
  },
  "confidence": 0.6
}
```

---

## 🚀 Future Improvements

### Before backend:

- 🎭 Scribe styles (clinical / patient / SOAP / insurance)  
- 🔊 Audio noise reduction  
- 🤖 Whisper model auto-selection  
- 🧍 Multi-speaker segmentation  
- 🦷 Tooth map visualizer  
- 🛡 Scribe validation layer  
- 📄 PDF export (PT/EN)

### After backend:

- 🔐 Authentication (JWT)  
- 🧑‍⚕️ Dentist profiles  
- 🧑‍🦱 Patient profiles  
- 📅 Appointments  
- 🏥 Clinic settings  
- 💾 Metadata injection into scribe  
- 📈 Longitudinal patient tracking

---

## 📌 Summary

This microservice includes:

✔ Whisper transcription  
✔ Clinical JSON extraction  
✔ Ensemble validation  
✔ PT/EN scribe report  
✔ Metadata-safe architecture  
✔ FastAPI endpoints  
✔ Modular, clean project structure