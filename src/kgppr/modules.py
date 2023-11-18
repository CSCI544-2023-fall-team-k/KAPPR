import dspy

class GenerateAnswer(dspy.Signature):
    """Answer questions with short factoid answers."""

    question = dspy.InputField()
    context = dspy.InputField(desc="facts that might be relevant to answer the question")
    answer = dspy.OutputField(desc="often between 1 and 5 words")

class GenerateFirstSubQuery(dspy.Signature):
    """Want to answer for a complex question that might need procedural reasoning. 
    Given the complex question, generate an initial question that is helpful to answer the complex question."""

    question = dspy.InputField(desc="complex question that might need procedural reasoning to answer.")
    subquery = dspy.OutputField(desc="an initial question to solve the complex question.")
    
class GenerateNextSubQuery(dspy.Signature):
    """Given the complex question, and the previous question-answer pairs, generate a next question that is helpful to answer the complex question. 
    The next question must not overlap the previous questions. If the complex question can be answered only using the previous question-answer pairs, say "NONE"."""

    question = dspy.InputField(desc="complex question that might need procedural reasoning to answer.")
    previous_qa = dspy.InputField(desc="the previous question and answer pairs")
    subquery = dspy.OutputField(desc="next simple question to solve the complex question.")
    
class SolveQuestion(dspy.Signature):
    """Answer the complex question. You are given some question and answer pairs that might be useful when answering to the complex question. If a question and answer pair is not useful, ignore it."""

    question = dspy.InputField(desc="complex question that might need procedural reasoning to answer.")
    previous_qa = dspy.InputField(desc="the question and answer pairs as context")
    answer = dspy.OutputField(desc="often between 1 to 5 words.")

class EvaluateAnswer(dspy.Signature):
    """Given a list of target phrases and a predicted phrase, say "True" if the predicted phrase is semantically identical to one of the target phrases, otherwise say "False".
    Say also "True" if the predicted one is a hypernym or hyponym of targets."""

    target = dspy.InputField(desc="list of target phrases")
    predicted = dspy.InputField(desc="predicted phrase")
    answer = dspy.OutputField(desc="True or False")