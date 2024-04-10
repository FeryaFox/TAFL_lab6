class NumberUtils:
    @staticmethod
    def covert_number_to_degree(number: int) -> str:
        degrees = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]

        return "".join([degrees[int(i)] for i in str(number)])