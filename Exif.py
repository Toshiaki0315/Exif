import sys
from ExifParser import AnalyzeExifData
from ExifTag import ExifTagInfomation

def display_tag_number(exif_data, ifd):
    print('{:4s} Tag Number = {:d}'.format(ifd, len(exif_data._exif_info[ifd])))


def display_message(exif_data, ifd):
    
    print(exif_data._exif_info[ifd][0])
    print(len(exif_data._exif_info[ifd]))
    print(type(exif_data._exif_info[ifd][0]))
    print(exif_data._exif_info[ifd][0].keys())
    print(type(exif_data._exif_info[ifd][0].keys()))
#    print(ExifTagInfomation().change_id_to_string(ifd, exif_data._exif_info[ifd][0].keys()))
    for count in range(len(exif_data._exif_info[ifd])):
        print(exif_data._exif_info[ifd][count])
#        print(change_id_to_string(ifd, exif_info.key))
 #       print('{:s} : [{:s} len={:d}] 0x{:08x}'.format( \
 #                                               ExifTagInfomation().change_id_to_string(ifd, exif_info), \
 #                                               ExifTagInfomation().change_format_to_string(exif_info[exif_info][count]["Type"]), \
 #                                               exif_info[exif_info][count]["Len"], \
 #                                               exif_info[exif_info][count]["value"]))


def get_0th_ifd(exif_data, data):

    exif_data.get_0th_offset(data)

    tag_number = get_ifd(exif_data, data, "0th")

    exif_data.get_1st_ifd_offset(data, tag_number)
    
    return


def get_ifd(exif_data, data, ifd):
    tag_number = exif_data.get_tag_number(data, ifd)

    for count in range(tag_number):
        tag_info = exif_data.get_tag_info(data, ifd, count)
    
    display_tag_number(exif_data, ifd)
    display_message(exif_data, ifd)

    return tag_number


def exif(argv):
    with open(argv[0], 'rb') as infile:
        data = infile.read()

    ifds = ["1st", "exif", "gps", "intr"]
    exif_data = AnalyzeExifData()

    exif_data.check_exif_string(data)

    get_0th_ifd(exif_data, data)
    for ifd in ifds:
        if exif_data.get_offset(ifd) > 0:
            print('{:4s} IFD Offset = 0x{:08x}'.format(ifd, exif_data.get_offset(ifd)))
            get_ifd(exif_data, data, ifd)


if __name__ == '__main__':
    exif(sys.argv[1:])