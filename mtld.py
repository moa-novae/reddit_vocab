import spacy
nlp = spacy.load('en_core_web_sm')
# test str
text = ("""The state was named for the Colorado River, which early Spanish """
        """explorers named the Río Colorado ("Red River") for the ruddy  """
        """silt the river carried from the mountains. The Territory of """
        """Colorado was organized on February 28, 1861, and on August """
        """1, 1876, U.S. President Ulysses S. Grant signed Proclamation """
        """230 admitting Colorado to the Union as the 38th state. Colorado """
        """is nicknamed the "Centennial State" because it became a state """
        """one century after the signing of the United States Declaration """
        """of Independence. Colorado is bordered by Wyoming to the north, """
        """Nebraska to the northeast, Kansas to the east, Oklahoma to the """
        """southeast, New Mexico to the south, Utah to the west, and """
        """touches Arizona to the southwest at the Four Corners. Colorado """
        """is noted for its vivid landscape of mountains, forests, high """
        """plains, mesas, canyons, plateaus, rivers and desert lands. """
        """Colorado is part of the western and southwestern United States """
        """and is one of the Mountain States. Denver is the capital and """
        """most populous city of Colorado. Residents of the state are """
        """known as Coloradans, although the antiquated term "Coloradoan" """
        """is occasionally used.""")


# For info on measurement of lexical diversity,
# read https://core.ac.uk/download/pdf/82620241.pdf
def safe_divide(numerator, denominator):
    if denominator == 0:
        index = 0
    else:
        index = numerator/denominator
    return index


# takes in a doc
def ttr(text):  # type-token ratio (1956, Templin)
    ntokens = len(text)
    ntypes = len(set(text))
    return safe_divide(ntypes, ntokens)


# takes in a doc, preferably after Lemmatisation
def mtld(input, min=10):  # original MTLD described in Jarvis & McCarthy
    def mtlder(text):
        total_segment = 0
        text_length = 0
        start = 0
        for x in range(len(text)):
            text_segment = text[start:x+1]
            if x+1 == len(text):  # if reach end of text
                total_segment += safe_divide(
                    (1 - ttr(text_segment)), (1 - .72)
                    )
                text_length += len(text_segment)
            else:  # if .720 ttr is reached
                if ttr(text_segment) < .720 and len(text_segment) >= min:
                    total_segment += 1
                    text_length += len(text_segment)
                    start = x+1
                else:
                    continue
        mtld = safe_divide(text_length, total_segment)
        return mtld
    input_reversed = list(reversed(input))
    # take the average of normal and reverse mtld(text)
    mtld_full = safe_divide((mtlder(input)+mtlder(input_reversed)), 2)
    return mtld_full


# takes in a doc object from spaCy
def avg_sentence_length(doc):
    nsentence = len(list(doc.sents))
    # this is really total number of tokens since punctuations are included
    text_length = len(doc)
    avg_sentence_length = safe_divide(text_length, nsentence)
    return avg_sentence_length
