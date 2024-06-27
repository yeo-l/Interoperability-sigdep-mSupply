from zato.server.service import Service
import requests
from requests.auth import HTTPBasicAuth
import json

class TransferPatients(Service):
    name = 'opencr.transfer.patients'

    def handle(self):
        connection = self.out.rest['opencr_api'].conn

        # Récupération des paramètres d'entrée

        # opencr_url = self.request.input['opencr_url']
        # opencr_username = self.request.input['opencr_username']
        # opencr_password = self.request.input['opencr_password']
        openmrs_url = self.request.input['openmrs_url']
        openmrs_username = self.request.input['openmrs_username']
        openmrs_password = self.request.input['openmrs_password']

        # Récupération des patients depuis OpenCR
        patients = connection.get_patients_from_opencr(self.cid)
        if patients:
            for patient in patients:
                self.send_patient_to_openmrs(openmrs_url, openmrs_username, openmrs_password, patient)
        else:
            self.logger.info("Aucun patient trouvé dans OpenCR")

    def get_patients_from_opencr(self, url, username, password):
        response = requests.get(f'{url}/api/fhir/Patient', auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(f'Échec de la récupération des patients depuis OpenCR: {response.status_code}')
            return None

    def send_patient_to_openmrs(self, url, username, password, patient):
        openmrs_patient = self.transform_patient_to_openmrs(patient)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{url}/ws/rest/v1/patient', auth=HTTPBasicAuth(username, password), headers=headers, data=json.dumps(openmrs_patient))
        if response.status_code in (200, 201):
            self.logger.info(f'Succès: Patient envoyé à OpenMRS (ID: {openmrs_patient.get("id")})')
        else:
            self.logger.error(f'Échec de l\'envoi du patient à OpenMRS: {response.status_code}')

    def transform_patient_to_openmrs(self, patient):
        # Transformation de la structure de données du patient d'OpenCR à OpenMRS
        openmrs_patient = {
            'person': {
                'names': [{
                    'givenName': patient['firstName'],
                    'familyName': patient['lastName']
                }],
                'gender': patient['gender'],
                'birthdate': patient['birthDate']
            },
            'identifiers': [{
                'identifier': patient['identifier'],
                'identifierType': 'e2b966d0-1d5f-11e0-b929-000c29ad1d07',  # Exemple d'UUID pour le type d'identifiant
                'location': '8d6c993e-c2cc-11de-8d13-0010c6dffd0f',  # Exemple d'UUID pour la localisation
                'preferred': True
            }]
        }
        return openmrs_patient
