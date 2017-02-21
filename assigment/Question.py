class Question:

    questionText = "Er dette et sporsmal?"
    answerList = [("ja", True), ("nei",False), ("kanskje",True),("kanskje",True)]

    def getQuestion(self):
        return self.questionText

    def getAnswerList(self):
        return self.answerList

