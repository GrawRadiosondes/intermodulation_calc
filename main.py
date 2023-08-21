import itertools

# Some fundamental explanation can be found at
# https://www.shure.com/en-US/performance-production/louder/all-about-wireless-intermodulation-distortion

frequencies = [400.11, 400.67, 401.09, 401.27, 401.67, 402.11, 402.49, 402.81, 403.17, 403.61, 403.99, 404.27, 404.61, 405.03, 405.31, 405.91]


threshold = 0.035 # minimum deviation to an intermodulation product needs to be 35 kHz

class IMProduct:
    def __init__(self, freq, parents, type):
        self.freq = freq
        self.parents = parents
        self.type = type

    def __str__(self):
        return '\n(Freq: ' + str(self.freq) + ', Parents: ' + str(self.parents) + ', Type: ' + self.type + ')'

    def __repr__(self):
        return str(self)

if __name__ == '__main__':
    combinations = list(itertools.combinations(frequencies, 2))
    im = []

    for combination in combinations:
        f1 = combination[0]
        f2 = combination[1]

        im.append(IMProduct(round(2 * f1 - f2, 3), [f1, f2], 'IM3'))
        im.append(IMProduct(round(2 * f2 - f1, 3), [f1, f2], 'IM3'))
        im.append(IMProduct(round(3 * f1 - 2 * f2, 3), [f1, f2], 'IM5'))
        im.append(IMProduct(round(3 * f2 - 2 * f1, 3), [f1, f2], 'IM5'))
        im.append(IMProduct(round(4 * f1 - 3 * f2, 3), [f1, f2], 'IM7'))
        im.append(IMProduct(round(4 * f2 - 3 * f1, 3), [f1, f2], 'IM7'))

    im.sort(key=lambda x: x.freq)

    # Print the combinations
    print('### Input Frequency List: ', frequencies)
    print('### Third-Order Intermodulation Products (IM3): ', [x for x in im if x.type == 'IM3'])
    print('### Fifth-Order Intermodulation Products (IM5): ', [x for x in im if x.type == 'IM5'])
    print('### Seventh-Order Intermodulation Products (IM7): ', [x for x in im if x.type == 'IM7'])

    def check_critical(freq, im):
        class CriticalIMProduct(IMProduct):
            def __init__(self, *args):
                if type(args[0]) is IMProduct:
                    self.__dict__ = args[0].__dict__.copy()
                    distance = args[1]
                    affected_freq = args[2]
                else:
                    super(CriticalIMProduct, self).__init__(*args[:3])
                    distance = args[3]
                    affected_freq = args[4]
                self.distance = distance
                self.affected_freq = affected_freq

            def __str__(self):
                return '\n(Freq: ' + str(self.freq) + \
                       ', Parents: ' + str(self.parents) + \
                       ', Type: ' + self.type + \
                       ', Distance: ' + str(self.distance) + \
                       ', Affected Frequency: ' + str(self.affected_freq) + ')'

        distance = round(abs(freq - im.freq), 3)
        if distance <= threshold:
            return CriticalIMProduct(im, distance, freq)
        else:
            return 0


    critical_im = [check_critical(freq, product) for freq in frequencies for product in im if check_critical(freq, product)]

    print('### Critical IM3: ', [x for x in critical_im if x.type == 'IM3'])
    print('### Critical IM5: ', [x for x in critical_im if x.type == 'IM5'])
    print('### Critical IM7: ', [x for x in critical_im if x.type == 'IM7'])