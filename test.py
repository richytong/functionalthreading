import time
from functionalthreading import Thread, partial, _, chain, tap, tmap

def test_Thread():
    assert Thread.__doc__, 'Should have docs.'

    def f(n):
        return n ** 2

    t = Thread(target=f, args=[3])
    t.start()
    t.join()
    assert t.result == 9, f't.result ({t.result}) != 9'

    def f(a, b, c):
        return a + b + c

    t = Thread(target=f, args=[1, 2, 3])
    t.start()
    t.join()
    assert t.result == 6, f't.result ({t.result}) != 6'

    t = Thread(target=f, kwargs={ 'a': 1, 'b': 2, 'c': 3 })
    t.start()
    t.join()
    assert t.result == 6, f't.result ({t.result}) != 6'

def test_partial_and__():
    assert partial.__doc__, 'Should have docs.'

    def f(a, b, c):
        return a + b + c

    g = partial(f, 1)
    h = partial(g, 2)
    ret = h(3)

    def f(a, b, c):
        return [a, b, c]

    g = partial(f, _, _, 3)
    h = partial(g, 1)
    ret = h(2)

    assert ret[0] == 1, f'ret[0] ({ret[0]}) != 1'
    assert ret[1] == 2, f'ret[1] ({ret[1]}) != 2'
    assert ret[2] == 3, f'ret[2] ({ret[2]}) != 3'

def test_chain():
    assert chain.__doc__, 'Should have docs.'

    ret = chain(
        1,
        lambda n: n + 1,
        lambda n: n ** 2,
        lambda n: n * 3,
    )
    assert ret == 12, f'({ret}) != 12'

    func_chain = chain(
        lambda n: n + 1,
        lambda n: n ** 2,
        lambda n: n * 3,
    )
    ret = func_chain(1)
    assert ret == 12, '12'

def test_tap():
    assert tap.__doc__, 'Should have docs.'

    ret = tap(lambda n: n + 1)(1)
    assert ret == 1, f'({ret}) != 1'

    n = None
    def f(_n):
        nonlocal n
        n = _n

    ret = tap(f)(1)
    assert ret == 1, f'ret ({ret}) != 1'
    assert n == 1, f'n ({n}) != 1'

def test_tmap():
    assert tmap.__doc__, 'Should have docs.'

    ret = tmap([1, 2, 3], lambda n: n ** 2)
    assert ret[0] == 1, f'ret[0] ({ret[0]}) != 1'
    assert ret[1] == 4, f'ret[1] ({ret[1]}) != 4'
    assert ret[2] == 9, f'ret[2] ({ret[2]}) != 9'

    mapping_func = tmap(lambda n: n ** 2)
    ret = mapping_func([1, 2, 3])
    assert ret[0] == 1, f'ret[0] ({ret[0]}) != 1'
    assert ret[1] == 4, f'ret[1] ({ret[1]}) != 4'
    assert ret[2] == 9, f'ret[2] ({ret[2]}) != 9'

    def f(n):
        time.sleep(1)
        return n + 1

    start = time.time()
    ret = tmap([1, 2, 3], f)
    end = time.time()

    assert ret[0] == 2, f'ret[0] ({ret[0]}) != 2'
    assert ret[1] == 3, f'ret[1] ({ret[1]}) != 3'
    assert ret[2] == 4, f'ret[2] ({ret[2]}) != 4'
    assert end - start < 1.1, 'Took too much time.'


def test():
    test_Thread()
    test_partial_and__()
    test_chain()
    test_tap()
    test_tmap()

if __name__ == '__main__':
    test()
