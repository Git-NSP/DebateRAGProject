from judge import JudgeAgent

history = [

    {
        "speaker": "Pro",
        "argument": "Spring Boot greatly simplifies Java backend development."
    },

    {
        "speaker": "Con",
        "argument": "Django offers faster development because Python is more concise."
    },

    {
        "speaker": "Pro",
        "argument": "Spring Boot has stronger enterprise integration."
    }

]

judge = JudgeAgent()

result = judge.judge_debate(

    topic="Spring Boot is better than Django.",

    debate_history=history

)

print(result)

