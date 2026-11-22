import re

## The study material may contain some extra blank and un needed spaces, so we need to clean the text before chunking. This class is used to clean the text.
class TextCleaner:
    """
    Cleans extracted PDF text before chunking.
    """

    def clean(self, text: str) -> str:

        # Replace multiple spaces with one
        text = re.sub(r"[ \t]+", " ", text)

        # Replace multiple newlines with one
        text = re.sub(r"\n{2,}", "\n", text)

        # Remove leading/trailing spaces
        text = text.strip()

        return text
    
## Ideas for V2 cleaner: It currently removes the page number written at the end of the page but in future we can implement a cleaner which identifies the page number format and then acts unoformly on it.