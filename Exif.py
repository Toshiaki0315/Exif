import sys
from ExifParser import ParseExifData
from ExifTag import ExifTagInformation
import unicodedata

ADJUST_LEFT  = 1
ADJUST_RIGHT = 2

def adjust_message(pos, digit, message):
    for character in message:
        if unicodedata.east_asian_width(character) in ('F', 'W', 'A'):
            digit -= 2
        else:
            digit -= 1

    if pos == ADJUST_LEFT:
        return message + ' ' * digit

    return ' ' * digit + message

def display_message(exif_data, data, ifd):

    print('-------------------- {:s} --------------------'.format(ifd) )
    print('{:4s} IFD Offset = 0x{:08x}'.format(ifd, exif_data.get_offset(ifd)))
    print('{:4s} Tag Number = {:d}'.format(ifd, len(exif_data._exif_info[ifd])))
    
    for count in range(len(exif_data._exif_info[ifd])):
        
        exif_info = ExifTagInformation(ifd, exif_data._exif_info[ifd][count])
        value = exif_info.change_value( data, exif_data._base_offset)

        print('{:s} : [{:s} len = {:6d}] (0x{:08x}) : {:s}'.format( \
                                                adjust_message(ADJUST_LEFT, 30, exif_info.change_id_to_string()), \
                                                adjust_message(ADJUST_LEFT, 10, exif_info.change_format_to_string()), \
                                                exif_info.exif_tag_length(), \
                                                exif_info.exif_tag_value(), \
                                                value))


def exif(argv):
    with open(argv[0], 'rb') as infile:
        data = infile.read()

    ifds = ["0th", "1st", "exif", "gps", "intr"]
    exif_data = ParseExifData(data)

    exif_data.check_exif_string()

    for ifd in ifds:
        if ifd == "0th":
            exif_data.parse_0th_ifd()
            display_message(exif_data, data, ifd)
        elif exif_data.get_offset(ifd) > 0:
            exif_data.parse_ifd(ifd)
            display_message(exif_data, data, ifd)


if __name__ == '__main__':
    exif(sys.argv[1:])
