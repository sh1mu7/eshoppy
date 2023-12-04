import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# PRODUCTION SERVER
# CREDENTIALS = {
#     "type": "service_account",
#     "project_id": "dogrocer-398bc",
#     "private_key_id": "11beae747ca386f98d026041fd1b7c0b110b28b3",
#     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCzaf34JSO9LPR4\nZPyE8FZeVclfisWkwX/3cjlMSOmM5sDvbnxJVUUL8hJ8OLcvi1DlOuianR1t7mQO\nkMZIutf1oT6cZ+sQCizEikvpxoHYDeVtkmmye/AT9O28tV2D3acY+xmi8nFhemcI\n0r29JGyGwaqDekON3S+lgBQ8IQ5lDk78olJGXK54BrFcDBvKu/3sWm+DAKWS4gcE\no4pqZvIdbipqeP8iCkFYHl5kzNwNHLcQ+7iW6E2NUTi/4ku7nxOkv9Rg8gDpMha+\nzCc4FNrIvBlDZe+e4wYjZBsoU2xQeO57gTuVkSyNo03EWagk8m+QT+rVsFFPdPRu\nql7RRS47AgMBAAECggEALydd1QCp3nf4vsXH6oaiJIQGe4JlBLLIl7fhIFAPdfVV\n4vfWWY28KnIScqyTVL8YYU70wGIn0HM1v/BD9OyKgufApWnYiWwrLPKuFgCSsr6g\nPIadGghh5lTawNyn+dbhKnsgV0fCDd0WRGbi8Fmo3lf7ITgalif6dFRvvQfxGRTS\n/A41YgAXyQvWtLXbFOc2Y3r+N0BlSTmo9Bhv2o+RA25pSo55QaOukMFdui4m5olZ\n1pJFWopQuLmlvqYubn1FkXrPZErkd9YAtO4hSFicKVnb4k91chJsCu147s4FHeYl\n9MyTJc9X1p5JQVhvR7PF2Bp2Q+e+vmiNJhw0EF/GJQKBgQDrlzCYHJkEobL3/h3M\n6VYMzknJ9Qi3mqHEx3TzSsAssbYWxUe2d0SiNBxsyQdEByS1OyS5X5ay5XKgtOIV\nI0O53U479UlmkUAhZLKnsDqabVGcTKrSbgFeYh9wsLntyGIJqGQ6q0Ffbgs9tLLR\nudn1Jes4Koqjfc+bMgnLGGr05wKBgQDC9PJdDbgS5gUidZOH397UWwSihNsntX0+\nm9X1UKlyATcS7MgPTaqbHSRhbRrw2p5QRCIZOI6pu7K2coUEMZYyt3BGR/gqau63\nvYC1PomElY7WpFPtTahG1qe7+oReSdsiOP7gwwmeO45YMc96M5zpBkg3PpViOciM\nt+Jz5Iz9jQKBgHY3ucS6pPY0BdB3jZCjjfCDG3fiI2uuhnpt8/uZiPFkg5DNkfy3\nwJL8Pz8/aQvz4bGnafgzRTWj+W83FTOyLGv55yYjIZ/8Rwf6tcN7pQyUypz5w8Yw\nOTOZXVl49POi178s5o6iHP28BJwELq8a6YogavYWMtdzbFfeNhfZuuIFAoGAHkJe\ni8rhUy2YhmyxZVl+AH/QDFmKmnM06U7OurC2XBeMMMfHlXh8jm7LgsOodtG32MV6\ndWet3PJhHqhPtQLtSRnnt0DcZ9kJDEPBgmAegBGmhfIjhKWVBMm0ZxzPBsN326v1\nA3XCPGkKAu5YQaNZK2HqO4jfLsvBMPYpk8tZhtECgYEAwCQ+hpQ2enhFkNOoY8qn\n0y9p5WdQ/lJZ6SP3FtQJVuLcxRVyPgnWdURGtBBq3xIYoZ+Jich0c6YtcQEf/7Go\nJXxaK/DJTUvZc7ShOp0CGiY291UTz5jQ8HbNbHzSxQRSzq9I6gAJbiNrfKk5zPrZ\nrW++YH2xGypFPlVDvPS5qHo=\n-----END PRIVATE KEY-----\n",
#     "client_email": "firebase-adminsdk-hohtk@dogrocer-398bc.iam.gserviceaccount.com",
#     "client_id": "106476377008346797872",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-hohtk%40dogrocer-398bc.iam.gserviceaccount.com"
# }

