from collections import Counter
import string
import random


def make_title(line):
    """
    Edits the given line so that it can be used as a title.
    Edit operations include removing unnecessary punctuations and converting the text into title case
    :param line: line of the poem chosen as the title
    :return: title of the poem
    """

    # Removing punctuations at the end of the line
    for char in line[::-1]:
        if char in string.punctuation:
            line = line[:-1]
        else:
            break

    # Removing punctuations at the beginning of the line
    for char in line:
        if char in string.punctuation:
            line = line[1:]
        else:
            break
    return line.title()


def remove_weird_punctuation(poem):
    """
    Removes unnecessary punctuations from given poem.
    :param poem: Poem from which unnecessary punctuations need to be removed
    :return: Poem with no unnecessary punctuations
    """

    swap_dict = {":": " ", "--": "-", '"--"': " ", ",-": ","}

    # Removing incorrect punctuation sequences that usually occur in poems
    for item in swap_dict.items():
        poem = poem.replace(item[0], item[1])

    # Removing punctuations that immediately follow . and !
    temp = poem[0]
    for i, char in enumerate(poem[1:]):
        if (poem[i] == '.' or poem[i] == '!') and char in string.punctuation and poem[i]+char != "!!":
            continue
        temp += char
    poem = temp

    # Correcting words of the format: _word_
    lines = poem.split("\n")
    poem = ""
    for line in lines:
        for word in line.split():
            if word[0] == "_" and word[-1] == "_":
                poem += word[1:-1] + " "
            else:
                poem += word + " "
        poem = poem[:-1] + "\n"
    return poem[:-1]



def generate_title(poem):
    """
    Returns the title as the most repeated line in the poem.
    :param poem: poem whose title has to be generated
    :return: title of the given poem
    """
    lines = poem.split('\n')
    occurrences = Counter(lines)
    occurrences = {k: v for k, v in sorted(occurrences.items(), key=lambda item: item[1], reverse=True)}
    for line in occurrences:
        if len(line) < 7 or len(line) > 35:
            continue
        return make_title(line)

    temp = list(lines)
    lines = []
    for line in temp:
        if len(line) < 7 or len(line) > 35:
            continue
        lines.append(line)
    if lines:
        return make_title(random.choice(lines))
    else:
        return make_title(random.choice(poem.split("\n")))


# poem = """So this is my heart,\nThat here it is, this is my spirit;\nMy right hand, my left hand,\nI see this now;\nMy right hand, I know;\nBut the right hand,\nI know not why."""
# print(generate_title(poem))
# print(remove_weird_punctuation(poem))
