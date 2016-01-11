def et():
    try:
        c = b + 1
    except:
        if Exception is NameError:
            print('Error')
        else:
            print(Exception)
            exc = dir(Exception)
            for e in exc:
                print(getattr(Exception, e))
                try:
                    print(getattr(Exception, e()))
                except:
                    print('no function')

# except TypeError:
#     print('TypeError')
# except NameError:
#     print('NE')


    # if Exception is TypeError:
    #     print('TypeError')
    # elif Exception is NameError:
    #     print('NE')