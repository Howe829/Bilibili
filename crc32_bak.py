import math

CRC32_POLY = 0xEDB88320

def unsigned32(n):
    return n & 0xffffffff
class Crc32Engine:
    @staticmethod
    def initCrc32Table(table):
        for i in range(0, 256):
            currCrc = i
            for l in range(8):
                if currCrc & 1:
                    currCrc = (currCrc >> 1) ^ CRC32_POLY
                else:
                    currCrc >>= 1
            table[i] = currCrc& 0xFFFFFFFF
    def __init__(self):

        self.crc32Table = [0 for i in range(256)]#UN
        Crc32Engine.initCrc32Table(self.crc32Table)

        self.rainbowTableHash = [0 for i in range(100000)]
        self.rainbowTableValue = [0 for i in range(100000)]
        self.fullHashCache = [0 for i in range(100000)]
        self.shortHashBuckets = [0 for i in range(65537)]
        for i in range(100000):
            hasc = self.compute(i) >> 0
            self.fullHashCache[i] = hasc &0xFFFFFFFF
            self.shortHashBuckets[hasc >> 16] += 1
        self.runningSum = 0

        def f(x):
            self.runningSum += x
            return self.runningSum
        self.shortHashBucketStarts = list(map(f, self.shortHashBuckets))
        for i in range(100000):
            self.shortHashBucketStarts[self.fullHashCache[i] >> 16] -= 1
            idx = self.shortHashBucketStarts[self.fullHashCache[i] >> 16]
            self.rainbowTableValue[idx] = i
            self.rainbowTableHash[idx] = self.fullHashCache[i]


    def compute(self, input, addPadding=False):
        currCrc = 0
        for d in str(input):
            currCrc = self.crc32Update(currCrc, int(d))
        if addPadding:
            for i in range(5):
                currCrc = self.crc32Update(currCrc, 0)
        return currCrc& 0xFFFFFFFF

    def crc32Update(self, currCrc, code):
        return ((currCrc >> 8) ^ self.crc32Table[(currCrc ^ code) & 0xFF])&0xFFFFFFFF

    def lookup(self, h):
        h >>= 0
        h = h&0xFFFFFFFF
        candidates = []
        shortHash = h >> 16
        for i in range(self.shortHashBucketStarts[shortHash], self.shortHashBucketStarts[shortHash + 1]):
            if self.rainbowTableHash[i] == h:
                print(self.rainbowTableHash[i], h)

                candidates.append(self.rainbowTableValue[i])
        return candidates

    def crack(self, hasc):
        candidates = []
        hashVal = ~int('0x' + hasc, 16) >> 0
        basHash = 0xFFFFFFFF

        for digitCount in range(1, 10):
            basHash = self.crc32Update(basHash, 0x30)
            if digitCount < 6:
                candidates += self.lookup(hashVal ^ basHash)
            else:
                startPrefix = math.pow(10, digitCount - 6)
                endPrefix = math.pow(10, digitCount - 5)

                for prefix in range(int(startPrefix), int(endPrefix)):
                    for postfix in self.lookup(hashVal ^ basHash ^ self.compute(prefix, True)):
                        candidates.append(prefix * 100000 + postfix)

        return candidates


if __name__ == '__main__':
    crc32 = Crc32Engine()
    print(crc32.crack('88462c9a'))
