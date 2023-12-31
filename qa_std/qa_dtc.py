"""
FILE:           qa_std/qa_dtc.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing application data type convertor.

DEFINES

    (method)    public; Any         convert
    (class)     public; data class  CFA
    ...         private methods

DEPENDENCIES

    typing.*
    sys.stderr                  [alias: stderr]
    dataclasses.dataclass       [alias: dataclass]
    qa_std.locale               [alias: locale]

"""

from sys import stderr
from typing import *
from . import locale
from dataclasses import dataclass


@dataclass
class CFA:
    list_delim: str = ', '
    dict_kv_delim: str = ': '
    dict_entry_delim: str = ', '

    aggregate_to_numerical_conversion: int = 0
    '''
        aggregate_to_numerical_conversions
        
        Determines how "FLOAT" and "INT" treat list, tuple, set, and dict values.
        0:  Counter             Returns the number of items in the struct
        1:  Additive            List, Tuples, and Sets: adds the values of the struct (automatically converted to floats)
                                Dict: keys --> float then added
        2:  Additive            l, t, and s: same as 1
                                d: values --> float then added
        3: Additive             l, t, and s: same as 
                                d: keys --> float and values --> float then added.
    '''


"""
The Basics:

Data types, at least the ones we're interested in, can be classified as one of the following:
1)  Default aggregate 
2)  Default non-aggregate 
3)  Custom

"Default aggregate" refers to any such data types that can contain more than one value. 
    Rev. A1 of the convertor deals with the following:
    i.      Tuple
    ii.     List
    iii.    Set
    iv.     Dictionary
    
"Default non-aggregate" refers to any such default data type that are not covered by the above.
    Rev. A1 of the convertor deal with the following:
    i.      String
    ii.     Bytes
    iii.    Integer
    iv.     Float
    v.      Complex
    vi.     Boolean
    
"Custom" refers to any data types defined by the quizzing application system.

SPEC:
    Each of the above data types, except "Custom types", should be able to convert to any other type.
    Custom data types may only convert to a select few default data types.

"""

# Accepted data types
DNA = (str, bytes, int, float, complex, bool)   # Def non-aggregate
DA = (list, tuple, set, dict)                   # Def aggregate
CUSTOM = ()                                     # Custom

# Default aggregate


class ConvertToDefaultType:
    def __init__(
            self,
            output_type: type,
            data_type: type,
            supported_output_type: type,
            supported_data_types: Tuple[Type[Any], ...],
            *args: Any,
            **kwargs: Any
    ) -> None:
        """
        Parent class for default type convertors

        :param output_type:                 Output data type
        :param data_type:                   Input data type
        :param supported_output_type:       Intended output type (checked whether default type)
        :param supported_data_types:        Supported data types for input data
        :param args:                        Other arguments
        :param kwargs:                      Other keyword arguments

        :keyword cfa:                       Convertor function args struct.
                                            If none is provided, then a struct with default values
                                            will be created automatically.

        """

        assert supported_output_type in (*DNA, *DA)
        assert data_type in supported_data_types, '0x100000'
        assert output_type is supported_output_type, '0x100001'

        self.encoding = cast(str, locale.get_locale().encoding)

        self.cfa = kwargs.get('cfa')
        if not isinstance(self.cfa, CFA):
            self.cfa = CFA()

    def _reload_encoding_(self, *_: Any, **__: Any) -> None:
        self.encoding = cast(str, locale.get_locale().encoding)


class LIST(ConvertToDefaultType):
    supported_types: Tuple[Type[Any], ...] = (*DNA, *DA)

    def __init__(self, output_type: type, data: Any, *args: Any, **kwargs: Any) -> None:
        ConvertToDefaultType.__init__(self, output_type, type(data), list, self.supported_types, *args, **kwargs)
        self.ot, self.d = output_type, data

    def go(self) -> List[Any]:
        return {
                str: self._str,
                bytes: self._bytes,
                bool: self._bool,
                int: self._int,
                float: self._float,
                complex: self._complex,
                set: self._set,
                tuple: self._tuple,
                dict: self._dict
            }[type(self.d)]()

    def _str(self) -> List[Any]:
        return cast(str, self.d).split(cast(CFA, self.cfa).list_delim)

    def _bytes(self) -> List[Any]:
        return cast(bytes, self.d).split(cast(CFA, self.cfa).list_delim.encode(self.encoding))

    def _bool(self) -> List[Any]:
        return [] if cast(bool, self.d) else [1]

    def _int(self) -> List[Any]:
        return [self.d]

    def _float(self) -> List[Any]:
        return [self.d]

    def _complex(self) -> List[Any]:
        return [cast(complex, self.d).real, cast(complex, self.d).imag]

    def _set(self) -> List[Any]:
        return [*cast(Set[Any], self.d)]

    def _tuple(self) -> List[Any]:
        return [*cast(Tuple[Any], self.d)]

    def _dict(self) -> List[Any]:
        return [
            f'{convert(str, k, cfa=self.cfa)}{cast(CFA, self.cfa).dict_kv_delim}{convert(str, v, cfa=self.cfa)}'
            for k, v in cast(Dict[Any, Any], self.d).items()
        ]


