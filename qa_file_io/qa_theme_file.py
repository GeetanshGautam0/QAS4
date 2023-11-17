"""
FILE:           qa_file_io/qa_theme_file.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Quizzing Application Theme File Standard

DEFINES

    Type            Name                    [Inputs]                    [Outputs]                   [aliases]
    ---------------------------------------------------------------------------------------------------------
    (dataclass)     ThemeFile_s                                                                     Tf, theme file struct
    (dataclass)     Theme                                                                           Th
    (class)         ThemeFile                                                                       TF
    (method)        TF._read_header_        BytesIO object              HeaderData object

DEPENDENCIES

    hashlib
    os
    io  (BytesIO)
    qa_file_std
    qa_theme
    zlib


ERRORS

    Error Code                  Exception Type          Description
    ----------------------------------------------------------------------------------------------------------
    Read Header
    * 0x0000:0x0001             BadFileFormat           BadHeader error 1: Header absent/incomplete
    * 0x0000:0x0002             BadFileFormat           BadHeader error 2: Invalid magic bytes
    * 0x0000:0x0003             BadFileFormat           BadHeader error 3: Invalid/unsupported header version

    Read File
    * 0x0001:0x0001             AssertionError          Requested theme file not found.
    * 0x0001:0x0002             AssertionError          Invalid file version specified.
    * 0x0001:0x0003             AssertionError          Invalid header version for specified file version.
    * 0x0001:0x0004             AssertionError          Bad header (read.header_match_case or read.file_match_case)
    * 0x0001:0x0005             AssertionError          Bad header (struct).

    Generate File Data
    * 0x0011:0x0000             AssertionError          Bad theme header in theme struct (file header)
    * 0x0011:0x0001             AssertionError          Bad theme meta (theme author)
    * 0x0011:0x0002             AssertionError          Bad theme meta (theme author)
    * 0x0011:0x0003             AssertionError          Bad theme meta (theme name)
    * 0x0011:0x0004             AssertionError          Bad theme meta (theme name)
    * 0x0011:0x0005             AssertionError          Bad theme meta (theme collection name)
    * 0x0011:0x0006             AssertionError          Bad theme meta (theme collection name)
    * 0x0011:0x0007             AssertionError          Bad theme meta (no themes)

RELEVANT POLICIES
    * POLICY_FO_GEN_THEME_FILE_VERSION

"""

import os, io, json, zlib, hashlib, random
from typing import cast, List, Literal, Dict, Any
from qa_std import qa_def, qa_app_pol, locale
from dataclasses import dataclass
from . qa_file_std import (
    FileIO,
    FileType,
    BadFileFormat,
    HeaderData,
    Header,
    HeaderVersionOne,
    HeaderSection,
    GetMagicBytes
)


file_io_manager: FileIO


@dataclass
class Theme:
    # Meta
    theme_name: str  # "Light", "Dark", etc.
    theme_code: str  # An MD5 string and a CRC32 value for the theme + a random number (salt)

    # Theme Colors
    background: qa_def.HexColor
    foreground: qa_def.HexColor
    successful: qa_def.HexColor
    error:      qa_def.HexColor
    warning:    qa_def.HexColor
    accent:     qa_def.HexColor
    grey:       qa_def.HexColor

    # Theme Font
    title_font_face: str
    font_face: str
    font_size_title: int
    font_size_large: int
    font_size_normal: int
    font_size_small: int

    # Border Theme
    border_radius: int
    border_color: qa_def.HexColor


@dataclass
class ThemeFile_s:
    # Meta
    # Theme File Header
    header: HeaderData  # Standard q file header.
    author: str  # Author of the theme file.
    collection_name: str  # Default, Official Addons, etc.

    # Theme File
    file: qa_def.File  # Location of the theme file

    # Content
    themes: List[Theme]

    # V
    CHECKSUM: int
    SHA3_256: str


