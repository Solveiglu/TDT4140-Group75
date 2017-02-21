class AnswerChecker:
    def checkAnswer(self, correctAnswer, userAnswer):
        resultList = []
        print(userAnswer, correctAnswer)
        for i in range(len(correctAnswer)):
            if correctAnswer[i][1] == userAnswer[i]:
                resultList.append(True)
            else:
                resultList.append(False)

        return resultList

    #TODO return result of each answer