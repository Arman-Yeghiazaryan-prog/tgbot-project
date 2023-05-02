from .models import Users, Armenian, English
from django.conf import settings
from django.db.models import Q


def get_terms_for_table(languagecode):
    terms = []
    if languagecode == settings.ENGLISH:
        for i, item in enumerate(English.objects.all()):
            terms.append([i+1, item.word, item.translation])
        return terms
    elif languagecode == settings.ARMENIAN:
        for i, item in enumerate(Armenian.objects.all()):
            terms.append([i+1, item.word, item.translation])
        return terms


def get_terms_for_quiz(user_id, languagecode):
    terms = []
    if languagecode == settings.ENGLISH:
        for i, item in enumerate(English.objects.filter(Q(source='admin') | Q(source=user_id))):
            terms.append([i + 1, item.word, item.translation])
        return terms
    elif languagecode == settings.ARMENIAN:
        for i, item in enumerate(Armenian.objects.filter(Q(source='admin') | Q(source=user_id))):
            terms.append([i + 1, item.word, item.translation])
        return terms


def write_term(new_term, new_definition, user_id, languagecode):
    if languagecode == settings.ENGLISH:
        term = English(word=new_term, translation=new_definition, source=user_id)
    elif languagecode == settings.ARMENIAN:
        term = Armenian(word=new_term, translation=new_definition, source=user_id)
    term.save()


def write_user(user_id):
    user = Users(userid=user_id, numtestsen=0, avgresen=0.0, numtestsam=0, avgresam=0.0)
    user.save()


def get_stats(user_id):
    terms = []
    # for i, item in enumerate(Users.objects.filter(userid=user_id)):
    for i, item in enumerate(Users.objects.filter(userid='admin')):
        terms.append([i + 1, item.numtestsen, item.avgresen, item.numtestsam, item.avgresam])
    return terms


def update_stats(user_id, newres, languagecode):
    terms = []
    # for i, item in enumerate(Users.objects.filter(userid=user_id)):
    for i, item in enumerate(Users.objects.filter(userid='admin')):
        terms.append([i + 1, item.numtestsen, item.avgresen, item.numtestsam, item.avgresam])
    oldterm = terms[0]
    if languagecode == settings.ENGLISH:
        newterm = Users(userid=user_id, numtestsen=oldterm[1]+1,
                        avgresen=((oldterm[2] * oldterm[1]) + newres) / (oldterm[1] + 1),
                        numtestsam=oldterm[3], avgresam=oldterm[4])
    elif languagecode == settings.ARMENIAN:
        newterm = Users(userid=user_id, numtestsen=oldterm[1], avgresen=oldterm[2],
                        numtestsam=oldterm[3]+1,
                        avgresam=((oldterm[2] * oldterm[1]) + newres) / (oldterm[1] + 1))
    newterm.save()
