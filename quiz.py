# 개별 퀴즈
class Quiz:
    def __init__(self, question, choices, answer, hint="힌트가 없습니다."):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def print_quiz(self):
        print(self.question)
        for choice in self.choices:
            print(choice)

    def checkAnswer(self,userAnswer):
         return userAnswer==self.answer

    