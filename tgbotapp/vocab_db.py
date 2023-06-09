from .models import Users, Armenian, English
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


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
    try:
        term = Users.objects.get(userid="user_id")
    except ObjectDoesNotExist:
        user = Users(userid=user_id, numtestsen=0, avgresen=0.0, numtestsam=0, avgresam=0.0)
        user.save()


def get_stats(user_id):
    terms = []
    for i, item in enumerate(Users.objects.filter(userid=user_id)):
        terms.append([i + 1, item.numtestsen, item.avgresen, item.numtestsam, item.avgresam])
    return terms


def update_stats(user_id, newres, languagecode):
    term = Users.objects.get(userid=user_id)
    tmp1 = term.numtestsen
    tmp2 = term.avgresen
    tmp3 = term.numtestsam
    tmp4 = term.avgresam
    if languagecode == settings.ENGLISH:
        term.numtestsen = tmp1+1
        term.avgresen = 100*(((tmp2 * tmp1) + newres) / (tmp1 + 1)) / settings.QUIZ_QUESTIONS_NUMBER
    elif languagecode == settings.ARMENIAN:
        term.numtestsam = tmp3 + 1
        term.avgresam = 100*(((tmp4 * tmp3) + newres) / (tmp3 + 1)) / settings.QUIZ_QUESTIONS_NUMBER
    term.save()
