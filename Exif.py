import sys
from ExifParser import ParseExifData
from ExifTag import ExifTagInfomation

def display_message(exif_data, ifd):

    print('-------------------- {:s} --------------------'.format(ifd) )
    print('{:4s} IFD Offset = 0x{:08x}'.format(ifd, exif_data.get_offset(ifd)))
    print('{:4s} Tag Number = {:d}'.format(ifd, len(exif_data._exif_info[ifd])))
    
    for count in range(len(exif_data._exif_info[ifd])):
        print('{:s} : [{:s} len={:d}] 0x{:08x}'.format( \
                                                ExifTagInfomation().change_id_to_string(ifd, exif_data._exif_info[ifd][count]["id"]), \
                                                ExifTagInfomation().change_format_to_string(exif_data._exif_info[ifd][count]["type"]), \
                                                exif_data._exif_info[ifd][count]["len"], \
                                                exif_data._exif_info[ifd][count]["value"]))


def exif(argv):
    with open(argv[0], 'rb') as infile:
        data = infile.read()

    ifds = ["0th", "1st", "exif", "gps", "intr"]
    exif_data = ParseExifData()

    exif_data.check_exif_string(data)

    for ifd in ifds:
        if ifd == "0th":
            exif_data.parse_0th_ifd(data)
            display_message(exif_data, ifd)
        elif exif_data.get_offset(ifd) > 0:
            exif_data.parse_ifd(data, ifd)
            display_message(exif_data, ifd)


if __name__ == '__main__':
    exif(sys.argv[1:])
