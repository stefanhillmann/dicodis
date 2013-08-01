from measures import jensenDistance


def test_jensen_distance():
    p = [0.1, 0.2, 0.2, 0.5]
    q = p
    
    d = jensenDistance(p, q)
    
    if d != 0:
        print 'test_jensenDistance() FAILED: Test distance must be 0.0 but was {}.'.format(d)
    else:
        print 'test_jensenDistance() SUCCEEDED.'
        
test_jensen_distance()