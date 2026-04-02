import requests

class DefoldAgent:
    def __init__(self, model="gemma:2b", url="http://localhost:11434/api/generate"):
        self.model = model
        self.url = url

    def ask_scenario(self):
        print("🎮 Опишите сценарий вашей игры (например: тир с 12 целями).")

    def generate_base_code(self, description: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"Сгенерируй базовый Lua-скрипт для Defold.\n\nОписание игры:\n{description}\n\nКод:",
            "stream": False
        }
        response = requests.post(self.url, json=payload)
        return response.json().get("response", "").strip()

    def ask_additions(self):
        print("⚙️ Какие дополнения нужны? (например: UI, анимации, звук)")

    def generate_additions(self, base_code: str, additions: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"Вот базовый Lua-скрипт:\n{base_code}\n\nДобавь следующие дополнения: {additions}\n\nОбновлённый код:",
            "stream": False
        }
        response = requests.post(self.url, json=payload)
        return response.json().get("response", "").strip()


if __name__ == "__main__":
    agent = DefoldAgent()
    agent.ask_scenario()
    scenario = input("Ваш сценарий: ")
    base_code = agent.generate_base_code(scenario)
    print("\n=== Базовый Lua-код ===\n", base_code)

    agent.ask_additions()
    additions = input("Ваши дополнения: ")
    updated_code = agent.generate_additions(base_code, additions)
    print("\n=== Обновлённый Lua-код ===\n", updated_code)