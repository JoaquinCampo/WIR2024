import redditAPI
import huggingface

class Politician:
    """
    A class to represent a politician.
    
    Attributes:
        name (str): The full name of the politician.
        first_name (str): The first name of the politician.
        last_name (str): The last name of the politician.
        party (str): The political party of the politician.
        opinions (array of ('thread', [{'label', 'score'})): An array that contains the opinions of the Politician
                                                            and a measure of positivenes associated with the opinion.
                                                            Example: [{'thread': 'Trump is normal', 'label': 'Neutral', 'score': 0.901429295539856}]
    """

    def __init__(self, name, party):
        self.name = name
        self.party = party
        self.first_name, self.last_name = self.split_name(name)
        self.opinions = []
        self.after = None

    def split_name(self, name):
        """
        Splits the full name into first and last name. Assumes the last token as the last name,
        and the rest as the first name.

        Parameters:
           name (str): The full name of the politician.

        Returns:
           tuple: first name, last name
        """
        parts = name.split()
        if len(parts) > 1:
            return (' '.join(parts[:-1]), parts[-1])
        else:
            return (name, "")  # Single name 

    def display_info(self):
        return f"Name: {self.name}, First Name: {self.first_name}, Last Name: {self.last_name}, Party: {self.party}"
    
    def retrieve_info(self):
        threads, self.after = redditAPI.get_politician_data(self.last_name, self.after)
        
        sentiment_results = huggingface.analyse_sentiment(self.last_name, threads)
        
        i = 0
        for sentiment in sentiment_results:
            result = sentiment
            opinion = {
                'thread': threads[i],   # The results are returned in order according to the threads
                'label': sentiment['label'],
                'score': sentiment['score']
            }
            self.opinions.append(opinion)
            i+= 1

