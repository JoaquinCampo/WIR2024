import redditAPI
import huggingface

class Politician:
    """
    Represents a politician with their name, party, opinions, and other information.

    Attributes:
        name (str): The full name of the politician.
        party (str): The political party the politician belongs to.
        first_name (str): The first name of the politician.
        last_name (str): The last name of the politician.
        opinions (list): A list of opinions expressed by the politician.
        after (str): A token used for pagination when retrieving politician data.

    Methods:
        split_name(name): Splits the full name into first and last name.
        display_info(): Returns a string with the politician's information.
        retrieve_info(): Retrieves and analyzes politician data from Reddit and Hugging Face.
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
            return (name, "")

    def display_info(self):
        """
        Returns a string with the politician's information.

        Returns:
            str: The politician's information.
        """
        return f"Name: {self.name}, First Name: {self.first_name}, Last Name: {self.last_name}, Party: {self.party}"
    
    def retrieve_info(self):
        """
        Retrieves and analyzes politician data from Reddit and Hugging Face.
        Updates the opinions list with the analyzed posts.

        Returns:
            None
        """
        posts, self.after = redditAPI.get_politician_data(self.last_name, self.after)
        
        print(f" la cantidad de posts es: {len(posts)}")

        scored_posts = huggingface.analyse_sentiment(self.last_name, posts)
        
        for post in scored_posts:
            self.opinions.append(post)

