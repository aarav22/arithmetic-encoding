import sys
from decimal import Decimal as d, getcontext
class ArithematicCoding:

    def __init__(self, filename):
        self.filename = filename
        self.cache = {}
        self.counter = 0

    
    
    def encode(self, msg):

        high, low = 1, 0
        bits = []
        for symbol in msg:
            current_range = high - low
            high = low + current_range * self.cdf[self.order[ord(symbol)]]
            low = low + current_range * self.cdf[self.order[ord(symbol)] - 1]
            high, low, bits = self.rescaling(high, low, bits)
        
        # print(high, low)
        self.bits = bits
        return high, low


    def decode(self, tag, prob, order):
        # print(self.cdf, tag)
        self.output = ''
        def getChar(i):
            for key, value in order.items():
                if value == i:
                    return chr(key)

        def decodeChar(tag, high, low): 
            while(len(tag) > 1):
                current_range = high - low
                for i in range(0, len(prob) - 1):
                    decimal = self.getDecimal(tag)
                    new_high  =   low + current_range * self.cdf[i + 1]
                    new_low   =   low + current_range * self.cdf[i]
                    # does it lie between low and high? if yes, then the symbol is i
                    if decimal >= new_low and decimal < new_high:
                        new_high, new_low, newtag = self.rescaling_decoding(new_high, new_low, tag)
                        self.output += getChar(i + 1)
                        # print(f'{i + 1}: {getChar(i + 1)}')
                        low, high, tag = new_low, new_high, newtag
                        break

        # get the decimal value of the tag
        decodeChar(tag, 1, 0)
        return self.output

    def start_encoding(self):
        self.init_frequencies()
        self.init_probabilities()
        self.init_cdf()
        high, low = self.encode(self.text)
        if 0.5 <= high < 1:
            self.bits.append(1)
        
        # append the bits to a binary string
        tag = ''.join([str(i) for i in self.bits])
        return tag, self.prob, self.order

    # helper functions

    def getDecimal(self, binary):
        # convert binary to decimal
        # convert tag to decimal value by multipling by 2^(-1)
        getcontext().prec=14000
        decimal = d(0)
        for i in range(1, len(binary) + 1):
            mult = d(2 ** (-i))
            mult_two = d(binary[i - 1])
            decimal += d(mult * mult_two)
        return decimal

    def rescaling_decoding(self, high, low, tag):
        counter = 0
        while not (high > 0.5 and low < 0.5):
            # clear output
            counter += 1
            if high <= 0.5 and low < 0.5:
                high = d(high*2)
                low = d(low*2)
            elif high > 0.5 and low >= 0.5:
                high = d((high * 2)  - 1)
                low = d((low  * 2)  - 1)
            # remove the first bit from the tag
            tag = tag[1:]
            # print(f'{counter}: {high} {low}')
        return high, low, tag

    def rescaling(self, high, low, bits):
        # print("rescaling")
        while not (high > 0.5 and low < 0.5):
            # clear output
            self.counter += 1
            if high <= 0.5 and low < 0.5:
                high = d(high*2)
                low = d(low*2)
                bits.append(0)
            elif high > 0.5 and low >= 0.5:
                high = d((high * 2)  - 1)
                low = d((low  * 2)  - 1)
                bits.append(1)
            # print(f'{self.counter}: ', high, low)

        return high, low, bits

    def init_cdf(self): 
        prob = self.prob
        # calculate CDF of each letter
        cdf = [0] * len(self.order)
        cdf[0] = d(prob[0])
        for i in range(1, len(self.order)):
            cdf[i] = d(prob[i] + cdf[i - 1])

        
        self.cdf = cdf

    def init_frequencies(self):
        # count letter frequency in the file
        with open(self.filename, 'r') as f:
            # read the file
            text = f.read()
            self.text = text

            # count the frequency of each letter
            freq = [0] * 257
            for c in text:
                c = ord(c)
                freq[c] += 1
                
            
            # copy all non-zero frequencies
            new_freq = [0]
            order = {}
            counter = 1
            order[0] = 0
            for i in range(0, 257):
                if freq[i] != 0:
                    new_freq.append(freq[i])
                    order[i] = counter
                    counter += 1
                    
            self.freq = new_freq
            self.order = order
    
    def init_probabilities(self):
        # calculate the probability of each letter
        getcontext().prec = 4000
        prob = [0] * len(self.order)
        for c in range(0, len(self.order)):
            prob[c] = d(self.freq[c] / len(self.text))

        self.prob = prob

    

def main(filename):
    if filename == None:
        print("Please provide a filename")
        return
    
    # create an instance of the class
    ac = ArithematicCoding(filename)
    tag, prob, order = ac.start_encoding()
    print(f'Encoded tag: {tag}')
    msg = ac.decode(tag, prob, order)
    print(f'Decoded message: {msg}')
        
    
    
    


# accept cmd line arguments
if __name__ == "__main__":
    # try:
        # accept a text file as input
        main(sys.argv[1])
    # except IndexError:
    #     main(None)
    # except Exception as e:
    #     print(e)