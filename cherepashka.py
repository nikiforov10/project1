# import turtle
# import colorsys
#
#
# loop_1 = 25
# loop_2 = 15
# circle_radius = 50
#
# turtle.speed(0)
# turtle.bgcolor("black")
# turtle.width(2)
# turtle.setup((circle_radius + 282.84) * 2, (circle_radius + 282.84) * 2)
# turtle.sety(-circle_radius)
#
# for i in range(loop_1):
#     for j in range(loop_2):
#         turtle.color(colorsys.hsv_to_rgb(j/loop_2, i/loop_1, 1))
#         turtle.right(90)
#         turtle.circle(200-i*4, 90)
#         turtle.left(90)
#         turtle.circle(200-i*4, 90)
#         turtle.left(180)
#         turtle.circle(circle_radius, 360 / loop_2)
#
# turtle.ht()
# turtle.exitonclick()
# turtle.mainloop()
from turtle import *
from time import sleep

bgcolor("black")
t = [Turtle(), Turtle()]
x = 6
colors = ["blue", "yellow", "white"]
for index, i in enumerate(t):
  i.speed(0)
  i.color("white")
  i.shape("circle")
  i.shapesize(0.3)
  i.width(3)
  i.pu()
  i.seth(90)
  i.fd(350)
  i.seth(-180)
  i.pd()
t[0].pu()

delay(0)
speed(0)
ht()
sleep(4)
for i in colors:
  color(i)
  for i in range(360):
    t[0].fd(x)
    t[0].lt(1)
    pu()
    goto(t[0].pos())
    pd()
    t[1].fd(2 * x)
    t[1].lt(2)
    goto(t[1].pos())
done()