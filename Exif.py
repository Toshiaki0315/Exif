import sys
from ExifParser import ParseExifData as ped
from ExifTag import ExifTagInformation as eti
import unicodedata

ADJUST_LEFT  = 1
ADJUST_RIGHT = 2

def _adjust_string(pos:int, digit:int, message:str)->str:
    """文字列を左右どちらかに寄せる"""

    for character in message:
        if unicodedata.east_asian_width(character) in ('F', 'W', 'A'):
            digit -= 2
        else:
            digit -= 1

    if pos == ADJUST_LEFT:
        return message + ' ' * digit

    return ' ' * digit + message


def display_exif_info(exif_header:ped, read_jpeg_data:bytes, ifd:str)->None:
    """Exifの解析結果を表示する"""
    
    byte_order  = exif_header.exif_byte_order()
    base_offset = exif_header.exif_base_offset()
    exif_info_length = exif_header.exif_info_length(ifd)

    print('-------------------- {:s} --------------------'.format(ifd) )
    print('{:4s} IFD Offset = 0x{:08x}'.format(ifd, exif_header.ifd_offset(ifd)))
    print('{:4s} Tag Number = {:d}'.format(ifd, exif_info_length))
    
    for count in range(exif_info_length):
        
        exif_info = eti(ifd, byte_order, base_offset, exif_header.exif_info(ifd, count))

        print('{:s} : [{:s} len = {:6d}] (0x{:08x}) : {:s}'.format( \
                                                _adjust_string(ADJUST_LEFT, 30, exif_info.change_id_to_string()), \
                                                _adjust_string(ADJUST_LEFT, 10, exif_info.change_format_to_string()), \
                                                exif_info.exif_tag_length(), \
                                                exif_info.exif_tag_value(), \
                                                exif_info.change_tag_value_to_string(read_jpeg_data)))


def exif(argv:list)->None:
    """Exifの解析をおこなう"""

    with open(argv[0], 'rb') as infile:
        read_jpeg_data = infile.read()

    ifds = ["0th", "1st", "exif", "gps", "intr"]
    exif_header = ped(read_jpeg_data)

    if exif_header.check_exif_string() <= 0:
        print("not found exif header!")
        return
        
    for ifd in ifds:
        if ifd == "0th":
            exif_header.parse_0th_tag_info()
            display_exif_info(exif_header, read_jpeg_data, ifd)
        elif exif_header.ifd_offset(ifd) > 0:
            exif_header.parse_ifd_tag_info(ifd)
            display_exif_info(exif_header, read_jpeg_data, ifd)


if __name__ == '__main__':
    exif(sys.argv[1:])
