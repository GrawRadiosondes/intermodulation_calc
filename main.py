# https://www.shure.com/en-US/performance-production/louder/all-about-wireless-intermodulation-distortion
import itertools

#frequencies = [400.01, 400.13, 400.25, 400.37, 400.49, 400.63, 400.75, 400.89]
# frequencies = [400.36, 400.48, 400.63, 400.75, 400.89]
#frequencies = [400.5, 401.0, 401.5]
# frequencies = [400.48, 400.63]

# rogue sondes were on 400.63 and 400.49

# first start was on 400.01, 400.13 and 400.25

# was 400.37 already in the air?

#400.69 400.81

#frequencies = [400.01, 400.05, 400.21, 400.25, 400.57, 400.77, 405.29, 405.67, 404.01, 401.73, 404.95, 401.39]
#frequencies = [400.03, 400.11, 400.23, 400.31, 400.67, 400.97, 405.29, 405.67]

frequencies = [400.250, 400.625, 401.00, 401.375, 401.75, 402.125, 402.5, 402.875, 403.25, 403.625, 404.0, 404.375, 404.75, 405.125, 405.5, 405.875]


threshold = 0.035

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
        #im3.append(round(2 * f1 - f2, 3))
        #im3.append(round(2 * f2 - f1, 3))
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