class TUPLE(ConvertToDefaultType):
    supported_types: Tuple[Type[Any], ...] = (*DNA, *DA)

    def __init__(self, output_type: type, data: Any, *args: Any, **kwargs: Any) -> None:
        ConvertToDefaultType.__init__(self, output_type, type(data), tuple, self.supported_types, *args, **kwargs)
        self.ot, self.d = output_type, data

    def go(self) -> Tuple[Any, ...]:
        return (*convert(list, self.d, cfa=self.cfa),)


class SET(ConvertToDefaultType):
    supported_types: Tuple[Type[Any], ...] = (*DNA, *DA)

    def __init__(self, output_type: type, data: Any, *args: Any, **kwargs: Any) -> None:
        ConvertToDefaultType.__init__(self, output_type, type(data), set, self.supported_types, *args, **kwargs)
        self.ot, self.d = output_type, data

    def go(self) -> Set[Any]:
        return {*convert(list, self.d, cfa=self.cfa),}


class DICT(ConvertToDefaultType):
    supported_types: Tuple[Type[Any], ...] = (*DNA, *DA)

    def __init__(self, output_type: type, data: Any, *args: Any, **kwargs: Any) -> None:
        ConvertToDefaultType.__init__(self, output_type, type(data), dict, self.supported_types, *args, **kwargs)
        self.ot, self.d = output_type, data

    def go(self) -> Dict[Any, Any]:
        return cast(
            Dict[Any, Any],
            {  # type: ignore
                str: self._str,
                bytes: self._bytes,
                bool: self._bool,
                int: self._int,
                float: self._float,
                complex: self._complex,
                list: self._list,
                tuple: self._tuple,
                set: self._set
            }[type(self.d)]()
        )

    def _str(self) -> Dict[Any, Any]:
        self.d = cast(str, self.d).strip()

        if self.d[0] == '{':
            assert len(self.d) >= 2
            self.d = self.d[1::]

        if self.d[-1] == '}':
            assert len(self.d) >= 2
            self.d = self.d[:-1]

        e = self.d.split(cast(CFA, self.cfa).dict_entry_delim)
        o = {}

        for entry in e:
            k = entry.split(cast(CFA, self.cfa).dict_kv_delim)[0].strip(cast(CFA, self.cfa).dict_kv_delim).strip()
            v = entry.replace(k, '', 1).strip(cast(CFA, self.cfa).dict_kv_delim).strip()

            o[k] = v

        return o

    def _bytes(self) -> Dict[Any, Any]:
        self.d = cast(bytes, self.d).strip()

        if self.d[0] in ('{'.encode(self.encoding), ord('{'.encode(self.encoding))):
            assert len(self.d) >= 2
            self.d = self.d[1::]

        if self.d[-1] == ('}'.encode(self.encoding), ord('}'.encode(self.encoding))):
            assert len(self.d) >= 2
            self.d = self.d[:-1]

        e = self.d.split(cast(CFA, self.cfa).dict_entry_delim.encode(self.encoding))
        o = {}

        for entry in e:
            k = entry.split(cast(CFA, self.cfa).dict_kv_delim.encode(self.encoding))[0].strip(
                cast(CFA, self.cfa).dict_kv_delim.encode(self.encoding)).strip()
            v = entry.replace(k, ''.encode(self.encoding), 1).strip(
                cast(CFA, self.cfa).dict_kv_delim.encode(self.encoding)).strip()

            o[k] = v

        return o

    def _bool(self) -> Dict[Any, Any]:
        return {} if not self.d else {1: True}

    def _int(self) -> Dict[Any, Any]:
        return {0: self.d}

    def _float(self) -> Dict[Any, Any]:
        return {0: self.d}

    def _complex(self) -> Dict[Any, Any]:
        return {
            'real': cast(complex, self.d).real,
            'imaginary': cast(complex, self.d).imag
        }

    def _set(self) -> Dict[Any, Any]:
        return self._list([*cast(Set[Any], self.d)])

    def _tuple(self) -> Dict[Any, Any]:
        return self._list([*cast(Tuple[Any, ...], self.d)])

    def _list(self, d: Optional[List[Any]]) -> Dict[Any, Any]:
        data = d if isinstance(d, list) else cast(List[Any], self.d)
        o = {}

        for e in data:
            tp = type(e)
            ep = convert(str, e, cfa=self.cfa)

            k = ep.split(cast(CFA, self.cfa).dict_kv_delim)[0]
            v = ep.replace(k, '', 1)

            o[k] = convert(tp, v, cfa=self.cfa)

        return o


