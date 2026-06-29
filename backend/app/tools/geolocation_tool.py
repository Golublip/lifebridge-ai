class GeolocationTool:
    """
    Computes distances, checks zip codes, and coordinates region-specific lookup.
    """
    def estimate_distance(self, zip_a: str, zip_b: str) -> float:
        """
        Mock distance calculation based on ZIP code differences
        """
        if zip_a == zip_b:
            return 1.2
        try:
            val_a = int(zip_a[:3])
            val_b = int(zip_b[:3])
            return float(abs(val_a - val_b)) * 1.5 + 2.0
        except ValueError:
            return 8.5
