import time
import requests


class VerificationCodeService:
    # def __init__(self, session_hash, token):
    #     self._session_hash = session_hash
    #     self._token = token

    def get(self):
        return input('Enter verification code: ')
        # verification_codes = []
        # while len(verification_codes) == 0:
        #     time.sleep(0.5)
        #     verification_codes = self._get_verification_code()
        # return verification_codes[0]['verification_code']

    # def _get_verification_code(self):
    #     response = requests.get('http://127.0.0.1:8000/sniper/session/' + str(self._session_hash) + '/verify/', 
    #         headers={"Authorization": "Bearer " + str(self._token)}
    #     )
    #     return response.json()