# Default non-aggregate

class STRING(ConvertToDefaultType):
    supported_types: Tuple[Type[Any], ...] = (*DNA, *DA)

    def __init__(self, output_type: type, data: Any, *args: Any, **kwargs: Any) -> None:
        ConvertToDefaultType.__init__(self, output_type, type(data), str, self.supported_types, *args, **kwargs)
        self.ot, self.d = output_type, data
        self._reload_encoding_()

    def go(self) -> str:
        return cast(bytes, convert(bytes, self.d, cfa=self.cfa)).decode(self.encoding)


class INTEGER(ConvertToDefaultType):
    supported_types: Tuple[Type[Any], ...] = (*DNA, *DA)

    def __init__(self, output_type: type, data: Any, *args: Any, **kwargs: Any) -> None:
        ConvertToDefaultType.__init__(self, output_type, type(data), int, self.supported_types, *args, **kwargs)
        self.ot, self.d = output_type, data

    def go(self) -> int:
        return int(convert(float, self.d, cfa=self.cfa))


class FLOAT(ConvertToDefaultType):
    supported_types: Tuple[Type[Any], ...] = (*DNA, *DA)

    def __init__(self, output_type: type, data: Any, *args: Any, **kwargs: Any) -> None:
        ConvertToDefaultType.__init__(self, output_type, type(data), float, self.supported_types, *args, **kwargs)
        self.ot, self.d = output_type, data

    def go(self) -> float:
        return cast(
            float,
            {  # type: ignore
                str: self._str,
                bytes: self._bytes,
                int: self._int,
                complex: self._complex,
                bool: self._bool,
                list: self._list,
                tuple: self._tuple,
                set: self._set,
                dict: self._dict
            }[type(self.d)]()
        )

    def _str(self) -> float:
        return float(self.d)

    def _bytes(self) -> float:
        return float(cast(bytes, self.d).decode(self.encoding))

    def _int(self) -> float:
        return cast(float, self.d)

    def _complex(self) -> float:
        return float(cast(complex, self.d).real)

    def _list(self, d: Optional[List[Any]] = None) -> float:
        if isinstance(d, list):
            data = d

        else:
            data = cast(List[Any], self.d)

        match cast(CFA, self.cfa).aggregate_to_numerical_conversion:
            case 0:
                # Length
                return len(data)  # type: ignore

            case 1:
                return sum([convert(int, e, cfa=cast(CFA, self.cfa)) for e in data])  # type: ignore

            case 2:
                return sum([convert(int, e, cfa=cast(CFA, self.cfa)) for e in data])  # type: ignore

            case 3:
                return sum([convert(int, e, cfa=cast(CFA, self.cfa)) for e in data])  # type: ignore

            case _:
                stderr.write(f'[WARNING] [QA-DTC] [AGGREGATE --> NUMERICAL] Invalid value for ANC var. Default to 0\n')
                cast(CFA, self.cfa).aggregate_to_numerical_conversion = 0
                return self._list(data)

    def _tuple(self) -> float:
        return self._list(d=[*self.d])

    def _set(self) -> float:
        return self._list(d=[*self.d])

    def _dict(self) -> float:
        match cast(CFA, self.cfa).aggregate_to_numerical_conversion:
            case 0:
                return len(self.d)  # type: ignore

            case 1:
                return sum([convert(float, e, cfa=self.cfa) for e in self.d.keys()])  # type: ignore

            case 2:
                return sum([convert(float, e, cfa=self.cfa) for e in self.d.values()])  # type: ignore

            case 3:
                return sum(  # type: ignore
                    [convert(float, k, cfa=self.cfa) + convert(float, v, cfa=self.cfa) for k, v in self.d.items()]
                )

            case _:
                stderr.write(f'[WARNING] [QA-DTC] [DICT --> NUMERICAL] Invalid value for ANC var. Default to 0\n')
                cast(CFA, self.cfa).aggregate_to_numerical_conversion = 0
                return self._dict()

    def _bool(self) -> float:
        return float(self.d)


