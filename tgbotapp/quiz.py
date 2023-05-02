# from . import terms_work
from . import vocab_db
from . import models
from random import choices, sample
from django.conf import settings

quiznum = settings.QUIZ_QUESTIONS_NUMBER


class Quiz:
    def __init__(self, user_id, languagecode):
        # random_terms = sample(terms_work.get_terms_for_quiz(user_id), k=quiznum)
        random_terms = sample(vocab_db.get_terms_for_quiz(user_id, languagecode), k=quiznum)

        self.qna = []
        cnt = 0
        for rt in random_terms:
            qna_item = []
            cnt += 1
            qna_item.append(cnt)
            qna_item = qna_item + rt[1:]
            self.qna.append(qna_item)

            self.user_answers = []
            self.qna_iter = iter(self.qna)  # Объект-итератор для вопросов-ответов

    def next_qna(self):
        """Возвращает очередной вопрос"""
        return next(self.qna_iter)

    def record_user_answer(self, a):
        """Добавляет ответ пользователя в переменную экземпляра (список ответов)"""
        self.user_answers.append(a)

    def get_user_answers(self):
        """Возвращает список ответов пользователя"""
        return self.user_answers

    def check_quiz(self):
        """Проверяет ответы и возвращает список эмодзи"""
        count = 0
        correct_answers = [qna_item[2] for qna_item in self.qna]
        answers_true_false = [i == j for i, j in zip(self.user_answers, correct_answers)]
        for i, j in zip(self.user_answers, correct_answers):
            if i == j:
                count = count + 1
        answers_message = [str(atf).replace('False', '❌ ' + str(j) + '\n\n').replace('True', '✅\n\n')
                           for atf, j in zip(answers_true_false, correct_answers)]
        return answers_message, count
