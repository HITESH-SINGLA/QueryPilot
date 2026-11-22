from backend.app.ingestion.cleaner import TextCleaner


def test_clean_text():

    cleaner = TextCleaner()

    raw = """

        JEE      Physics

        Laws of Motion


        A body of mass 2 kg accelerates at 5 m/s^2.


    """

    cleaned = cleaner.clean(raw)

    assert "JEE Physics" in cleaned

    assert cleaned.endswith("5 m/s^2.")