class COMPLEX(ConvertToDefaultType):
    supported_types: Tuple[Type[Any], ...] = (*DNA, *DA)

    def __init__(self, output_type: type, data: Any, *args: Any, **kwargs: Any) -> None:
        ConvertToDefaultType.__init__(self, output_type, type(data), complex, self.supported_types, *args, **kwargs)
        self.ot, self.d = output_type, data

    def go(self) -> complex:
        """
        DTC - To complex

            STRING:     if in complex format, str -> complex
                        else len(str) -> real
            BYTES:      bytes.decode --> str comprehension
            INT:        int -> real
            FLOAT:      float -> real
            BOOLEAN:    real: 1 if True else real: 0
            LIST:       if list.len = 2 then real: l[0] imag: l[1]
                        else list.len -> real
            TUPLE:      same as list
            SET:        same as list
            DICT:       if real or imaginary in dict: real: d.real, imag: d.imaginary
                        else len(dict) -> real

        :return: complex
        """
        return complex({  # type: ignore
            str: self._str,
            bytes: self._bytes,
            int: self._int,
            float: self._float,
            bool: self._bool,
            list: self._list,
            tuple: self._tuple,
            set: self._set,
            dict: self._dict
        }[type(self.d)](self.d))

    @staticmethod
    def _str(d: str) -> complex:
        try:
            return complex(d)

        except ValueError as e:
            return complex(len(d), 0)

    def _bytes(self, d: bytes) -> complex: return COMPLEX._str(d.decode(self.encoding))

    @staticmethod
    def _int(d: int) -> complex: return complex(d, 0)

    @staticmethod
    def _float(d: float) -> complex: return complex(d, 0)

    @staticmethod
    def _bool(d: bool) -> complex: return complex(1 if d else 0, 0)

    @staticmethod
    def _list(d: List[Any]) -> complex:
        if 0 < len(d) <= 2:
            return complex(*d)

        else:
            return complex(len(d), 0)

    @staticmethod
    def _tuple(d: Tuple[Any, ...]) -> complex: return COMPLEX._list(cast(List[Any], d))

    @staticmethod
    def _set(d: Set[Any]) -> complex: return COMPLEX._list(cast(List[Any], d))

    @staticmethod
    def _dict(d: Dict[Any, Any]) -> complex:
        if 'real' in d or 'imag' in d:
            return complex(d.get('real', 0), d.get('imaginary', 0))

        else:
            return complex(len(d), 0)


class BYTES(ConvertToDefaultType):
    supported_types: Tuple[Type[Any], ...] = (*DNA, *DA)

    def __init__(self, output_type: type, data: Any, *args: Any, **kwargs: Any) -> None:
        ConvertToDefaultType.__init__(self, output_type, type(data), bytes, self.supported_types, *args, **kwargs)
        self._reload_encoding_()
        self.ot, self.d = output_type, data

    def go(self) -> bytes:
        return cast(
            bytes,
            {  # type: ignore
                str: self._str,
                int: self._int,
                float: self._float,
                complex: self._complex,
                list: self._list,
                tuple: self._tuple,
                dict: self._dict,
                bool: self._bool,
                set: self._set
            }[type(self.d)]()
        )

    def _str(self) -> bytes: return cast(str, self.d).encode(self.encoding)

    def _int(self) -> bytes: return f'{self.d}'.encode(self.encoding)

    def _float(self) -> bytes: return f'{self.d}'.encode(self.encoding)

    def _complex(self) -> bytes:
        return f'({cast(complex, self.d).real}+{cast(complex, self.d).imag}j)'.encode(self.encoding)

    def _bool(self) -> bytes: return ('True' if self.d else 'False').encode(self.encoding)

    def _list(self, d: Optional[List[Any]] = None, paren: str = '[]') -> bytes:
        o: bytes = paren[0].encode(self.encoding)
        l = self.d if not isinstance(d, list) else d

        for i, el in enumerate(cast(List[Any], l)):
            o += convert(bytes, el, cfa=self.cfa)

            if i != len(l) - 1:
                o += cast(CFA, self.cfa).list_delim.encode(self.encoding)

        o += paren[1].encode(self.encoding)
        return o

    def _tuple(self) -> bytes: return self._list([*self.d], '()')

    def _set(self) -> bytes: return self._list([*self.d], '{}')

    def _dict(self) -> bytes:
        o: bytes = '{'.encode(self.encoding)

        for i, (k, v) in enumerate(cast(Dict[Any, Any], self.d).items()):
            o += convert(bytes, k, cfa=self.cfa)
            o += cast(CFA, self.cfa).dict_kv_delim.encode(self.encoding)
            o += convert(bytes, v, cfa=self.cfa)

            if i != len(self.d) - 1:
                o += cast(CFA, self.cfa).dict_entry_delim.encode(self.encoding)

        o += '}'.encode(self.encoding)

        return o


