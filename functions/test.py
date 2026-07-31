from __init__ import chain, tap

def test_chain():
    assert chain.__doc__, 'Should have docs'

    ret = chain(
        1,
        lambda n: n + 1,
        lambda n: n ** 2,
        lambda n: n * 3,
    )
    assert ret == 12, f'{ret} != 12'

    func_chain = chain(
        lambda n: n + 1,
        lambda n: n ** 2,
        lambda n: n * 3,
    )
    ret = func_chain(1)
    assert ret == 12, '12'

def test_tap():
    assert tap.__doc__, 'Should have docs'

    ret = tap(lambda n: n + 1)(1)
    assert ret == 1, f'{ret} != 1'

    n = None
    def f(_n):
        nonlocal n
        n = _n

    ret = tap(f)(1)
    assert ret == 1, f'{ret} != 1'
    assert n == 1, f'{n} != 1'

def test():
    test_chain()
    test_tap()

if __name__ == '__main__':
    test()
