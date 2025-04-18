import json
import os
import logging
from flask import Flask, render_template, request, abort

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key')
app.config['JSON_SORT_KEYS'] = False  # Preserve JSON order
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

# Sample data for the forms
def load_data():
    return {
        "set1": {
            "medical_expense": {
                "claim_number": "WCB123456789",
                "worker_name": "John Smith",
                "worker_app_id": "APP00123",
                "submitted_date": "2023-04-15",
                "prescription_drugs": [
                    ["Amoxicillin", "2023-03-01", "2023-03-02", "Dr. Johnson", "$24.99"],
                    ["Ibuprofen", "2023-03-10", "2023-03-11", "Dr. Williams", "$12.50"]
                ],
                "otc_drugs": [
                    ["Tylenol", "2023-03-05", "$9.99", "Walmart Pharmacy", "Pain relief"],
                    ["Advil", "2023-03-15", "$11.50", "CVS Pharmacy", "Inflammation"]
                ],
                "medical_supplies": [
                    ["Wrist Brace", "2023-03-03", "Yes", "Dr. Wilson", "$45.99", "Medical Supply Co."],
                    ["Bandages", "2023-03-12", "No", "N/A", "$7.50", "Pharmacy Plus"]
                ],
                "parking": [
                    ["Central Medical Center, 123 Health St.", "2023-03-02", "$5.00", "Yes", "M2459"],
                    ["City Hospital, 456 Care Ave.", "2023-03-10", "$8.00", "No", "N/A"]
                ],
                "mileage": [
                    ["2023-03-02", "Central Medical Center, 123 Health St.", "Industrial Park, 789 Work Rd.", "24 km"],
                    ["2023-03-10", "City Hospital, 456 Care Ave.", "Industrial Park, 789 Work Rd.", "32 km"]
                ],
                "bus_taxi": [
                    ["2023-03-15", "Home, 321 Residence Ln.", "Physical Therapy Center, 654 Recovery Rd.", "Bus", "$4.50"],
                    ["2023-03-20", "Home, 321 Residence Ln.", "Dr. Williams Office, 987 Medicine Ave.", "Taxi", "$25.00"]
                ]
            },
            "worker_progress": {
                "claim_number": "WCB123456789",
                "worker_name": "John Smith",
                "worker_app_id": "APP00123",
                "submitted_date": "2023-04-15",
                "return_to_work": {
                    "status": "I returned to work on:",
                    "date": "2023-03-20",
                    "working_status": "Modified duties, reduced hours",
                    "progress": "My wrist is still sore, but I am able to perform light duties. My supervisor has been very accommodating.",
                    "expected_return": "2023-05-01",
                    "concerns": "I'm concerned about being able to lift heavy items again.",
                    "employer_contact": "Jane Doe, HR Manager",
                    "contact_date": "2023-04-10"
                },
                "recovery": {
                    "status": "I have not fully recovered from my workplace injury.",
                    "comments": "I am making steady progress but still experience pain when using my wrist for extended periods.",
                    "pain_level": 4,
                    "treatment_status": "I am continuing to receive medical treatment for my workplace injury from:",
                    "provider_type": "Physiotherapist",
                    "last_treatment_date": "2023-04-05",
                    "last_provider": "Lisa Johnson, PT",
                    "next_treatment_date": "2023-04-19",
                    "next_provider": "Lisa Johnson, PT",
                    "treatment_frequency": "twice per week",
                    "medication_status": "I am taking medication for my workplace injury:",
                    "medication": "Naproxen 500mg",
                    "exercise_status": "I am doing home exercises for my workplace injury.",
                    "exercises": "Wrist flexion and extension, grip strengthening, and rotational exercises as prescribed."
                },
                "other_info": "I've been practicing the ergonomic techniques that were recommended, which seems to be helping prevent further strain."
            }
        },
        "set2": {
            "medical_expense": {
                "claim_number": "WCB987654321",
                "worker_name": "Jane Doe",
                "worker_app_id": "APP00456",
                "submitted_date": "2023-03-28",
                "prescription_drugs": [
                    ["Cyclobenzaprine", "2023-02-15", "2023-02-16", "Dr. Anderson", "$35.75"],
                    ["Naproxen", "2023-02-25", "2023-02-26", "Dr. Thompson", "$18.99"]
                ],
                "otc_drugs": [
                    ["Aspirin", "2023-02-20", "$6.49", "Rite Aid", "Pain relief"],
                    ["Biofreeze", "2023-02-28", "$15.99", "Target", "Muscle pain"]
                ],
                "medical_supplies": [
                    ["Back Brace", "2023-02-18", "Yes", "Dr. Anderson", "$89.95", "Orthopedic Supplies Inc."],
                    ["Ice Pack", "2023-02-22", "No", "N/A", "$12.99", "Drug Mart"]
                ],
                "parking": [
                    ["Spine & Pain Center, 789 Back St.", "2023-02-16", "$10.00", "No", "N/A"],
                    ["Physical Therapy Group, 555 Rehab Way", "2023-02-22", "$3.00", "Yes", "P1256"]
                ],
                "mileage": [
                    ["2023-02-16", "Spine & Pain Center, 789 Back St.", "Downtown Office, 123 Main St.", "18 km"],
                    ["2023-02-22", "Physical Therapy Group, 555 Rehab Way", "Downtown Office, 123 Main St.", "15 km"]
                ],
                "bus_taxi": [
                    ["2023-02-28", "Home, 456 Oak St.", "Dr. Thompson Office, 333 Medical Pkwy.", "Bus", "$5.25"],
                    ["2023-03-05", "Home, 456 Oak St.", "MRI Center, 222 Diagnostic Dr.", "Taxi", "$32.75"]
                ]
            },
            "worker_progress": {
                "claim_number": "WCB987654321",
                "worker_name": "Jane Doe",
                "worker_app_id": "APP00456",
                "submitted_date": "2023-03-28",
                "return_to_work": {
                    "status": "I have not returned to work",
                    "date": "",
                    "working_status": "",
                    "progress": "",
                    "expected_return": "2023-04-15",
                    "concerns": "I'm concerned that sitting for long periods at my desk will aggravate my back injury.",
                    "employer_contact": "Robert Smith, Supervisor",
                    "contact_date": "2023-03-20"
                },
                "recovery": {
                    "status": "I have not fully recovered from my workplace injury.",
                    "comments": "I continue to experience significant lower back pain, especially after standing or walking for more than 30 minutes.",
                    "pain_level": 6,
                    "treatment_status": "I am continuing to receive medical treatment for my workplace injury from:",
                    "provider_type": "Chiropractor",
                    "last_treatment_date": "2023-03-22",
                    "last_provider": "Dr. Michael Roberts, DC",
                    "next_treatment_date": "2023-03-29",
                    "next_provider": "Dr. Michael Roberts, DC",
                    "treatment_frequency": "once per week",
                    "medication_status": "I am taking medication for my workplace injury:",
                    "medication": "Cyclobenzaprine 10mg, Naproxen 500mg",
                    "exercise_status": "I am doing home exercises for my workplace injury.",
                    "exercises": "Stretching exercises for lower back, core strengthening exercises including modified planks and gentle bridges, as recommended by my physical therapist."
                },
                "other_info": "I've been referred to an orthopedic specialist for a consultation regarding possible additional treatment options. Appointment scheduled for April 5."
            }
        }
    }

@app.route('/')
def index():
    """Render the index page with form options"""
    return render_template('index.pug')

@app.route('/medical-expense')
def medical_expense():
    """Render the Medical & Travel Expense Request form"""
    data_set = request.args.get('data_set', 'set1')
    form_data = load_data()[data_set]['medical_expense']
    return render_template('medical_expense.pug', form_data=form_data)

@app.route('/worker-progress')
def worker_progress():
    """Render the Worker Progress Report form"""
    data_set = request.args.get('data_set', 'set1')
    form_data = load_data()[data_set]['worker_progress']
    return render_template('worker_progress.pug', form_data=form_data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.pug', error='Page not found'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.pug', error='Server error'), 500