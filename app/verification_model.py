import random


class VerificationModel:
    def verify(self, image_bytes):
        """
        A stub classifier that returns a hardcoded dictionary with random confidence.
        """
        materials = ["concrete", "wood", "metal", "unknown"]
        return {
            "material": random.choice(materials),
            "confidence": random.uniform(0.7, 0.95),
        }
