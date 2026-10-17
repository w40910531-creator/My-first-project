import tkinter as tk
import random

WIDTH = 400
HEIGHT = 400
GRID_SIZE = 20
GAME_SPEED = 140  # ความเร็วในการเคลื่อนที่

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("เกมหนอนในทุ่งหญ้า (เก็บผลไม้ 3 ชิ้น)")
        self.root.resizable(False, False)

        # สร้าง Canvas สำหรับแสดงผลเกม
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        # แสดงคะแนนและความยาว
        self.score_label = tk.Label(root, text="คะแนน: 0 | ความยาวหนอน: 3", font=("Arial", 12, "bold"))
        self.score_label.pack(pady=5)

        self.restart()
        self.root.bind("<Key>", self.change_direction)
        self.update_game()

    def restart(self):
        # เริ่มต้นตำแหน่งหนอน
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        
        self.foods = []
        self.bombs = []
        
        # สร้างระเบิด 2 ลูก และผลไม้ 3 ชิ้น
        for _ in range(2):
            self.spawn_bomb()
        for _ in range(3):
            self.spawn_food()

    def spawn_food(self):
        while True:
            pos = [
                random.randrange(0, WIDTH, GRID_SIZE),
                random.randrange(0, HEIGHT, GRID_SIZE)
            ]
            if pos not in self.snake and pos not in self.foods and pos not in self.bombs:
                self.foods.append(pos)
                break

    def spawn_bomb(self):
        while True:
            pos = [
                random.randrange(0, WIDTH, GRID_SIZE),
                random.randrange(0, HEIGHT, GRID_SIZE)
            ]
            if pos not in self.snake and pos not in self.foods and pos not in self.bombs:
                self.bombs.append(pos)
                break

    def change_direction(self, event):
        key = event.keysym
        if key in ["Up", "w", "W"] and self.direction != "Down":
            self.next_direction = "Up"
        elif key in ["Down", "s", "S"] and self.direction != "Up":
            self.next_direction = "Down"
        elif key in ["Left", "a", "A"] and self.direction != "Right":
            self.next_direction = "Left"
        elif key in ["Right", "d", "D"] and self.direction != "Left":
            self.next_direction = "Right"

    def update_game(self):
        self.direction = self.next_direction
        head = list(self.snake[0])

        # ขยับหัวหนอนตามทิศทาง
        if self.direction == "Up":
            head[1] -= GRID_SIZE
        elif self.direction == "Down":
            head[1] += GRID_SIZE
        elif self.direction == "Left":
            head[0] -= GRID_SIZE
        elif self.direction == "Right":
            head[0] += GRID_SIZE

        # กฎใหม่: ชนกำแพงไม่ตาย แต่ทะลุไปโผล่อีกฝั่ง
        if head[0] < 0:
            head[0] = WIDTH - GRID_SIZE
        elif head[0] >= WIDTH:
            head[0] = 0
        
        if head[1] < 0:
            head[1] = HEIGHT - GRID_SIZE
        elif head[1] >= HEIGHT:
            head[1] = 0

        # ถ้าชนตัวเอง -> ตาย
        if head in self.snake:
            self.game_over()
            return

        # เช็คว่าชนระเบิดไหม (กินระเบิดตายทันที)
        if head in self.bombs:
            self.game_over()
            return

        self.snake.insert(0, head)

        # เช็คว่ากินผลไม้ไหม
        if head in self.foods:
            self.score += 1
            self.foods.remove(head)
            self.spawn_food()  # สุ่มผลไม้ใหม่ขึ้นมาแทนที่ชิ้นที่กินไป
            # ตัวใหญ่ขึ้น (ไม่ต้องตัดหางออก)
        else:
            # ถ้าไม่ได้กินผลไม้ ให้ตัดหางออกเพื่อให้ขนาดเท่าเดิม
            self.snake.pop()

        self.render()
        self.root.after(GAME_SPEED, self.update_game)

    def render(self):
        self.canvas.delete("all")

        # วาดพื้นหลังทุ่งหญ้า (สีเขียวธรรมชาติ)
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#88D498", outline="")
        
        # ตกแต่งลายพื้นหญ้าเล็กๆ น้อยๆ
        for i in range(0, WIDTH, 40):
            for j in range(0, HEIGHT, 40):
                self.canvas.create_line(i+10, j+10, i+10, j+5, fill="#75C986", width=2)

        # วาดผลไม้ 3 ชิ้น (🍎)
        for food in self.foods:
            self.canvas.create_oval(
                food[0], food[1], 
                food[0] + GRID_SIZE, food[1] + GRID_SIZE, 
                fill="#FF3366", outline=""
            )

        # วาดระเบิด (💣)
        for bomb in self.bombs:
            self.canvas.create_text(
                bomb[0] + GRID_SIZE/2, bomb[1] + GRID_SIZE/2,
                text="💣", font=("Arial", 14)
            )

        # วาดตัวหนอน (หัวสีเขียวเข้ม ตัวสีฟ้าอ่อน)
        for i, segment in enumerate(self.snake):
            color = "#2E8B57" if i == 0 else "#48D1CC"
            self.canvas.create_rectangle(
                segment[0], segment[1], 
                segment[0] + GRID_SIZE, segment[1] + GRID_SIZE, 
                fill=color, outline="#2E5A36"
            )

        self.score_label.config(text=f"คะแนน: {self.score} | ความยาวหนอน: {len(self.snake)}")

    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#2D3142", outline="")
        self.canvas.create_text(
            WIDTH/2, HEIGHT/2 - 20, 
            text="GAME OVER", font=("Arial", 24, "bold"), fill="#EF476F"
        )
        self.canvas.create_text(
            WIDTH/2, HEIGHT/2 + 20, 
            text="กดปุ่ม Spacebar เพื่อเริ่มเกมใหม่", font=("Arial", 12), fill="#FFD166"
        )
        self.root.bind("<space>", lambda e: self.restart_from_game_over())

    def restart_from_game_over(self):
        self.root.unbind("<space>")
        self.restart()
        self.update_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
