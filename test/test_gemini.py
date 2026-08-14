import os

from dotenv import load_dotenv

from src.ai_extractor import GeminiAIExtractor


load_dotenv()


def test_gemini_connection():

    if not os.getenv("GEMINI_API_KEY"):
        raise AssertionError(
            "GEMINI_API_KEY is missing from .env"
        )

    extractor = GeminiAIExtractor()

    result = extractor.extract(
        """
        4-1/2" x .045" x 7/8"
        Performance+ Metal Cut Off Wheel - Type 27

        Maximum RPM: 13,300 RPM
        """
    )

    assert result.diameter is not None
    assert result.thickness is not None
    assert result.arbor_size is not None