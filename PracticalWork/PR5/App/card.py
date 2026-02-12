import tkinter as tk
from tkinter import messagebox
import tkintermapview
import requests
from PIL import Image, ImageTk
from io import BytesIO


class WorldMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("World Map Country Information")
        self.root.geometry("1000x700")

        self.map_widget = tkintermapview.TkinterMapView(
            self.root, width=1000, height=700, corner_radius=0
        )
        self.map_widget.pack(fill="both", expand=True)

        self.map_widget.set_position(55.75, 37.61)
        self.map_widget.set_zoom(4)

        countries = {
            "Russia": (55.75, 37.61),
            "Germany": (52.52, 13.40),
            "Spain": (40.41, -3.70),
            "India": (28.61, 77.20),
        }

        for name, coords in countries.items():
            self.map_widget.set_marker(
                coords[0], coords[1], text=name, command=self.on_marker_click
            )

        self.info_frame = None

    def on_marker_click(self, marker):
        country_name = marker.text
        self.fetch_country_data(country_name)

    def fetch_country_data(self, name):
        try:
            response = requests.get(f"https://restcountries.com/v3.1/name/{name}")
            response.raise_for_status()
            data = response.json()[0]

            common_name = data["translations"].get("rus", {}).get("common", name)
            pop = f"{data['population']:,}".replace(",", " ")
            currency_code = list(data["currencies"].keys())[0]
            currency_name = data["currencies"][currency_code]["name"]
            flag_url = data["flags"]["png"]

            self.show_info_panel(common_name, currency_name, pop, flag_url)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить данные: {e}")

    def show_info_panel(self, name, currency, population, flag_url):
        if self.info_frame:
            self.info_frame.destroy()

        self.info_frame = tk.Frame(
            self.root, bg="white", highlightbackground="gray", highlightthickness=1
        )
        self.info_frame.place(x=20, y=20, width=300, height=350)

        tk.Label(
            self.info_frame, text=name, font=("Arial", 16, "bold"), bg="white"
        ).pack(pady=10)

        img_response = requests.get(flag_url)
        img_data = Image.open(BytesIO(img_response.content))
        img_data = img_data.resize((150, 90))
        self.flag_img = ImageTk.PhotoImage(img_data)

        tk.Label(self.info_frame, image=self.flag_img, bg="white").pack(pady=5)

        tk.Label(self.info_frame, text=f"Валюта: {currency}", bg="white").pack(
            anchor="w", padx=20, pady=5
        )
        tk.Label(self.info_frame, text=f"Население: {population}", bg="white").pack(
            anchor="w", padx=20, pady=5
        )

        tk.Button(
            self.info_frame, text="Закрыть", command=self.info_frame.destroy
        ).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = WorldMapApp(root)
    root.mainloop()