class ThemeFile:
    extension = 'qTheme'
    _allowed_header_versions = {
        1: (1, )
    }

    @staticmethod
    def _read_header_(fp: io.BytesIO) -> HeaderData:

        header_length = sum([section.SectionLength for section in cast(List[HeaderSection], Header.items) if 1 in section.HeaderVersion])
        header = fp.read(header_length)

        if len(header) != header_length:
            raise BadFileFormat('Theme', '0x0000:0x0001 Bad header (LEN).')

        # Read and test the magic bytes off the header
        magic_bytes = header[Header.MAGIC_BYTES.SectionStart:(Header.MAGIC_BYTES.SectionStart + Header.MAGIC_BYTES.SectionLength)]
        if magic_bytes != GetMagicBytes(FileType.Theme):
            raise BadFileFormat('Theme', '0x0000:0x0002 Bad header (MAG).')

        # Read version information off the header.
        version = header[Header.VERSION.SectionStart:(Header.VERSION.SectionStart + Header.VERSION.SectionLength)]
        version_int = int.from_bytes(version, Header.byteorder)

        # Read the header version off the header
        header_version = header[
                         Header.HEADER_VERSION.SectionStart:(
                                 Header.HEADER_VERSION.SectionStart + Header.HEADER_VERSION.SectionLength
                         )]
        header_version_int = int.from_bytes(header_version, cast(Literal["big", "little"], Header.byteorder))

        match header_version_int:
            case 1:
                # Return a version one compliant header
                return HeaderVersionOne(
                    magic_bytes,
                    version, version_int,
                    header_version, header_version_int,
                    FileType.Theme
                )

            case _:
                raise BadFileFormat('Theme', f'0x0000:0x0003 Bad header (VER; {header_version_int})')

    @staticmethod
    def _read_version_one_file_(file: qa_def.File, theme_file: Dict[str, Any]) -> ThemeFile_s:
        assert 'meta' in theme_file
        assert 'content' in theme_file
        assert 'v' in theme_file

        v = theme_file.pop('v')
        meta, content = theme_file['meta'], theme_file['content']

        assert isinstance(v, dict)
        assert len(theme_file) == 2
        assert (len(meta) == 4) & (len(content) > 0)
        assert isinstance(meta, dict) & isinstance(content, dict)

        m_and_c = json.dumps(theme_file).encode()
        checksum = zlib.crc32(m_and_c)
        sha3_256 = hashlib.sha3_256(m_and_c).hexdigest()

        del theme_file, m_and_c
        assert (v['Theme.CRC32'] == checksum) & (v['Theme.HASH'] == sha3_256)

        file_version = meta["ThemeFile.FileVersion"]
        header_version = meta["ThemeFile.HeaderVersion"]
        author = meta["Theme.Author"]
        collection = meta["Theme.Collection"]

        assert isinstance(file_version, int) & isinstance(header_version, int) & \
               isinstance(author, str) & isinstance(collection, str)

        assert (file_version == 1) & (header_version in ThemeFile._allowed_header_versions[file_version])

        author, collection = author.strip(), collection.strip()
        assert bool(len(author)) & bool(len(collection))

        themes: List[Theme] = []

        for theme_name, theme in content.items():
            assert isinstance(theme_name, str)
            theme_name = theme_name.strip()
            assert len(theme_name)

            BG = qa_def.HexColor(theme["Theme.BG"])
            FG = qa_def.HexColor(theme["Theme.FG"])
            ER = qa_def.HexColor(theme["Theme.ER"])
            WA = qa_def.HexColor(theme["Theme.WA"])
            OK = qa_def.HexColor(theme["Theme.OK"])
            AC = qa_def.HexColor(theme["Theme.AC"])
            GR = qa_def.HexColor(theme["Theme.GR"])
            TTL_FF = theme["Theme.Font"]["Theme.Font.TTL_FF"]
            FF = theme["Theme.Font"]["Theme.Font.FF"]
            TTL_FS = theme["Theme.Font"]["Theme.Font.TTL_FS"]
            LRG_FS = theme["Theme.Font"]["Theme.Font.LRG_FS"]
            NRM_FS = theme["Theme.Font"]["Theme.Font.NRM_FS"]
            SML_FS = theme["Theme.Font"]["Theme.Font.SML_FS"]
            BC = qa_def.HexColor(theme["Theme.Border"]["Theme.Border.Color"])
            BR = theme["Theme.Border"]["Theme.Border.Radius"]

            # An MD5 string and a CRC32 value for the theme + a random number (salt)
            t_str = json.dumps(theme)
            t_crc = zlib.crc32(t_str.encode())
            t_md5 = hashlib.md5(t_str.encode()).hexdigest()
            t_rnd = random.randint(100_000_000, 999_999_999) % random.randint(10, 20)

            theme_code = f'{t_md5}{t_crc}{t_rnd}'
            del t_str, t_crc, t_md5, t_rnd

            assert isinstance(TTL_FF, str) & isinstance(FF, str) & isinstance(TTL_FS, int) & \
                   isinstance(LRG_FS, int) & isinstance(NRM_FS, int) & isinstance(SML_FS, int) & \
                   isinstance(BR, int)

            themes.append(
                Theme(
                    theme_name, theme_code, BG, FG, OK, ER, WA, AC, GR, TTL_FF, FF, TTL_FS, LRG_FS, NRM_FS, SML_FS,
                    BR, BC
                )
            )

        header = HeaderVersionOne(
            GetMagicBytes(FileType.Theme),
            (1).to_bytes(Header.VERSION.SectionLength, Header.byteorder), 1,
            (1).to_bytes(Header.HEADER_VERSION.SectionLength, Header.byteorder), 1,
            FileType.Theme
        )

        return ThemeFile_s(header, author, collection, file, themes, checksum, sha3_256)

    @staticmethod
    def read_file(file: qa_def.File) -> ThemeFile_s:
        """
        Read Theme File

        :param file:    Source file
        :return:        Theme information
        """

        # 1) Read the file
        assert os.path.isfile(file.file_path), '0x0001:0x0001'

        with open(file.file_path, 'rb') as f_in:
            fp = io.BytesIO(f_in.read())
            f_in.close()

        # 2) Read the header. fp then only contains the theme data (JSON)
        header = ThemeFile._read_header_(fp)
        body = fp.read()

        # 3) Basic checks
        header_version = header.HEADER_VERSION_INT
        file_version = header.VERSION_INT

        assert file_version in ThemeFile._allowed_header_versions.keys(), '0x0001:0x0002 Bad file version'
        assert header_version in ThemeFile._allowed_header_versions[file_version], '0x0001:0x0003 Bad header'

        match header_version:
            case 1:
                assert isinstance(header, HeaderVersionOne), '0x0001:0x0005 Bad header'

            case _:
                raise Exception('0x0001:0x0004 Bad header')

        # 4) Read the json data
        theme = json.loads(body.decode(locale.get_locale().encoding))

        # 5) Convert the theme data to an appropriate Theme struct
        match file_version:
            case 1:
                return ThemeFile._read_version_one_file_(file, theme)

            case _:
                raise Exception('0x0001:0x0004 Bad header')

    @staticmethod
    def _create_version_one_header_() -> bytes:
        # Create a bytearray of the correct length
        header_length = sum([section.SectionLength for section in Header.items if 1 in section.HeaderVersion])
        output = bytearray()
        output += b'\x00' * header_length

        output[Header.MAGIC_BYTES.SectionStart:(Header.MAGIC_BYTES.SectionStart+Header.MAGIC_BYTES.SectionLength)] = \
            GetMagicBytes(FileType.Theme)

        output[
            Header.HEADER_VERSION.SectionStart:(Header.HEADER_VERSION.SectionStart + Header.HEADER_VERSION.SectionLength)
        ] = (1).to_bytes(Header.HEADER_VERSION.SectionLength, Header.byteorder)

        output[
            Header.VERSION.SectionStart:(Header.VERSION.SectionStart + Header.VERSION.SectionLength)
        ] = (1).to_bytes(Header.VERSION.SectionLength, Header.byteorder)

        return bytes(output)

    @staticmethod
    def _gen_version_one_file_(theme_file: ThemeFile_s) -> bytes:
        # Create new HeaderData
        #   Version one theme files only support version one headers.
        #       1) Magic Bytes
        #       2) Header Version
        #       3) File Version

        magic_bytes = GetMagicBytes(FileType.Theme)
        header_version = (1).to_bytes(Header.HEADER_VERSION.SectionLength, Header.byteorder)
        file_version = (1).to_bytes(Header.VERSION.SectionLength, Header.byteorder)

        assert HeaderData(magic_bytes, file_version, 1, header_version, 1, FileType.Theme) == theme_file.header, \
            '0x0011:0x0000 Bad theme'

        assert isinstance(theme_file.author, str), '0x0011:0x0001 Bad theme'
        theme_file.author = theme_file.author.strip()
        assert len(theme_file.author), '0x0011:0x0002 Bad theme'

        for theme in theme_file.themes:
            assert isinstance(theme, Theme), '0x0011:0x0007 Bad theme'
            assert isinstance(theme.theme_name, str) & isinstance(theme.theme_code, str), '0x0011:0x0005 Bad theme'
            theme.theme_name = theme.theme_name.strip()
            theme.theme_code = theme.theme_code.strip()
            assert (len(theme.theme_name) > 0) and (len(theme.theme_code) > 0), '0x0011:0x0006 Bad theme'

        assert isinstance(theme_file.collection_name, str), '0x0011:0x0005 Bad theme'
        theme_file.collection_name = theme_file.collection_name.strip()
        assert len(theme_file.collection_name), '0x0011:0x0006 Bad theme'

        assert len(theme_file.themes), '0x0011:0x0007 Bad theme'

        output = {
            "meta":
                {
                    "ThemeFile.FileVersion":                1,
                    "ThemeFile.HeaderVersion":              1,
                    "Theme.Author":                         theme_file.author,
                    "Theme.Collection":                     theme_file.collection_name
                },
            "content":
                {
                    theme.theme_name:
                        {
                            "Theme.BG":                     theme.background.color,
                            "Theme.FG":                     theme.foreground.color,
                            "Theme.ER":                     theme.error.color,
                            "Theme.WA":                     theme.warning.color,
                            "Theme.OK":                     theme.successful.color,
                            "Theme.AC":                     theme.accent.color,
                            "Theme.GR":                     theme.grey.color,
                            "Theme.Font":
                                {
                                    "Theme.Font.TTL_FF":    theme.title_font_face,
                                    "Theme.Font.FF":        theme.font_face,
                                    "Theme.Font.TTL_FS":    theme.font_size_title,
                                    "Theme.Font.LRG_FS":    theme.font_size_large,
                                    "Theme.Font.NRM_FS":    theme.font_size_normal,
                                    "Theme.Font.SML_FS":    theme.font_size_small
                                },
                            "Theme.Border":
                                {
                                    "Theme.Border.Color":   theme.border_color.color,
                                    "Theme.Border.Radius":  theme.border_radius
                                }
                        }
                    for theme in theme_file.themes if isinstance(theme, Theme)
                }
        }

        assert len(output['content']), '0x0011:0x0007 Bad theme'

        # Generate checksum and hash values
        m_and_c = json.dumps(output).encode()
        checksum = zlib.crc32(m_and_c)
        sha3_256 = hashlib.sha3_256(m_and_c).hexdigest()

        del m_and_c

        output['v'] = {
            'Theme.CRC32': checksum,
            'Theme.HASH': sha3_256
        }

        # Add a version one header and return the output as JSON
        return ThemeFile._create_version_one_header_() + json.dumps(output, indent=4).encode()

    @staticmethod
    def generate_file_data(theme_file: ThemeFile_s) -> bytes:
        match qa_app_pol.POLICY_FO_GEN_THEME_FILE_VERSION:
            case 1:
                return ThemeFile._gen_version_one_file_(theme_file)

            case _:
                raise Exception('Invalid theme file version requested.')

