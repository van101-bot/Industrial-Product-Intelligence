import json
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from google import genai


load_dotenv()


@dataclass
class AIExtractionResult:
    product_type: Optional[str] = None
    series: Optional[str] = None
    diameter: Optional[str] = None
    thickness: Optional[str] = None
    arbor_size: Optional[str] = None
    wheel_type: Optional[str] = None
    max_rpm: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "product_type": self.product_type,
            "series": self.series,
            "diameter": self.diameter,
            "thickness": self.thickness,
            "arbor_size": self.arbor_size,
            "wheel_type": self.wheel_type,
            "max_rpm": self.max_rpm,
        }


class MockAIExtractor:
    """
    Deterministic extractor used by automated tests.
    """

    def extract(self, evidence: str) -> AIExtractionResult:

        evidence_lower = evidence.lower()

        result = AIExtractionResult()

        if "cut off wheel" in evidence_lower:
            result.product_type = "Metal Cut-Off Wheel"

        if "performance+" in evidence_lower:
            result.series = "Performance+"

        if '4-1/2"' in evidence:
            result.diameter = "4-1/2 in"

        if ".045" in evidence:
            result.thickness = "0.045 in"

        if '7/8"' in evidence:
            result.arbor_size = "7/8 in"

        if "type 27" in evidence_lower:
            result.wheel_type = "Type 27"

        if "13,300 rpm" in evidence_lower:
            result.max_rpm = "13,300 RPM"

        return result


class GeminiAIExtractor:
    """
    Gemini-powered structured product attribute extractor.
    """

    def __init__(self, model: str = "gemini-3.6-flash"):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Add it to your .env file."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def extract(self, evidence: str) -> AIExtractionResult:

        prompt = f"""
You are an industrial product data extraction system.

Extract product attributes ONLY from the supplied evidence.

IMPORTANT RULES:

1. Never invent information.
2. Never use outside knowledge.
3. If an attribute is not explicitly supported by the evidence,
   return null.
4. Preserve the technical meaning of the evidence.
5. Return ONLY valid JSON.
6. Do not include markdown.
7. Use the following exact field names.

Fields:

product_type
series
diameter
thickness
arbor_size
wheel_type
max_rpm

Evidence:

{evidence}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
            },
        )

        data = json.loads(response.text)

        return AIExtractionResult(
            product_type=data.get("product_type"),
            series=data.get("series"),
            diameter=data.get("diameter"),
            thickness=data.get("thickness"),
            arbor_size=data.get("arbor_size"),
            wheel_type=data.get("wheel_type"),
            max_rpm=data.get("max_rpm"),
        )