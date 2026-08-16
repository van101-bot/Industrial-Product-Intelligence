class MockAIExtractor:

    def extract_product_attributes(self, text: str) -> dict:

        text_lower = text.lower()

        result = {
            "diameter": None,
            "thickness": None,
            "arbor": None,
            "length": None,
            "width": None,
            "height": None,
            "pack_quantity": None,
            "product_type": None,
        }

        if "cut off" in text_lower:

            result["product_type"] = "Metal Cut Off Disc"

        return result