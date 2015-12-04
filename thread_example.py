import threading


class PrimeNumber(threading.Thread):
    prime_numbers = {}
    lock = threading.Lock()

    def __init__(self, number):
        threading.Thread.__init__(self)
        self.Number = number
        PrimeNumber.lock.acquire()
        PrimeNumber.prime_numbers[number] = "None"
        PrimeNumber.lock.release()

    def run(self):
        counter = 2
        res = True
        steps = 1000
        while counter*counter < self.Number and res:
            if self.Number % counter == 0:
                res = False
                print(str(self.Number) + " is not prime, divisible by " + str(counter))
            counter += 1
            if counter % steps == 0:
                print(str(counter))
        PrimeNumber.lock.acquire()
        if res is True:
            print(str(self.Number) + " is prime")
        PrimeNumber.prime_numbers[self.Number] = res
        PrimeNumber.lock.release()
threads = []
while True:
    num_input = input("number: ")
    try:
        num_input = int(num_input)
    except ValueError:
        print("not int")
        break
    if num_input < 1:
        print("less than 1")
        break

    int_input = int(num_input)

    thread = PrimeNumber(int_input)
    threads += [thread]
    thread.start()

# for x in threads:
    # print(type(x))
    # x.join()
