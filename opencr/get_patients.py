# -*- coding: utf-8 -*-
# zato: ide-deploy=True

from zato.server.service import Service


class TransferPatients(Service):
    name = 'opencr.get.patients'

    def handle(self):
        connection = 'FHIR.Opencr'

        with self.out.hl7.fhir[connection].conn.client() as client:

            patients = client.resources('Patient')
            self.logger.debug('Patients: {}'.format(patients))
            result = patients

            for elem in result:
                self.logger.info('Received -> %s', elem['name'])


