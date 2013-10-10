from datetime import timedelta
from decimal import Decimal
from .models import UserQuestionnaire, Questionnaire


def compute_score(user_questionnaire):
    """
    Computes the CDAI score.
    :param UserQuestionnaire user_questionnaire: A Questionnaire object.
    :return: An integer representing the score for the object.
    """
    hematocrit_base = 47 if user_questionnaire.user_profile.gender == 'Male' else 42
    standard_weight = 150.0
    score = 0
    questions = []
    current_question = UserQuestionnaire.objects.get(user_profile=user_questionnaire.user_profile,
                                                     day=user_questionnaire.day).questionnaire
    for q in UserQuestionnaire.objects.filter(user_profile=user_questionnaire.user_profile,
                                              day__gt=user_questionnaire.day-timedelta(days=7),
                                              day__lte=user_questionnaire.day):
        questions.append(Questionnaire.objects.get(id=q.questionnaire.id))
    for q in questions:
        score += (q.liquid_stool * 2)
        score += (q.abdominal_pain * 5)
        score += (q.general_well_being * 7)

    score += (current_question.number_of_complications * 20)
    score += (current_question.taking_lomatil_or_opiates * 30)
    score += (current_question.presence_of_abdominal_mass * 10)
    score += ((hematocrit_base - current_question.hematocrit) * 6)
    # use the decimal library for precision. Use quantize to apply standard rounding rules.
    weight_score = Decimal(100*(1-Decimal(current_question.current_weight)/Decimal(standard_weight)))
    weight_score = weight_score.quantize(Decimal('1'))
    if weight_score < -9:
        score += -10
    else:
        score += weight_score
    return score

