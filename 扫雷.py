import random
import tkinter as tk
from tkinter import messagebox

# 游戏难度对应的参数
DIFFICULTIES = {
    "简单": (10, 10, 20),
    "中等": (20, 20, 40),
    "困难": (30, 30, 99),
}

class Minesweeper:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.visible = [[False for _ in range(cols)] for _ in range(rows)]
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)]
        self.marked = [[False for _ in range(cols)] for _ in range(rows)]
        self.gameover = False
        self.unrevealed = rows * cols - mines
        # 初始化地雷
        for i in range(mines):
            while True:
                x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
                if self.board[x][y] == 0:
                    self.board[x][y] = -1
                    break
        # 计算周围的地雷数
        for i in range(rows):
            for j in range(cols):
                if self.board[i][j] != -1:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if (
                                0 <= ni < rows
                                and 0 <= nj < cols
                                and self.board[ni][nj] == -1
                            ):
                                self.board[i][j] += 1

    def click(self, x, y):
        if self.visible[x][y] or self.flagged[x][y] or self.gameover:
            return
        if self.board[x][y] == -1:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] == -1:
                        self.visible[i][j] = True
            self.gameover = True
            messagebox.showerror("游戏结束", "你输了！")
            return
        self.visible[x][y] = True
        self.unrevealed -= 1
        if self.unrevealed == 0:
            self.gameover = True
            messagebox.showinfo("游戏结束", "你赢了！")
            return
        if self.board[x][y] == 0:
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = x + di, y + dj
                    if 0 <= ni < self.rows and 0 <= nj < self.cols:
                        self.click(ni, nj)

    def flag(self, x, y):
        if self.visible[x][y] or self.gameover:
            return
        self.flagged[x][y] = not self.flagged[x][y]
        self.marked[x][y] = False

    def mark(self, x, y):
        if self.visible[x][y] or self.gameover:
            return
        if self.flagged[x][y]:  # 若该格子已经被标记为旗子，则将其状态改为未标记状态
            self.flagged[x][y] = False
        else:
            self.marked[x][y] = not self.marked[x][y]
    
    def render(self, canvas):
        canvas.delete("all")
        # 绘制格子
        for i in range(self.rows):
            for j in range(self.cols):
                x0, y0 = j * 25, i * 25
                x1, y1 = x0 + 24, y0 + 24
                if self.flagged[i][j]:
                    canvas.create_rectangle(
                        x0, y0, x1, y1, fill="orange", outline="black"
                    )
                elif self.marked[i][j]:
                    canvas.create_rectangle(
                        x0, y0, x1, y1, fill="gray", outline="black"
                    )
                    canvas.create_text(
                        x0 + 12, y0 + 12, text="?", font=("Arial", 16), fill="black"
                    )
                elif not self.visible[i][j]:
                    canvas.create_rectangle(
                        x0, y0, x1, y1, fill="gray", outline="black"
                    )
                elif self.board[i][j] == -1:
                    canvas.create_rectangle(
                        x0, y0, x1, y1, fill="red", outline="black"
                    )
                    canvas.create_text(
                        x0 + 12, y0 + 12, text="*", font=("Arial", 16), fill="white"
                    )
                else:
                    num = self.board[i][j]
                    color = (
                        "blue",
                        "green",
                        "red",
                        "purple",
                        "maroon",
                        "turquoise",
                        "black",
                        "gray",
                    )[num - 1]
                    canvas.create_rectangle(
                        x0, y0, x1, y1, fill="white", outline="black"
                    )
                    canvas.create_text(
                        x0 + 12, y0 + 12, text=str(num), font=("Arial", 16), fill=color
                    )
        for i in range(self.rows):
            for j in range(self.cols):
                if self.flagged[i][j] and self.board[i][j] == -1:
                    x0, y0 = j * 25, i * 25
                    x1, y1 = x0 + 24, y0 + 24
                    canvas.create_text(
                        x0 + 12, y0 + 12, text="P", font=("Arial", 16), fill="black"
                    )

    def __str__(self):
        lines = []
        for row in self.board:
            line = ""
            for cell in row:
                if cell == -1:
                    line += "*"
                elif cell == 0:
                    line += " "
                else:
                    line += str(cell)
            lines.append(line)
        return "\n".join(lines)


class MinesweeperApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("扫雷")
        self.canvas = tk.Canvas(self.window, width=750, height=750)
        self.canvas.pack(side="top", fill="both", expand=1)
        # 初始化游戏
        self.game = None
        # 创建控件
        self.frame = tk.Frame(self.window)
        self.frame.pack(side="bottom", fill="x")
        self.difficulty_var = tk.StringVar()
        self.difficulty_var.set("简单")
        for difficulty in DIFFICULTIES:
            tk.Radiobutton(
                self.frame,
                text=difficulty,
                variable=self.difficulty_var,
                value=difficulty,
                command=self.new_game,
            ).pack(side="left")
        self.new_game_button = tk.Button(
            self.frame, text="新游戏", command=self.new_game
        )
        self.new_game_button.pack(side="right")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

    def on_right_click(self, event):
        if self.game is None:
            return
        x, y = event.x // self.block_size, event.y //  self.block_size
        self.game.mark(x, y)
        self.game.render(self.canvas)

    def run(self):
        # 进入主循环
        self.window.mainloop()

    def new_game(self):
        rows, cols, mines = DIFFICULTIES[self.difficulty_var.get()]
        self.game = Minesweeper(rows, cols, mines)
        self.game.render(self.canvas)

    def on_click(self, event):
        if self.game is None:
            return
        x, y = event.y // 25, event.x // 25
        self.game.click(x, y)
        self.game.render(self.canvas)

    def on_double_click(self, event):
        if self.game is None:
            return
        x, y = event.y // 25, event.x // 25
        self.game.flag(x, y)
        self.game.render(self.canvas)


if __name__ == "__main__":
    app = MinesweeperApp()
    app.run()
