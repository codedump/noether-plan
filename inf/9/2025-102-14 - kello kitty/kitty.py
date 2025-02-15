cat = "Kitty"

jinkies = 7

def sum(a, b):
    '''
    Adds two numbers and returns sum.
    '''
    return a+b+jinkies


##
## Testing module
##

if __name__ == "__main__":

    print(f'Testing module now... my name is {__name__}')
    assert sum(5, 2)==14
    if not (sum(5, 2)==14):
        raise RuntimeError()
