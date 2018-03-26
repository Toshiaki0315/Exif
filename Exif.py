import sys
from ExifParser import AnalyzeExifData
from ExifTag import ExifTagInfomation

def display_tag_number(tag_number, ifd):
    print('{:4s} Tag Number = {:d}'.format(ifd, tag_number))

def display_message(tag_info, ifd):
    print('{:s} : [{:s} len={:d}] 0x{:08x}'.format( \
                                                ExifTagInfomation().change_id_to_string(ifd, tag_info[0]), \
                                                ExifTagInfomation().change_format_to_string(tag_info[1]), \
                                                tag_info[2], \
                                                tag_info[3]))

def get_0th_ifd(exif_data, data):

    exif_data.get_0th_offset(data)

    tag_number = get_ifd(exif_data, data, "0th")

    exif_data.get_1st_ifd_offset(data, tag_number)
    
    return
    
def get_ifd(exif_data, data, ifd):
    tag_number = exif_data.get_tag_number(data, ifd)
    display_tag_number(tag_number, ifd)

    for count in range(tag_number):
        tag_info = exif_data.get_tag_info(data, ifd, count)
        display_message(tag_info, ifd)
    
    return tag_number

def exif(argv):
    ifds = ["1st", "exif", "gps", "intr"]
    exif_data = AnalyzeExifData()

    with open(argv[0], 'rb') as infile:
        data = infile.read()

    exif_data.check_exif_string(data)

    get_0th_ifd(exif_data, data)
    for ifd in ifds:
        if exif_data.get_offset(ifd) > 0:
            print('{:4s} IFD Offset = 0x{:08x}'.format(ifd, exif_data.get_offset(ifd)))
            get_ifd(exif_data, data, ifd)
if __name__ == '__main__':
    exif(sys.argv[1:])