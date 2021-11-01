#!/usr/bin/python3


def load_text(file):
    """
    load_text returns content of a file as list of lines.
    :param file: a path to a .txt file
    :return: list of lines from the file
    """
    with open(file) as subs:
        text = subs.readlines()
        return text


def insert_text_into_subtitles(originalSubs, originalText, translatedText):
    """
    insert_text_into_subtitles takes a translated Text and creates a list of lines representing a .srt file with timings according to the original language subs file.
    :param originalSubs: .srt file containing the original subs
    :param originalText: .txt file containing the original text (one string, no subs formatting)
    :param translatedText: .txt file with translation of the original text (one string)
    :return: list of lines representing a .srt file with the translated text
    """

    # calculate length ratio between English and Czech text
    textLengthRatio = len(translatedText) / len(originalText)

    desirableLineEnds = ["\n", " "]
    translatedSubs = list()
    cutStartPosition = 0  # to save a position where last cutting of the translated text ended
    lengthChecker = 0 # to save how many positions are the subtitles ahead of what they should be if cuts were made in the middle of a word

    for i, line in enumerate(originalSubs):
        if (i - 2) % 4 != 0:  # copy the subtitle number, timing, and empty line from the original file
            translatedSubs.append(line)

        if (i - 2) % 4 == 0:  # insert translated text
            desiredTextLength = int(len(line) * textLengthRatio)
            cutEndPosition = cutStartPosition + desiredTextLength

            # make sure you are cutting string in a desirable place
            #TODO figure out how to set up lengthChecker properly
            while lengthChecker > 385 and translatedText[cutEndPosition] not in desirableLineEnds:
                cutEndPosition -= 1
                lengthChecker -= 1

            while translatedText[cutEndPosition] not in desirableLineEnds:
                cutEndPosition += 1
                lengthChecker += 1

            cutTranslated = translatedText[cutStartPosition:cutEndPosition].strip()
            textToBeInserted = cutTranslated + "\n"
            translatedSubs.append(textToBeInserted)
            cutStartPosition = cutEndPosition

    print(lengthChecker)
    return translatedSubs


if __name__ == "__main__":

    # load data from text files
    subsEng = load_text("subs_eng.srt")
    textEng = load_text("text_eng.txt")[0]
    textCze = load_text("text_cze.txt")[0]

    with open("subs_cze_machine.srt", "w", encoding="UTF-8") as file:
        file.writelines(insert_text_into_subtitles(subsEng, textEng, textCze))
