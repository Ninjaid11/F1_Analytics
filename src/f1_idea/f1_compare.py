from src.llm.llm_service import LLMService

class F1Compare:

    def __init__(self):
        self.llm = LLMService()

    def compare_pilots(self, pilot1_name: str, pilot2_name: str, pilots_data: list):
        if not pilots_data:
            return "Нет данных о пилоте."

        pilot1 = next((p for p in pilots_data if pilot1_name.lower() in f"{p['name']} {p['surname']}".lower()), None)
        pilot2 = next((p for p in pilots_data if pilot2_name.lower() in f"{p['name']} {p['surname']}".lower()), None)

        if not pilot1 or not pilot2:
            return f"Один из пилотов не найден: {pilot1_name}, {pilot2_name}"

        system_instruction = """
        You are a Formula 1 expert and commentator.
        Compare two drivers based on their current season performance.
        Use emojis 🏎️🔥⚡️ to make it engaging and fun.
        - Give the answer in Russian.
        Give answer whis humor.
        """

        user_prompt = f"""
        Compare these two Formula 1 drivers:

        1 - {pilot1['name']} {pilot1['surname']} — {pilot1['team']} — {pilot1['PTS']} pts  
        2 - {pilot2['name']} {pilot2['surname']} — {pilot2['team']} — {pilot2['PTS']} pts  

        Your task:
        - Compare them by results, points, and momentum.
        - Highlight who is currently stronger and why.
        - Mention team dynamics or possible future outcomes.
        - Write in a short, lively and emotional style with emojis.
        - Give the answer in Russian.
        """

        return self.llm.generate(system_instruction, user_prompt)