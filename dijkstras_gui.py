from turtle import *
from tkinter import *
from sys import exit


def exit_from_final(x, y):
    global shortest_distance
    if 225 >= (500 - x) ** 2 + (-350 - y) ** 2:
        exit()


def final(starting, ending):
    speed(0)
    penup()
    setposition(500, -365)
    pendown()
    fillcolor('Yellow')
    begin_fill()
    circle(15)
    end_fill()
    penup()
    setposition(493, -363)
    write('end')
    pencolor('Green')
    onscreenclick(exit_from_final)
    global shortest_distance, positions
    if ending == shortest_distance[ending][1]:
        window_1 = Tk()
        Label(window_1, text="Their is no path from " + starting + " to " + ending).grid(row=0, column=0)
        z = Button(window_1, text="close",
                   command=lambda: starting_ending(window_1))
        z.grid(row=2, column=1)
        window_1.mainloop()
    pensize(5)
    setposition(positions[ending])
    speed(1)
    pendown()
    temp = ending
    while starting != temp:
        temp = shortest_distance[temp][1]
        setposition(positions[temp])
    window = Tk()
    Label(window, text="The sortest distance from " + str(starting) + " to " + str(ending) + "=" + str(
        shortest_distance[ending][0])).grid(row=0, column=0)
    z = Button(window, text="close", command=lambda: window.destroy())
    z.grid(row=2, column=1)
    window.mainloop()


def visiting(node, ending):
    global positions, shortest_distance, visited, queue, graph
    for i in graph[node].keys():
        distance_from_node = shortest_distance[node][0] + graph[node][i]
        if i not in visited and shortest_distance[i][0] > distance_from_node:
            if i not in queue:
                queue.append(i)
            penup()
            setposition(positions[node])
            pendown()
            setposition(positions[i])
            shortest_distance[i] = [distance_from_node, node]
    return False


def from_dijkstra(node_1, node_2, window):
    global starting, ending, shortest_distance, visited, queue, graph
    starting = node_1.get()
    ending = node_2.get()
    window.destroy()
    if starting not in graph.keys() or ending not in graph.keys():
        window_1 = Tk()
        Label(window_1, text="Starting node or ending node does not exist").grid(row=0, column=0)
        z = Button(window_1, text="close",
                   command=lambda: starting_ending(window_1))
        z.grid(row=2, column=0)
        window_1.mainloop()
    speed(1)
    shortest_distance = {}
    visited = []
    queue = [starting]
    for i in graph.keys():
        shortest_distance[i] = [9999, i]
    shortest_distance[starting] = [0, starting]
    while queue:
        temp = [9999, 1]
        for i in queue:
            if shortest_distance[i][0] < temp[0]:
                temp = [shortest_distance[i][0], i]
        node = temp[1]
        queue.remove(node)
        if visiting(node, ending):
            break
        visited.append(node)
    final(starting, ending)


def starting_ending(window_1=None):
    if window_1:
        window_1.destroy()
    pencolor("Blue")
    pensize(3)
    window = Tk()
    Label(window, text="Enter starting node:").grid(row=0, column=0)
    node_1 = Entry(window)
    node_1.grid(row=0, column=1)
    Label(window, text="Enter ending node:").grid(row=1, column=0)
    node_2 = Entry(window)
    node_2.grid(row=1, column=1)
    z = Button(window, text="Enter",
               command=lambda node_1=node_1, node_2=node_2, window=window: from_dijkstra(node_1, node_2, window))
    z.grid(row=2, column=1)
    window.mainloop()


def from_click_third(node, click_2, window):
    global graph, click_1
    weight = int(node.get())
    window.destroy()

    graph[click_1][click_2] = weight
    graph[click_2][click_1] = weight
    half_distance = (positions[click_1][0] + positions[click_2][0]) // 2, (
            positions[click_1][1] + positions[click_2][1]) // 2
    pendown()
    setposition(half_distance)
    write(weight)
    setposition(positions[click_2])
    penup()
    click_1 = None


