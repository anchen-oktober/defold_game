import requests
import sys

def load_system_prompt(path="defold_prompt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

class DefoldAgent:
    def __init__(self, model="gemma:2b", url="http://localhost:11434/api/generate"):
        self.model = model
        self.url = url
        self.system_prompt = load_system_prompt()

    def ask_scenario(self):
        print("🎮 Опишите сценарий вашей игры (или напишите 'exit' для выхода):")

    def generate_base_code(self, description: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"{self.system_prompt}\n\nСгенерируй базовый Lua-скрипт для Defold.\n\nОписание игры:\n{description}\n\nКод:",
            "stream": False
        }
        response = requests.post(self.url, json=payload)
        return response.json().get("response", "").strip()

    def ask_additions(self):
        print("⚙️ Какие дополнения нужны? (например: UI, анимации, звук) или 'exit' для выхода:")

    def generate_additions(self, base_code: str, additions: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"{self.system_prompt}\n\nВот базовый Lua-скрипт:\n{base_code}\n\nДобавь следующие дополнения: {additions}\n\nОбновлённый код:",
            "stream": False
        }
        response = requests.post(self.url, json=payload)
        return response.json().get("response", "").strip()

if __name__ == "__main__":
    agent = DefoldAgent()

    while True:
        agent.ask_scenario()
        scenario = input("Ваш сценарий: ")
        if scenario.lower() == "exit":
            print("👋 Выход из программы.")
            sys.exit()

        base_code = agent.generate_base_code(scenario)
        print("\n=== Базовый Lua-код ===\n", base_code)

        agent.ask_additions()
        additions = input("Ваши дополнения: ")
        if additions.lower() == "exit":
            print("👋 Выход из программы.")
            sys.exit()

        updated_code = agent.generate_additions(base_code, additions)
        print("\n=== Обновлённый Lua-код ===\n", updated_code)