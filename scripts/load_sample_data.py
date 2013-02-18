
from lottery.models import (Interview, Question,
                        Photo, Audio, Quote)

questions_en = [
    "How many NY Lotto tickets do you sell each week?",
    "What kinds of numbers do people pick?",
    "Do you play the lottery? Why or why not?",
    "Are there lottery regulars who buy tickets here?",
    "How many tickets do people usually buy?",
    "How much of the money (or what percentage of the money) that the store brings in for lottery tickets does the store get to keep?",
            ]

questions_es = [
    "Cuanto billetes vende usted cada semana?",
    "Que tipos de numeros elige la genta?",
    "Juega usted la loteria? Por que o por que no?",
    "Hay gente que suele venir aqui para jugar?",
    "Cuanto billetes suele comprar la gente?",
    "Que porcentaje de las ventas sobra para la tienda?"
            ]


def load_questions():
    for i, en in enumerate(questions_en):
        q = Question()
        q.text_en = en
        q.text_es = questions_es[i]
        q.save()


load_questions()






