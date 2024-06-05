def compare_texts(text1: str, text2: str):


    matches = 0

    for i in range(min(len(text1), len(text2))):
        if text1[i] == text2[i]:
            matches += 1

    return matches / min(len(text1), len(text2))

