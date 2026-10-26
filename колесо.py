import tkinter as tk
import random
import math

class WheelQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Английский язык для Серёжи")
        self.root.geometry("750x800")
        self.root.configure(bg="#c8c8c8")

        # Полная база данных притяжательных местоимений
        self.tasks_dict = {
            "мой": {"correct": "my", "wrong": ["his", "her", "its", "your", "our"]},
            "твой": {"correct": "your", "wrong": ["my", "his", "her", "its", "our"]},
            "его": {"correct": "his", "wrong": ["my", "her", "its", "your", "our"]},
            "её": {"correct": "her", "wrong": ["my", "his", "its", "their", "your"]},
            "наш": {"correct": "our", "wrong": ["my", "his", "her", "its", "their"]},
            "их": {"correct": "their", "wrong": ["our", "your", "his", "her", "its"]}
        }
        
        # Активный список оставшихся секторов и их исходных цветов
        self.sectors = ["мой", "твой", "его", "её", "наш", "их"]
        self.colors = ["#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#e67e22", "#9b59b6"]

        # Состояние анимации колеса
        self.angle = 0
        self.speed = 0
        self.is_spinning = False
        self.current_word = None

        # Верхний статус игры
        self.label_status = tk.Label(root, text="Раскрутите колесо фортуны!", font=("Arial", 16, "bold"), bg="#c8c8c8", fg="black")
        self.label_status.pack(pady=15)

        # Холст для рисования колеса
        self.canvas = tk.Canvas(root, width=420, height=420, bg="#c8c8c8", highlightthickness=0)
        self.canvas.pack()

        # Кнопка запуска
        self.btn_spin = tk.Button(root, text="КРУТИТЬ КОЛЕСО", font=("Arial", 14, "bold"), bg="#2ecc71", fg="white", command=self.start_spin, width=20, height=2)
        self.btn_spin.pack(pady=15)

        # Контейнер для викторины (изначально скрыт)
        self.frame_quiz = tk.Frame(root, bg="#c8c8c8")
        
        self.label_question = tk.Label(self.frame_quiz, text="", font=("Arial", 14, "bold"), bg="#c8c8c8", fg="#2c3e50")
        self.label_question.pack(pady=5)
        
        # Сетка 2x3 для 6 окошек вариантов ответа
        self.frame_buttons = tk.Frame(self.frame_quiz, bg="#c8c8c8")
        self.frame_buttons.pack()
        
        self.option_buttons = []
        for i in range(6):
            row = i // 3
            col = i % 3
            btn = tk.Button(self.frame_buttons, text="", font=("Arial", 12, "bold"), width=12, height=2, bd=2, relief="groove")
            btn.grid(row=row, column=col, padx=8, pady=8)
            self.option_buttons.append(btn)

        self.draw_wheel()

    def draw_wheel(self):
        self.canvas.delete("all")
        cx, cy, r = 210, 210, 170
        num_sectors = len(self.sectors)

        # Если секторов больше нет, колесо не рисуем
        if num_sectors == 0:
            return

        arc_angle = 360 / num_sectors

        # Отрисовка только оставшихся секторов
        for i in range(num_sectors):
            start = (self.angle + i * arc_angle) % 360
            
            self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=arc_angle, fill=self.colors[i], outline="black", width=2)
            
            # Названия секторов внутри круга
            mid_angle = math.radians(start + arc_angle / 2)
            tx = cx + (r * 0.6) * math.cos(mid_angle)
            ty = cy - (r * 0.6) * math.sin(mid_angle)
            
            self.canvas.create_text(tx, ty, text=self.sectors[i], font=("Arial", 12, "bold"), fill="black")

        # Стрелка-указатель сверху колеса
        self.canvas.create_polygon(cx, cy-r-15, cx-12, cy-r+10, cx+12, cy-r+10, fill="black")
        
        # Центральная ось
        self.canvas.create_oval(cx-10, cy-10, cx+10, cy+10, fill="white", outline="black", width=2)

    def start_spin(self):
        if not self.is_spinning and len(self.sectors) > 0:
            self.frame_quiz.pack_forget()
            self.is_spinning = True
            self.speed = random.uniform(15, 25)
            self.label_status.config(text="Колесо крутится...", fg="black")
            self.animate()

    def animate(self):
        num_sectors = len(self.sectors)
        if num_sectors == 0:
            return

        arc_angle = 360 / num_sectors

        if self.speed > 0.1:
            self.angle = (self.angle + self.speed) % 360
            self.speed *= 0.97
            self.draw_wheel()
            self.root.after(20, self.animate)
        else:
            self.is_spinning = False
            self.speed = 0
            
            # Рассчитываем, какой сектор оказался вверху (угол 90 градусов)
            pointer_pos = (90 - self.angle) % 360
            sector_idx = int(pointer_pos // arc_angle) % num_sectors
            
            # Запоминаем текущий индекс выпавшего сектора, чтобы удалить его в случае успеха
            self.current_sector_index = sector_idx
            self.current_word = self.sectors[sector_idx]
            
            self.label_status.config(text="Колесо остановилось! Найдите перевод:", fg="blue")
            self.show_task(self.current_word)

    def show_task(self, word):
        task = self.tasks_dict[word]
        
        self.label_question.config(text=f"Найдите английский эквивалент слова: « {word} »")
        
        # Генерируем 6 окошек: 1 правильный ответ + 5 неправильных
        options = [task['correct']] + task['wrong']
        random.shuffle(options)  # Каждый раз перемешиваем варианты
        
        for i, btn in enumerate(self.option_buttons):
            choice = options[i]
            btn.config(text=choice, bg="white", fg="black", state="normal",
                       command=lambda c=choice, b=btn: self.check_answer(c, b, task['correct']))
            
        self.frame_quiz.pack(pady=10)

    def check_answer(self, chosen, button, correct):
        if chosen == correct:
            button.config(bg="#2ecc71", fg="white")
            
            # Отключаем кнопки текущего подзадания
            for btn in self.option_buttons:
                btn.config(state="disabled")
            
            # 🔥 УДАЛЯЕМ ПРАВИЛЬНО ОТГАДАННЫЙ СЕКТОР И ЕГО ЦВЕТ ИЗ СПИСКОВ
            self.sectors.pop(self.current_sector_index)
            self.colors.pop(self.current_sector_index)
            
            # Сбрасываем угол, чтобы анимация следующего круга рассчитывалась корректно
            self.angle = 0 
            self.draw_wheel() # Перерисовываем колесо (оно уменьшится в количестве секторов)
            
            # Проверяем финальную победу (если секторов больше не осталось)
            if len(self.sectors) == 0:
                self.canvas.pack_forget() # Полностью прячем колесо
                self.frame_quiz.pack_forget() # Прячем окошки ответов
                self.label_status.config(text="Серёжа Молодец !", font=("Arial", 36, "bold"), fg="#27ae60")
                self.btn_spin.config(state="disabled", text="УРА! ПОБЕДА!")
            else:
                self.label_status.config(text=f"Правильно! Слово «{self.current_word}» угадано и убрано с колеса. Крутите дальше!", fg="green")
        else:
            button.config(bg="#e74c3c", fg="white", state="disabled")
            self.label_status.config(text="Неверно! Ищите правильное окошко.", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = WheelQuizApp(root)
    root.mainloop()