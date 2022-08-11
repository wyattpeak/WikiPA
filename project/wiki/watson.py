from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, KeywordsOptions


def get_keywords(txt):
    if txt.strip() == '':
        return []

    authenticator = IAMAuthenticator(
        # 'MrQXm9ZP3J3gv6jb_Gj5sI3SRlLPtE65KzEQKxWAK2Fp')
        '1B6cEVSdUKtLA6lFULKu-uxr98znn9gKKUPk29txrtmv')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url('https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/2318ee97-e67f-4d23-a9a0-a23f14ae636f')

    response = natural_language_understanding.analyze(
        text=txt,
        features=Features(keywords=KeywordsOptions(limit=50))).get_result()

    return response['keywords']
