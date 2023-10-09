import qa_inc as fnc


if __name__ == "__main__":
    fnc.error_management.ErrorStruct(fnc.error_management.ErrorType.UnspecifiedError, 823, True)
    locale = fnc.locale.get_locale()
    print(f'{locale}')
    cfa = fnc.dtc.CFA()
    o = fnc.dtc.convert(str, {0: 1, 1: 2, 2: 3, 3: 4}, cfa=cfa)
    o = fnc.dtc.convert(bytes, o, cfa=cfa)
    print(o)
    o1 = fnc.dtc.convert(dict, o, cfa=cfa)
    print(o1)
