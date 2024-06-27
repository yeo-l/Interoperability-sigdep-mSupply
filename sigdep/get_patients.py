from zato.server.service import Service
import requests
from requests.auth import HTTPBasicAuth

class GetPatients(Service):
    name = 'sigdep.get.patients'

    class SimpleIO:
        input_required = ('openmrs_url', 'openmrs_username', 'openmrs_password')

    def handle(self):
        # Récupération des paramètres d'entrée
        openmrs_url = self.request.input['openmrs_url']
        openmrs_username = self.request.input['openmrs_username']
        openmrs_password = self.request.input['openmrs_password']

        # Récupération des patients depuis OpenMRS
        patients = self.get_patients_from_openmrs(openmrs_url, openmrs_username, openmrs_password)
        if patients:
            self.response.payload = patients
        else:
            self.response.payload = {'error': 'Aucun patient trouvé'}

    def get_patients_from_openmrs(self, url, username, password):
        response = requests.get(f'{url}/ws/rest/v1/patient', auth=HTTPBasicAuth(username, password))
        if response.status_code == 200:
            print(f'liste des patients : {response.json()}')
            return response.json()['results']
        else:
            self.logger.error(f'Échec de la récupération des patients depuis OpenMRS: {response.status_code}')
            return None