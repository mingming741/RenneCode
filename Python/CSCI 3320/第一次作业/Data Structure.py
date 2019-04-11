def tupleDes():
    print("Tuple - (): done dimensional, fixed-length, unchanged sequence, for record things")
    print("tuple format is: ")
    tup = 1,"emm",3
    print(tup)

    print("tuple add: ")
    tup1 = 1,3
    tup2 = 2,'a'
    print(tup1 + tup2)
    print("tuple multipul: ")
    tup0 = 'haha','emm'
    print(tup1 * 3)

    print("tuple index: ")
    tup0 = 1, 'haha','emm', 4, "oh", 6, 'sb', "haha"
    print(len(tup0))
    print(tup0.index("oh"))
    print(tup0.count("haha"))
    return


def listDes():
    print("List - []: variable-length sequence, changed contented, for variable")
    print("list format is: ")
    list = ["emm", 0, None, 2, 'Showing', 123, "Showing", ["sub1", "sub2", 233, ['subsub1', "subsub2"]], (1,3, 4, 234)]
    print(list)
    list[1] = 'hhhhh'
    list.append('YY')

    print("list remove is: ")
    list.remove('emm')
    print(list)
    print(list.index('YY'))
    return

#listDes();

def dictDes():
    print("Dictionary - {}: flexibly-sized , store key-value pairs")
    print("format is: ")
    d1 = {'name' : 'Showing', "age": 12, "sID" : 12345, 000 : 'haha', "friends" : ["Kalu", 'Wan', 23, "?"] }
    print(d1)
    return

def setDes():
    print("Set - {}: order collection unique elements（即重复的会去除）")
    print("format is: ")
    s1 = set([2,3,3,2,1,1,1,1])
    print(s1)
    return