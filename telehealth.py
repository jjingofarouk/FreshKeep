import json
import random
import datetime
import time

class Patient:
    def __init__(self, id, name, age, gender):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.medical_history = []

class Doctor:
    def __init__(self, id, name, specialization):
        self.id = id
        self.name = name
        self.specialization = specialization

class Appointment:
    def __init__(self, id, patient_id, doctor_id, date, time):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time

class TeleHealthSystem:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.appointments = {}
        self.load_data()

    def load_data(self):
        try:
            with open('patients.json', 'r') as f:
                self.patients = json.load(f)
            with open('doctors.json', 'r') as f:
                self.doctors = json.load(f)
            with open('appointments.json', 'r') as f:
                self.appointments = json.load(f)
        except FileNotFoundError:
            print("No existing data found. Starting with empty records.")

    def save_data(self):
        with open('patients.json', 'w') as f:
            json.dump(self.patients, f)
        with open('doctors.json', 'w') as f:
            json.dump(self.doctors, f)
        with open('appointments.json', 'w') as f:
            json.dump(self.appointments, f)

    def register_patient(self):
        name = input("Enter patient name: ")
        age = int(input("Enter patient age: "))
        gender = input("Enter patient gender (M/F/O): ")
        id = f"P{len(self.patients) + 1:03d}"
        patient = Patient(id, name, age, gender)
        self.patients[id] = patient.__dict__
        print(f"Patient registered successfully. ID: {id}")
        self.save_data()

    def add_doctor(self):
        name = input("Enter doctor name: ")
        specialization = input("Enter doctor specialization: ")
        id = f"D{len(self.doctors) + 1:03d}"
        doctor = Doctor(id, name, specialization)
        self.doctors[id] = doctor.__dict__
        print(f"Doctor added successfully. ID: {id}")
        self.save_data()

    def schedule_appointment(self):
        patient_id = input("Enter patient ID: ")
        doctor_id = input("Enter doctor ID: ")
        date = input("Enter appointment date (YYYY-MM-DD): ")
        time = input("Enter appointment time (HH:MM): ")
        id = f"A{len(self.appointments) + 1:03d}"
        appointment = Appointment(id, patient_id, doctor_id, date, time)
        self.appointments[id] = appointment.__dict__
        print(f"Appointment scheduled successfully. ID: {id}")
        self.save_data()

    def start_consultation(self):
        appointment_id = input("Enter appointment ID: ")
        if appointment_id in self.appointments:
            appointment = self.appointments[appointment_id]
            patient = self.patients[appointment['patient_id']]
            doctor = self.doctors[appointment['doctor_id']]
            print(f"\nStarting consultation for:")
            print(f"Patient: {patient['name']}")
            print(f"Doctor: {doctor['name']} ({doctor['specialization']})")
            print(f"Date: {appointment['date']}, Time: {appointment['time']}")
            print("\nSimulating video call...")
            time.sleep(2)
            print("Video call connected.")
            self.conduct_consultation(patient, doctor)
        else:
            print("Appointment not found.")

    def conduct_consultation(self, patient, doctor):
        print("\n--- Consultation in progress ---")
        symptoms = input("Patient, please describe your symptoms: ")
        print(f"\nDr. {doctor['name']} is analyzing the symptoms...")
        time.sleep(2)
        diagnosis = self.simple_diagnosis(symptoms)
        print(f"\nDr. {doctor['name']}'s diagnosis: {diagnosis}")
        prescription = input("Doctor, please provide prescription: ")
        self.update_medical_history(patient['id'], diagnosis, prescription)
        print("\nConsultation completed. Medical history updated.")

    def simple_diagnosis(self, symptoms):
        common_diagnoses = ["Common Cold", "Allergies", "Stress", "Fatigue", "Mild Flu"]
        return random.choice(common_diagnoses)

    def update_medical_history(self, patient_id, diagnosis, prescription):
        if patient_id in self.patients:
            entry = {
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "diagnosis": diagnosis,
                "prescription": prescription
            }
            if 'medical_history' not in self.patients[patient_id]:
                self.patients[patient_id]['medical_history'] = []
            self.patients[patient_id]['medical_history'].append(entry)
            self.save_data()

    def view_medical_history(self):
        patient_id = input("Enter patient ID: ")
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            print(f"\nMedical History for {patient['name']}:")
            if 'medical_history' in patient:
                for entry in patient['medical_history']:
                    print(f"Date: {entry['date']}")
                    print(f"Diagnosis: {entry['diagnosis']}")
                    print(f"Prescription: {entry['prescription']}")
                    print("---")
            else:
                print("No medical history available.")
        else:
            print("Patient not found.")

    def run(self):
        while True:
            print("\n--- TeleHealth Consultation System ---")
            print("1. Register Patient")
            print("2. Add Doctor")
            print("3. Schedule Appointment")
            print("4. Start Consultation")
            print("5. View Medical History")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.register_patient()
            elif choice == '2':
                self.add_doctor()
            elif choice == '3':
                self.schedule_appointment()
            elif choice == '4':
                self.start_consultation()
            elif choice == '5':
                self.view_medical_history()
            elif choice == '6':
                print("Thank you for using the TeleHealth Consultation System.")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    system = TeleHealthSystem()
    system.run()
