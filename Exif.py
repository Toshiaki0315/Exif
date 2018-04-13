import sys
from ExifParser import ParseExifData as ped
from ExifTag import ExifTagInformation as eti
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

def display_message(exif_header, read_jpeg_data, ifd):
    
    byte_order  = exif_header.exif_byte_order()
    base_offset = exif_header.exif_base_offset()
    exif_info_length = exif_header.exif_info_length(ifd)

    print('-------------------- {:s} --------------------'.format(ifd) )
    print('{:4s} IFD Offset = 0x{:08x}'.format(ifd, exif_header.ifd_offset(ifd)))
    print('{:4s} Tag Number = {:d}'.format(ifd, exif_info_length))
    
    for count in range(exif_info_length):
        
        exif_info = eti(ifd, byte_order, base_offset, exif_header.exif_info(ifd, count))

        print('{:s} : [{:s} len = {:6d}] (0x{:08x}) : {:s}'.format( \
                                                adjust_message(ADJUST_LEFT, 30, exif_info.change_id_to_string()), \
                                                adjust_message(ADJUST_LEFT, 10, exif_info.change_format_to_string()), \
                                                exif_info.exif_tag_length(), \
                                                exif_info.exif_tag_value(), \
                                                exif_info.change_value(read_jpeg_data)))


def exif(argv):
    with open(argv[0], 'rb') as infile:
        read_jpeg_data = infile.read()

    ifds = ["0th", "1st", "exif", "gps", "intr"]
    exif_header = ped(read_jpeg_data)

    exif_header.check_exif_string()

    for ifd in ifds:
        if ifd == "0th":
            exif_header.parse_0th_tag_info()
            display_message(exif_header, read_jpeg_data, ifd)
        elif exif_header.ifd_offset(ifd) > 0:
            exif_header.parse_ifd_tag_info(ifd)
            display_message(exif_header, read_jpeg_data, ifd)


if __name__ == '__main__':
    exif(sys.argv[1:])
