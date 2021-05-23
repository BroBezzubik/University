from numpy.random import exponential, normal
from matplotlib import pyplot


def exp_by_intensity(params):
    return exponential(1 / params[0])


def norm_by_intensity(params):
    res = -1
    while res < 0:
        res = normal(1 / params[0], 1 / params[1])
    return res


class Generator:
    def __init__(self, func, params):
        self.law = func
        self.params = params

    def generation_time(self):
        return self.law(self.params)


class EventModel:
    def __init__(self, generators, processor, total_apps=0):
        self.generators = generators
        self.processor = processor
        self.total_apps = total_apps

    def proceed(self):
        processed = 0
        self.queue = []
        self.events = []
        self.totally_waited = 0
        i = 0
        for generator in self.generators:
            self.events.append([generator.generation_time(), 'g', i])
            i += 1
        self.free = True
        while processed < self.total_apps:
            event = self.events.pop(0)
            if event[1] == 'g':
                self._generate(event)
            elif event[1] == 'p':
                processed += 1
                self._process(event[0])

        return self.totally_waited

    def _add_event(self, event: list):
        i = 0
        while i < len(self.events) and self.events[i][0] < event[0]:
            i += 1
        self.events.insert(i, event)

    def _generate(self, event):
        self.queue.append(event[0])
        self._add_event([event[0] + self.generators[event[2]].generation_time(), 'g', event[2]])
        if self.free:
            self._process(event[0])

    def _process(self, time):
        if len(self.queue) > 0:
            processing_time = self.processor.generation_time()
            self.totally_waited += processing_time + time - self.queue.pop(0)
            self._add_event([time + processing_time, 'p'])
            self.free = False
        else:
            self.free = True


def view(total_apps, proc_dev):
    max_int = 100
    proc = Generator(exp_by_intensity, (max_int, proc_dev))
    Xdata = list()
    Ydata = list()

    for intensity in range(1, max_int + 1):
        gen = Generator(exp_by_intensity, (intensity,))
        model = EventModel([gen], proc, total_apps)
        Xdata.append(intensity / max_int)
        Ydata.append(model.proceed() / total_apps)

    pyplot.title('Average awaiting time')
    pyplot.grid(True)
    pyplot.plot(Xdata, Ydata)
    pyplot.xlabel("Strain (p)")
    pyplot.ylabel("Average time")
    pyplot.show()


if __name__ == "__main__":
    total_apps = int(input("Enter total apps amount: "))
    if total_apps < 1:
        print("Input error.\n")
        exit(1)

    proc_int = float(input("Enter processor intensity: "))
    proc_dev = float(input("Enter processor standard deviation: "))

    gen_amount = int(input("Enter generators amount: "))
    gens = []
    gen_int_sum = 0
    for i in range(gen_amount):
        gen_int = float(input("Enter generator intensity: "))
        gens.append(Generator(exp_by_intensity, (gen_int,)))
        gen_int_sum += gen_int

    proc = Generator(norm_by_intensity, (proc_int, proc_dev))
    model = EventModel(gens, proc, total_apps)

    time = model.proceed()
    print("Strain: p =", gen_int_sum / proc_int, "\nTotal awaiting time:", time, "\nAverage time: ", time / total_apps)

    view(total_apps, proc_dev)