# TESTING SERVER
CREDENTIALS = {
    "type": "service_account",
    "project_id": "dogrocer-test",
    "private_key_id": "71fec280b129074a5447637be0c97038db1f12b9",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCND68JRGf5Pq3k\nFaCeCSPNNJg+j6m6Qic16wqDxeV1IfRXymJMoOOzReusCYdQO5VFnWxtPNXtSWwE\nYaVBaVVQ1yVHNEI3BVrld7BlmEY6S/cHU60R+OA6XJkazi6tELlEsXURoorUzSzA\nPPUG99pgV1FsBGHnF1bj1RAyV8RsocEQzBMNx0V5O38mJg0dknTOj6JyO87wo1MH\nOiFqO2dX8xPP29458SsICppXS+3XZX+sRJ8t6Opw2ufz57G9wf8CkewxOxsQIDy5\nXleznYpwsy77laBuczEPgqHCaWNXYy6h+ddjWeq/GA8QpWNtV/FUno6sGRffqj19\nMNB5bbUlAgMBAAECggEAFQ1zLSnlbqB5KWJE73Ejw7uGwUeFqEO5QGXM0u/VGA8y\nPWv6Eb+tXBMiYjGl3UaXN6WQChmbP+fGVD0Sgdmrnv4NFTxqaXXGJBsh23fHe2nc\n+130pYsERBGP1B1TgAbP772gYDpnB+17MVGnrBuPnvNJNprM1cV49VXWLf1FVoTw\n48IK1VfgKAZyAWDbAIHbUBZcSraLus9SQAXlNOXqURMKAxmt81scwN2MaQMlHMid\nhz9IMFZXmAzi6Ue3xWabv5u4YJDrAhnl8UjIl8zaWy4xkAB2cbXpyTTGKS3T03Au\n9Xue+UlNmIYw3JkNBMN7qQh/yQ/F0vKpFtUraVWHXQKBgQDCZSsors2TwiiuceWp\nVYsFc2NCNxC1bGmWY+fKka9FYBqWwjevZ2ykHuLJhoIvlEo78d9OQsyVY6oLuflx\n2PJy3gml2zCx01IUcs9hM143+j1mN12yp4ebTxQAcPiHLuXyK8zq4XyIUgW+4EfH\n5kxiKN63KkJp0QxZ/KZVtO3YNwKBgQC5w6hH52XNdhiL34uuGo6LtAOCdrd0dYPO\nMPDj83NDNVflt1s8pA8BqeMT4f7YaTjHnlEgCW53K80JZZjlwA27JOLwZuomkurk\n9BFVtCnNvNNOy1ZAetNPNjkYq0syVuuSbFG2Hy9B3wJPsnmSDsQlz26u+fV9HtuN\nP5/otT33gwKBgDGahSfNaxHAIodY8uSBuoa6ieJ0kKPqtQq2FYiAIjxOqJo9lt4A\nQx2h7/bChufDLCodrwCWVQPtuY9idj9Rv5QGCmozAzrtFG25WieQZwNbrF0v1Y3n\n59d+lzkBmrlMA0sHWDO7M/7JB0RMkKR2pJkLmsEcXHQJ7t/rczo9f8+DAoGBAJx7\nKrhXPjRTNN4ukxU4HbelDgfKRUN+8mawZ1s96mxE9SP2zo5IjLOUDkrjZq+aA1B0\nFlZsW3dbmD5ALQnsPCTXL6vepYOU4vW2exu8xjIey8lmE+QBExt4y6PyN0fSXGJd\niH9nyYEtgF7uMuZMNgK7t7sBqD+bzMoxPFzkv6xNAoGAB5HqNNjYUDDk5fd8ZSpN\nbFT1elio/KjmwleIksQgGCkxukCXXFtP0SkrI++d9GKyFiat9tFj5e10kdN0bxDR\nDK/zmgdnPSi6u3M39YZy61RRE+xkvot0MiG+1sxpZU1yAEK9cJ9U+R9wLOuHB272\neTWum/M4S1vPFPU9v3Cw9v0=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-h71gi@dogrocer-test.iam.gserviceaccount.com",
    "client_id": "105672577119766998907",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-h71gi%40dogrocer-test.iam.gserviceaccount.com"
}
cred = credentials.Certificate(CREDENTIALS)


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


# Testing Real Time Database
class Firebase(Singleton):
    fb = firebase_admin.initialize_app(cred, {
        "databaseURL": "https://dogrocer-test-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })


# Production Real Time Database
# class Firebase(Singleton):
#     fb = firebase_admin.initialize_app(cred, {
#         "databaseURL": "https://dogrocer-398bc-default-rtdb.firebaseio.com/"
#     })

def get_db_ref():
    firebase = Firebase()
    return db.reference("/")
