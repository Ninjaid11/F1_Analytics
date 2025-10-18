from src.llm.llm_service import LLMService

class F1Analytics:

    def __init__(self):
        self.llm = LLMService()

    def analyze_f1_data(self, pilots, results=None):
        if not pilots:
            return "Нет данных для анализа."

        drivers_text = "\n".join(
            [f"{p['№']}. {p['name']} {p['surname']} — {p['team']} — {p['PTS']}"
             for p in pilots]
        )

        results_text = ""
        if results:
            results_text = "\n\nРезультаты последних гонок:\n" + "\n".join(
                [f"{r['grand_prix']} ({r['date']}): победитель {r['winner']} ({r['team']}), "
                 f"{r['laps']} кругов, время {r['time']}"
                 for r in results]
            )

        system_instruction = """
        You are a Formula 1 expert and sports commentator.
        Your task is to create a short, lively, and exciting race and season summary.
        Use emojis 🎉🏁🔥⚡️ to convey emotions and highlight thrilling moments.
        Each text block should be 3–5 sentences long, full of energy and dynamics.
        Present the Top 5 drivers as a numbered list, including their points and teams.
        """

        user_prompt = f"""
        Here are the latest driver statistics:

        {drivers_text}

        And here are the most recent race results of this season:

        {results_text}

        Your task:
        1. Highlight the top 3 or top 5 drivers of the season in a numbered list.
        2. Provide 2–3 interesting facts about the races or drivers.
        3. Make a prediction for the upcoming race — for both teams and drivers.
        4. Write in the style of a sports commentator: short, dynamic, engaging.
        5. Don’t just list facts — make them part of a vivid story with emotions and emojis.
        6. Clearly separate the section with the prediction for the next race.
        7. Give the answer in Russian.
        """

        return self.llm.generate(system_instruction, user_prompt)
