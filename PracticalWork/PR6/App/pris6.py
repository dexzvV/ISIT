import tkinter as tk
from tkinter import ttk


class DecisionTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Дерево решений")
        self.root.geometry("950x600")

        self.tree_data = {
            "Запускать новый продукт?": {
                "Да": {
                    "Высокий спрос?": {
                        "Да": {
                            "Высокая прибыль?": {
                                "Да": {
                                    "Низкая конкуренция?": {
                                        "Да": "Запускать немедленно",
                                        "Нет": "Нужно УТП",
                                    }
                                },
                                "Нет": {
                                    "Низкая конкуренция?": {
                                        "Да": "Анализировать конкурентов",
                                        "Нет": "Искать нишу",
                                    }
                                },
                            }
                        },
                        "Нет": {
                            "Низкий спрос?": {
                                "Да": {
                                    "Есть сезонность?": {
                                        "Да": {
                                            "Пик спроса скоро?": {
                                                "Да": "Готовиться к запуску",
                                                "Нет": "Отложить запуск",
                                            }
                                        },
                                        "Нет": {
                                            "Пик спроса не скоро?": {
                                                "Да": "Развивать в низкий сезон",
                                                "Нет": "Искать другой рынок",
                                            }
                                        },
                                    }
                                },
                                "Нет": "Отказаться от запуска",
                            }
                        },
                    }
                },
                "Нет": "Отказаться от запуска",
            }
        }

        self.history = []
        self.current_path = []
        self.setup_ui()
        self.reset_game()

    def setup_ui(self):
        main_container = tk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(main_container)
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.heading("#0", text="Структура дерева решений", anchor="w")

        self.fill_tree_view("", self.tree_data)

        right_panel = tk.Frame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.q_frame = tk.LabelFrame(
            right_panel, text="Текущий вопрос", font=("Arial", 10)
        )
        self.q_frame.pack(fill="x", pady=(0, 10))

        self.lbl_question = tk.Label(
            self.q_frame, text="", font=("Arial", 12, "bold"), pady=15
        )
        self.lbl_question.pack()

        btn_box = tk.Frame(self.q_frame)
        btn_box.pack(pady=10)

        self.btn_yes = tk.Button(
            btn_box, text="Да", width=12, command=lambda: self.process_step("Да")
        )
        self.btn_yes.pack(side="left", padx=5)

        self.btn_no = tk.Button(
            btn_box, text="Нет", width=12, command=lambda: self.process_step("Нет")
        )
        self.btn_no.pack(side="left", padx=5)

        self.r_frame = tk.LabelFrame(right_panel, text="Результат")
        self.r_frame.pack(fill="x", pady=10)
        self.lbl_result = tk.Label(
            self.r_frame, text="", font=("Arial", 11), fg="darkgreen", height=2
        )
        self.lbl_result.pack()

        self.h_frame = tk.LabelFrame(right_panel, text="История ответов")
        self.h_frame.pack(fill="both", expand=True)
        self.history_list = tk.Listbox(self.h_frame, font=("Arial", 9))
        self.history_list.pack(fill="both", expand=True, padx=5, pady=5)

        nav_frame = tk.Frame(right_panel)
        nav_frame.pack(fill="x", pady=(10, 0))

        self.btn_back = tk.Button(
            nav_frame, text="Назад", width=10, command=self.go_back
        )
        self.btn_back.pack(side="left", padx=2)

        self.btn_reset = tk.Button(
            nav_frame, text="Сброс", width=10, command=self.reset_game
        )
        self.btn_reset.pack(side="left", padx=2)

    def fill_tree_view(self, parent, data):
        for key, value in data.items():
            node_id = self.tree.insert(parent, "end", text=key, open=True)
            if isinstance(value, dict):
                self.fill_tree_view(node_id, value)

    def get_node_by_path(self):
        node = self.tree_data
        for p in self.current_path:
            node = node[p]
        return node

    def process_step(self, choice):
        node = self.get_node_by_path()
        if isinstance(node, dict) and choice in node:
            q_text = self.lbl_question.cget("text")
            self.history.append(
                (list(self.current_path), f"Вопрос: {q_text} -> Ответ: {choice}")
            )
            self.history_list.insert(tk.END, self.history[-1][1])

            next_content = node[choice]
            if isinstance(next_content, dict):
                self.current_path.append(choice)
                next_q = list(next_content.keys())[0]
                self.current_path.append(next_q)
                self.lbl_question.config(text=next_q)
            else:
                self.lbl_result.config(text=next_content)
                self.lbl_question.config(text="РЕЗУЛЬТАТ")
                self.btn_yes.config(state="disabled")
                self.btn_no.config(state="disabled")

    def go_back(self):
        if self.history:
            prev_path, _ = self.history.pop()
            self.current_path = prev_path
            self.history_list.delete(tk.END)

            self.btn_yes.config(state="normal")
            self.btn_no.config(state="normal")
            self.lbl_result.config(text="")

            node = self.get_node_by_path()
            self.lbl_question.config(text=list(node.keys())[0])

    def reset_game(self):
        self.current_path = ["Запускать новый продукт?"]
        self.history = []
        self.history_list.delete(0, tk.END)
        self.lbl_result.config(text="")
        self.lbl_question.config(text="Запускать новый продукт?")
        self.btn_yes.config(state="normal")
        self.btn_no.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = DecisionTreeApp(root)
    root.mainloop()
