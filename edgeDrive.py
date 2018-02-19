z = []

x = [1, 2]
y = [3, 4]

x_edge = True
y_edge = True


class DataStream:
    def __init__(self, stream):
        self.stream = stream
        self.place = 0
        self.top = True

    def step(self):
        self.place += 1
        if self.top:
            self.top = False
        else:
            self.top = True

    def current(self):
        return self.stream[self.place]

    def __repr__(self):
        return str(self.stream[self.place]) + ' : ' + str(self.top)


x1 = DataStream(x)
y1 = DataStream(y)






for i in range(2):
    if x1.top and y1.top:
        low = min(x1.current(), y1.current())
        z.append(low)
        if low == x1.current():
            x1.step()
        if low == y1.current():
            y1.step()
    elif not (x1.top and y1.top):
        high = max(x1.current(), y1.current())
        z.append(high)
        if high == x1.current():
            x1.step()
        if high == y1.current():
            y1.step()
    elif x1.top or y1.top:
        if not x1.top:
            z.append(x1.current())
            x1.step()
        if not y1.top:
            z.append(y1.current())
            y1.step()


print(z)