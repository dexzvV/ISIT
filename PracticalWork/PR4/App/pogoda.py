import tkinter as tk
from tkinter import ttk
from datetime import datetime
import requests


class WeatherExpertSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("БИБИЗЯН ПОГОДА 3000")
        self.root.geometry("850x650")
        self.root.configure(bg="white")
        self.city_var = tk.StringVar()
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Action.TButton",
            background="#FF69B4",
            foreground="white",
            font=("Arial", 10, "bold"),
        )

    def create_widgets(self):
        header = tk.Frame(self.root, bg="#FF69B4", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text="БИБИЗЯН ПОГОДА",
            fg="white",
            bg="#FF69B4",
            font=("Arial", 24, "bold"),
        ).pack(anchor="w", padx=20, pady=(15, 0))
        tk.Label(
            header,
            text="Машина вывода реляционного типа (Бибизян Edition)",
            fg="#ffe0f0",
            bg="#FF69B4",
            font=("Arial", 12),
        ).pack(anchor="w", padx=20)

        selection_bar = tk.Frame(self.root, bg="#fff0f5", pady=20)
        selection_bar.pack(fill="x")
        tk.Label(
            selection_bar,
            text="Выберите город бибизян:",
            bg="#fff0f5",
            font=("Arial", 12, "bold"),
        ).pack(side="left", padx=(20, 10))
        cities = ["Макеевка", "Донецк", "Ростов", "Москва", "Санкт-Петербург"]
        self.city_var.set(cities[0])
        city_menu = ttk.OptionMenu(selection_bar, self.city_var, cities[0], *cities)
        city_menu.pack(side="left", padx=10)
        btn_update = tk.Button(
            selection_bar,
            text="Получить бибизян",
            bg="#FF1493",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.get_weather,
            padx=20,
        )
        btn_update.pack(side="left", padx=20)

        self.main_content = tk.Frame(self.root, bg="white", pady=20)
        self.main_content.pack(fill="both", expand=True, padx=40)

        self.city_label = tk.Label(
            self.main_content,
            text="Ждем бибизян...",
            font=("Arial", 28, "bold"),
            bg="white",
            fg="#333",
        )
        self.city_label.pack(anchor="w")
        self.condition_label = tk.Label(
            self.main_content, text="-", font=("Arial", 14), bg="white", fg="#FF69B4"
        )
        self.condition_label.pack(anchor="w", pady=(0, 20))

        self.cards_frame = tk.Frame(self.main_content, bg="white")
        self.cards_frame.pack(fill="both", expand=True)

        self.cards = {}
        parameters = [
            ("Температура бибизян", "#fff0f5", 0, 0),
            ("Ощущается как бибизян", "#fff5f8", 0, 1),
            ("Влажность бибизян", "#fdf0ff", 0, 2),
            ("Ветер бибизян", "#fffafa", 1, 0),
            ("Давление бибизян", "#f5f0ff", 1, 1),
            ("Осадки бибизян", "#f0ffff", 1, 2),
        ]

        for title, color, row, col in parameters:
            card = tk.Frame(
                self.cards_frame,
                bg=color,
                highlightbackground="#FFC0CB",
                highlightthickness=1,
                bd=0,
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            tk.Label(
                card, text=title, bg=color, font=("Arial", 10, "bold"), fg="#D02090"
            ).pack(anchor="w", padx=10, pady=(10, 0))
            val_label = tk.Label(
                card, text="-", bg=color, font=("Arial", 20, "bold"), fg="#333"
            )
            val_label.pack(anchor="w", padx=10)
            desc_label = tk.Label(
                card, text="-", bg=color, font=("Arial", 9, "italic"), fg="gray"
            )
            desc_label.pack(anchor="w", padx=10, pady=(0, 10))
            self.cards[title] = (val_label, desc_label)

        for i in range(3):
            self.cards_frame.grid_columnconfigure(i, weight=1)

        self.footer_label = tk.Label(
            self.root, text="", bg="white", fg="#FF69B4", font=("Arial", 9)
        )
        self.footer_label.pack(pady=10)

    def get_weather(self):
        city = self.city_var.get()
        coords = {
            "Макеевка": (48.023, 37.925),
            "Донецк": (48.015, 37.802),
            "Ростов": (47.222, 39.720),
            "Москва": (55.755, 37.617),
            "Санкт-Петербург": (59.937, 30.308),
        }.get(city)

        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={coords[0]}&longitude={coords[1]}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,surface_pressure,wind_speed_10m,weather_code"
            res = requests.get(url).json()["current"]
            self.city_label.config(text=f"Бибизян в г. {city}")
            self.condition_label.config(
                text=f"Состояние бибизян: {self.get_condition(res['weather_code'])}"
            )
            self.update_card(
                "Температура бибизян",
                f"{res['temperature_2m']}°C",
                self.eval_temp(res["temperature_2m"]),
            )
            self.update_card(
                "Ощущается как бибизян",
                f"{res['apparent_temperature']}°C",
                self.eval_feels(res["apparent_temperature"]),
            )
            self.update_card(
                "Влажность бибизян",
                f"{res['relative_humidity_2m']}%",
                "Бибизяне не мокро",
            )
            self.update_card(
                "Ветер бибизян",
                f"{res['wind_speed_10m']} км/ч",
                self.eval_wind(res["wind_speed_10m"]),
            )
            self.update_card(
                "Давление бибизян",
                f"{int(res['surface_pressure'])} гПа",
                "Бибизян в норме",
            )
            self.update_card(
                "Осадки бибизян", f"{res['precipitation']} мм", "Бибизян сухой"
            )
            self.footer_label.config(
                text=f"Бибизяны обновлены для {city}: {datetime.now().strftime('%H:%M:%S')}"
            )
        except Exception:
            self.city_label.config(text="Бибизян-ошибка!")

    def update_card(self, title, val, desc):
        self.cards[title][0].config(text=val)
        self.cards[title][1].config(text=desc)

    def get_condition(self, code):
        mapping = {
            0: "Ясно (бибизян рад)",
            1: "Почти ясно",
            3: "Пасмурно",
            61: "Дождь",
            71: "Снег",
        }
        return mapping.get(code, "Бибизян в недоумении")

    def eval_temp(self, t):
        if t < -10:
            return "Бибизяну очень холодно"
        elif t < 0:
            return "Бибизяну просто холодно"
        elif t < 15:
            return "Бибизяну прохладно"
        return "Бибизяну тепло"

    def eval_feels(self, t):
        if t < 0:
            return "Бибизян кутается в мех"
        return "Бибизяну комфортно"

    def eval_wind(self, w):
        if w < 5:
            return "Бибизяну обдувает слабый ветер"
        elif w < 15:
            return "Бибизяну обдувает умеренный ветер"
        return "Бибизяну сдувает!"

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = WeatherExpertSystem()
    app.run()
