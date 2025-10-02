# app/vo/asresult_question_vo.py
class AsresultQuestionVO:
    def __init__(self, question, user_answer, correct_answer, options):
        self.questionId = question.id
        self.questionTitle = question.content
        self.orderIndex = question.order_index
        self.userAnswer = user_answer
        self.correctAnswer = correct_answer
        self.isCorrect = set(user_answer) == set(correct_answer)
        self.options = [
            {
                "value": opt.value,
                "label": opt.label,
                "isCorrect": opt.is_correct
            }
            for opt in options
        ]

    def to_dict(self):
        return self.__dict__
