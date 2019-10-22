class PageSentiment:
    def __init__(self, url, header, blob):
        self.url = url
        self.header = header

        self.overall = blob.sentiment

        self.most_polar_sentence = blob.sentences[0]
        self.least_polar_sentence = blob.sentences[0]
        self.most_objective_sentence = blob.sentences[0]
        self.most_subjective_sentence = blob.sentences[0]

        for sentence in blob.sentences[1:]:
            if (
                self.most_polar_sentence.sentiment.polarity
                < sentence.sentiment.polarity
            ):
                self.most_polar_sentence = sentence

            if (
                self.least_polar_sentence.sentiment.polarity
                > sentence.sentiment.polarity
            ):
                self.least_polar_sentence = sentence

            if (
                self.most_objective_sentence.sentiment.subjectivity
                > sentence.sentiment.subjectivity
            ):
                self.most_objective_sentence = sentence

            if (
                self.most_subjective_sentence.sentiment.subjectivity
                < sentence.sentiment.subjectivity
            ):
                self.most_subjective_sentence = sentence