class BOOLEAN(ConvertToDefaultType):
    supported_types: Tuple[Type[Any], ...] = (*DNA, *DA)

    def __init__(self, output_type: type, data: Any, *args: Any, **kwargs: Any) -> None:
        ConvertToDefaultType.__init__(self, output_type, type(data), bool, self.supported_types, *args, **kwargs)
        self.ot, self.d = output_type, data

    def go(self) -> bool:
        """
        DTC - To boolean

            STRING:     'Tt' in str and 'Ff' not in str
            BYTES:      'Tt' in bytes and 'Ff' not in bytes
            INT:        calls bool(int)
            FLOAT:      calls bool(float)
            COMPLEX:    calls bool(complex.real, complex.imag)
            LIST:       True if len(list) else False
            TUPLE:      True if len(tuple) else False
            SET:        True if len(set) else False
            DICT:       True if len(dict) else False

        :return: (bool)True or (bool)False
        """
        return bool({  # type: ignore
            str: self._str,
            bytes: self._bytes,
            int: self._int,
            float: self._float,
            complex: self._complex,
            list: self._list,
            tuple: self._tuple,
            set: self._set,
            dict: self._dict
        }[type(self.d)](self.d))

    @staticmethod
    def _str(d: str) -> bool: return ('t' in d.lower()) and not ('f' in d.lower())

    @staticmethod
    def _bytes(d: bytes) -> bool: return (b't' in d.lower()) and not (b'f' in d.lower())

    @staticmethod
    def _int(d: int) -> bool: return bool(d)

    @staticmethod
    def _float(d: float) -> bool: return bool(d)

    @staticmethod
    def _complex(d: complex) -> bool: return bool(d.real + d.imag)

    @staticmethod
    def _list(d: List[Any]) -> bool: return BOOLEAN._int(len(d))

    @staticmethod
    def _tuple(d: Tuple[Any, ...]) -> bool: return BOOLEAN._int(len(d))

    @staticmethod
    def _set(d: Set[Any]) -> bool: return BOOLEAN._int(len(d))

    @staticmethod
    def _dict(d: Dict[Any, Any]) -> bool: return BOOLEAN._int(len(d))


def convert(output_type: type, data: Any, *args: Any, **kwargs: Any) -> Any:
    """
    Quizzing App Data Type Convertor (Public Fn.)

    :param output_type: Desired output type
    :param data:        Data to be converted
    :param args:        Additional args to be passed onto the convertor
    :param kwargs:      Additions keyword args to be passed onto the convertor

    :keyword cfa:       CFA struct
                        if none is provided, a new struct containing default CFA values will be generated automatically.

    :return:            data --> <output_type>

    Errors:
    *   0x000001        Original data's data type was not recognized.
    *   0x000002        Output data type not supported (global check)
    *
    *   0x100000        Output data type not supported (local check)
    *   0x100001        0x000001.DTC.TypeMappingError

    """

    # If the data is already of the correct type, then do not waste time running any of the following code.
    if isinstance(data, output_type):  # type: ignore
        return data

    assert isinstance(data, (*DNA, *DA, *CUSTOM)),          f'0x000001 {type(data)}'
    assert output_type in (*DNA, *DA, *CUSTOM),             f'0x000002 {output_type}'

    # Call the function
    return cast(Dict[type, Any], {
        str: STRING,
        int: INTEGER,
        float: FLOAT,
        complex: COMPLEX,
        bytes: BYTES,
        bool: BOOLEAN,
        list: LIST,
        tuple: TUPLE,
        dict: DICT,
        set: SET
    })[output_type](output_type, data, *args, **kwargs).go()
