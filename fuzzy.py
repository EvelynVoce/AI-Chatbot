from simpful import FuzzySystem, FuzzySet, Triangular_MF, Trapezoidal_MF, LinguisticVariable


def func():
    fuzzy_set1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=5), term="poor")
    fuzzy_set2 = FuzzySet(function=Triangular_MF(a=0, b=5, c=10), term="average")
    fuzzy_set3 = FuzzySet(function=Triangular_MF(a=5, b=10, c=10), term="good")
    return [fuzzy_set1, fuzzy_set2, fuzzy_set3]


def fuzzy_logic(writing_score: int, acting_score: int, impact_score: int):
    fs = FuzzySystem(show_banner=False)

    # Define fuzzy sets and linguistic variables
    fs.add_linguistic_variable("Writing", LinguisticVariable(func(), universe_of_discourse=[0, 10]))
    fs.add_linguistic_variable("Acting", LinguisticVariable(func(), universe_of_discourse=[0, 10]))
    fs.add_linguistic_variable("Impact", LinguisticVariable(func(), universe_of_discourse=[0, 10]))

    # Define output fuzzy sets and linguistic variable
    q_1 = FuzzySet(function=Triangular_MF(a=0, b=0, c=2.5), term="poor")
    q_2 = FuzzySet(function=Triangular_MF(a=0, b=2.5, c=5), term="average")
    q_3 = FuzzySet(function=Triangular_MF(a=2.5, b=5, c=7.5), term="good")
    q_4 = FuzzySet(function=Trapezoidal_MF(a=5, b=7.5, c=10, d=10), term="amazing")
    fs.add_linguistic_variable("Quality", LinguisticVariable([q_1, q_2, q_3, q_4], universe_of_discourse=[0, 10]))

    R1 = "IF (Writing IS poor) THEN (Quality IS poor)"
    R2 = "IF (Writing IS average) AND (Acting IS average) THEN (Quality IS average)"
    R3 = "IF (Writing IS average) AND (Acting IS good) THEN (Quality IS average)"
    R4 = "IF (Writing IS good) AND (Acting IS average) THEN (Quality IS average)"
    R5 = "IF (Writing IS good) AND (Acting IS good) THEN (Quality IS good)"
    R6 = "IF (Writing IS good) AND (Acting IS good) AND (Impact IS good) THEN (Quality IS amazing)"
    fs.add_rules([R1, R2, R3, R4, R5, R6])

    # Set antecedents values
    fs.set_variable("Writing", writing_score)
    fs.set_variable("Acting", acting_score)
    fs.set_variable("Impact", impact_score)

    # Perform Mamdani inference and print output
    quality_score = fs.Mamdani_inference(["Quality"])
    return int(quality_score["Quality"])
