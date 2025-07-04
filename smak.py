import turtle
import time
import random


screen = turtle.Screen()
screen.title("Змейка")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)


snake = []
for i in range(3):
    segment = turtle.Turtle("square")
    segment.color("lime")
    segment.penup()
    segment.goto(-20 * i, 0)
    snake.append(segment)

# Еда
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(random.randint(-280, 280) // 20 * 20, random.randint(-280, 280) // 20 * 20)

# Счет
score = 0
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write(f"Счет: {score}", align="center", font=("Courier", 24, "normal"))

# Переменные для управления
direction = "stop"
game_over = False
has_moved = False

def move():
    global direction, has_moved
    if direction == "up":
        y = snake[0].ycor()
        snake[0].sety(y + 20)
        has_moved = True
    elif direction == "down":
        y = snake[0].ycor()
        snake[0].sety(y - 20)
        has_moved = True
    elif direction == "left":
        x = snake[0].xcor()
        snake[0].setx(x - 20)
        has_moved = True
    elif direction == "right":
        x = snake[0].xcor()
        snake[0].setx(x + 20)
        has_moved = True

def go_up():
    global direction
    if direction != "down":
        direction = "up"

def go_down():
    global direction
    if direction != "up":
        direction = "down"

def go_left():
    global direction
    if direction != "right":
        direction = "left"

def go_right():
    global direction
    if direction != "left":
        direction = "right"


screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

# Основной игровой цикл
while not game_over:
    screen.update()


    if snake[0].distance(food) < 20:
        food.goto(random.randint(-280, 280) // 20 * 20, random.randint(-280, 280) // 20 * 20)
        new_segment = turtle.Turtle("square")
        new_segment.color("lime")
        new_segment.penup()
        snake.append(new_segment)
        score += 10
        score_display.clear()
        score_display.write(f"Счет: {score}", align="center", font=("Courier", 24, "normal"))

    # Движение змейки
    for i in range(len(snake) - 1, 0, -1):
        x = snake[i - 1].xcor()
        y = snake[i - 1].ycor()
        snake[i].goto(x, y)
    move()

    if has_moved:

        if (snake[0].xcor() > 290 or snake[0].xcor() < -290 or
            snake[0].ycor() > 290 or snake[0].ycor() < -290):
            score_display.clear()
            score_display.goto(0, 0)
            score_display.color("red")
            score_display.write("Вы проиграли!\nСчет: " + str(score), align="center", font=("Courier", 36, "bold"))
            game_over = True

        for segment in snake[1:]:
            if snake[0].distance(segment) < 5:
                score_display.clear()
                score_display.goto(0, 0)
                score_display.color("red")
                score_display.write("Вы проиграли!\nСчет: " + str(score), align="center", font=("Courier", 36, "bold"))
                game_over = True


        if len(snake) >= 10:
            score_display.clear()
            score_display.goto(0, 0)
            score_display.color("green")
            score_display.write("Вы выиграли!\nСчет: " + str(score), align="center", font=("Courier", 36, "bold"))
            game_over = True

    time.sleep(0.1)

#я закончил2
screen.mainloop()