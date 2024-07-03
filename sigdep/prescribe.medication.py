# -*- coding: utf-8 -*-
# zato: ide-deploy=True

from zato.server.service import Service


class PrescribeMedication(Service):
    name = 'prescribe.medication'

    def handle(self, patient_id, medication_code, medication_display):
        connection = 'FHIR.Opencr'

        with self.out.hl7.fhir[connection].conn.client() as client:

            patients = client.resources('Patient')

            if patients:
                patient = patients.search(patient_id)

        if patient:

                   # await client.resources('MedicationRequest') \
                   #     .include('MedicationRequest', 'patient', target_resource_type='Patient') \
                   #     .fetch_raw()
                   # await client.resources('MedicationDispense') \
                   #     .include('MedicationRequest', 'prescriber', recursive=True) \
                   #     .fetch_raw()


            medication_data = {
                "resourceType": "MedicationRequest",
                "status": "active",
                "intent": "order",
                "medicationCodeableConcept": {

                    "text": medication_display
                },
                "subject": {
                    "reference": f"Patient/{patient_id}"
                },
            }
            return medication_data

    def send_prescription_to_fhir(self, prescription):
        connect = 'FHIR.Sharing'
        response = connect.post('/MedicationRequest'),
        if response.status_code in (200, 201):
            self.logger.info(f'Succès: Prescription envoyée à FHIR (ID: {prescription.get("id")})')
        else:
            self.logger.error(
                f'Échec de l\'envoi de la prescription à FHIR: {response.status_code} {response.text}')