def click_third(x, y):
    global positions, click_1, graph
    if 225 >= (500 - x) ** 2 + (-350 - y) ** 2:
        starting_ending()
    k = True
    for i in positions.keys():
        if 225 >= (positions[i][0] - x) ** 2 + (positions[i][1] - y) ** 2:
            k = False

            if click_1 is None:
                click_1 = i
                setposition(positions[i])
            else:
                window_1 = Tk()
                if i in graph[click_1].keys():
                    Label(window_1, text='Edge already entered').grid(row=0, column=0)
                    z = Button(window_1, text="close", command=lambda: window_1.destroy())
                    z.grid(row=1, column=1)
                    click_1 = None
                else:
                    Label(window_1, text="Enter weight of the edge:").grid(row=0, column=0)
                    node = Entry(window_1)
                    node.grid(row=0, column=1)
                    z = Button(window_1, text="Enter",
                               command=lambda node=node, i=i, window=window_1: from_click_third(node, i, window))
                    z.grid(row=1, column=1)
                window_1.mainloop()
    if k:
        window = Tk()
        Label(window, text='Please click on node').grid(row=0, column=0)
        z = Button(window, text="close", command=lambda: window.destroy())
        z.grid(row=1, column=1)
        window.mainloop()


def third():
    window = Tk()
    if len(positions.keys()) < 2:
        Label(window, text='you have not entered minimum number of nodes').grid(row=0, column=0)
        z = Button(window, text="close", command=lambda: window.destroy())
        z.grid(row=1, column=1)
        window.mainloop()
    else:
        setposition(500, -365)
        pendown()
        fillcolor('Green')
        begin_fill()
        circle(15)
        end_fill()
        penup()
        setposition(493, -363)
        write('end')
        Label(window, text='Now enter for edges by clicking two nodes and hit green end').grid(row=0, column=0)
        z = Button(window, text="close", command=lambda: window.destroy())
        z.grid(row=1, column=0)
        onscreenclick(click_third)


def get(node, x, y, window2):
    global positions, graph
    node_name = str(node.get())
    window2.destroy()
    setposition(x, y)
    entry = 3
    for i in positions.keys():
        if i == node_name:
            entry = 1
            break
        else:
            entry = 3
    if entry == 1:
        frame_2 = Tk()
        Label(frame_2, text="Node already taken").grid(row=0, column=0)
        z = Button(frame_2, text="close", command=lambda: frame_2.destroy())
        z.grid(row=1, column=1)
    else:
        write(node_name)
        positions[node_name] = [x, y]
        graph[node_name] = {}


def click_second(x, y):
    global positions
    if 225 >= (500 - x) ** 2 + (-350 - y) ** 2:
        third()
    else:
        enter = True
        window_2 = Tk()
        for i in positions.keys():
            if 500 >= (positions[i][0] - x) ** 2 + (positions[i][1] - y) ** 2:
                enter = False
        if enter:
            Label(window_2, text="Enter node name:").grid(row=0, column=0)
            node = Entry(window_2)
            node.grid(row=0, column=1)
            z = Button(window_2, text="Enter",
                       command=lambda node=node, x=x, y=y, window_2=window_2: get(node, x, y, window_2))
            z.grid(row=1, column=1)
        else:
            Label(window_2, text="Entered position is near to the another node").grid(row=0, column=0)
            z = Button(window_2, text="Close", command=lambda: window_2.destroy())
            z.grid(row=1, column=1)


def second():
    Screen().setup(1200, 800)
    speed(0)
    penup()
    setposition(500, -365)
    pendown()
    fillcolor('red')
    begin_fill()
    circle(15)
    end_fill()
    penup()
    setposition(493, -363)
    write('end')
    onscreenclick(click_second)
    mainloop()


def first():
    window = Tk()
    Label(window, text="Right click for nodes to be inserted and then press end in the window").grid(row=0, column=0)
    z = Button(window, text="close", command=lambda: window.destroy())
    z.grid(row=1, column=0)
    window.mainloop()
    second()


click_1 = None
graph = {}
positions = {}
first()
