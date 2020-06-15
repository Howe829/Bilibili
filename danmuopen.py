import gzip
from io import StringIO


with open('seg.so', 'r') as f:
    daa = f.read()

    data = StringIO(daa)
    gz = gzip.GzipFile(fileobj=data, mode='r')
    print(data.read())
    data.close()
