__author__ = 'stefan'


def add_value(m, value):
    m.extend(value)


if __name__ == '__main__':
    l = ['a']
    add_value(l, 'b')
    print str(l)
