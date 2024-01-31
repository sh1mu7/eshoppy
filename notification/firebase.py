import logging
from typing import Any, Dict
from uuid import uuid4
from django.conf import settings
from django.core.cache import cache

import firebase_admin
from firebase_admin import credentials, auth, firestore, messaging, db

# TESTING SERVER
CREDENTIALS = {
  "type": "service_account",
  "project_id": "eshoppy-20",
  "private_key_id": "b834ead21a813dd7d8b9541a121cb056f1c5f185",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCzj28RhROc3AGE\n/XoTEi2azF2DB0QPhQqaOQrGhSAwihekq+N+giAsUw87/2Nz6RkxwWYBEx6wo/KI\n0mlPkswrgnhGhrJXnD2+9lgglQ8rYHTCsVvJAjJYOAILvgRpcOtxFPO2mYduU1eF\nCRysNyZOuipZDyNSZ1eF5mlH2TtcwVE7FRk3EE3Q+0U/JHjhlWKYNpYwJ9pqBXvr\nXaJNBK6LgWakMipEYCtNv68Gy0WqBLeuO8J9C4AzxnTEGKm4xXWAViz2znhoCyXh\noXwhofUztmhSbRUcYkWNGnm0MoOe3Vr+2TyvBKd54FzOVOhhifThXfj087HvUh/q\nq+0CdgXRAgMBAAECggEACp8ysKR2J2J5BonLaw25ZpMDTx54FLudMnKrDq5OXAC3\nQFWuD0xET0rvN5s2d2NedavdTF/6AfSuLWYrtk+BRhZMO3kkBfxnR1Yhmsp74L2D\n0AaXiY8DNREZxzcLjMSSG5jj3TU80TZwksfvYHKiEKiA8SQXm1F4rczrr8U2dpic\nJ1N+gYo1MZnXemcIBgQrZB57rwRgmppQ5YzdniRJC73YWHdSnYGiuTbLfz/6nbU5\n2+1WvGDQg9tEG/yCoVgm842qW2oIFrvRyCgtsUVaqSTL6YzTDWy2QQGrgrHkovlH\nVi/W4drK8G5/F5uHWSpiTvQOz3DCwAz0tL9ff7DbSQKBgQDsxau8twQ31qCq/kLY\ncp7LMzbtMoot83UTsdiwX5osYSJabtLCqn8vayuJV4IFxk7AZuno5FM6Y9NVMpgU\nmI+UGngLECIBMRiehmWwW6eW6gbedAzkEA2hMmzuS41+4Hrzlzl5T4dMrMHC9FWn\nfvTB99e/E6M8sChq60YM/WWKHQKBgQDCJF4zqAb5kDEsJhqvMFFkrESUMLBJfdgT\nRUzInLJfj/Lbf9jbRQgSSpGij8ozC3C0H6dXYCizjy99sXGHvd5HX2v3gKBqFuqS\nGW8dITMsJY6sGyTMhKA0jnP5MrDWruqLRi13TQWVfXGR+ci8ImZOU6YMN95DS0Qz\n0rihq008RQKBgQDHK4zIpYeF1SS4UkQ2wUx0kDNfGomEF+zfUVZ/HxyYwmjce6cN\nG9D7OYKY+KSmaOesD6YqQ48Dah/G5lVp1d/JbO6YF80TBZK5H0MBNEhouZpnnGWP\nnzVn6PwbBDEVjo2+xPIS6uRcimI/tbsrt676T5sL3+AL1/9X2WvG142HvQKBgE6a\nNuGnOBu2u5HqY4dmgq3F6YYuKFG499Dlj+7xMm7qcyNXoc81Jc1yD4DHws/j49+p\nqTEBJ7l7UXkMbLDOuL4g7i+pDkmluZcpYQlkNbm8AwW/f6imUc61llLgqSRicWeu\nJB5XOtmJjn/Rp+oz60PvLh1oST7prFVnDYW3O3AZAoGBAMjBlJgv5NkrvaZHmPFu\n6pD8+NdOs74s1FJAoNOSWEMa7jV25fDaBOCFbM479J2HTPxCTNB43y3KSXJ+gUe6\nBbvpgpCpqt5LQeOtnFDWyXMHMpw19HsYupN2HvAdEoxxYYKwSlM7ezooB4wbMdpH\ne9MaeGjTGwEs/4tUE9AkihmR\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-sxlwu@eshoppy-20.iam.gserviceaccount.com",
  "client_id": "115465192763868919032",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-sxlwu%40eshoppy-20.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
cred = credentials.Certificate(CREDENTIALS)

firebase_admin.initialize_app(cred)


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


# Testing Real Time Database
class Firebase(Singleton):
    fb = firebase_admin.get_app()


# Production Real Time Database
# class Firebase(Singleton):
#     def __init__(self):
#         print("Initializing Firebase")
#         self.fb = firebase_admin.get_app()  # Get the default Firebase app
#         print("Firebase initialized successfully")


def get_db_ref():
    print("Getting database reference")
    firebase = Firebase()
    ref = db.reference("/")
    print(ref)
    print("Database reference obtained successfully")
    return ref


