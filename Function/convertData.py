def changeFormatDate(tanggal):
    tgl_list = tanggal.split('-')
    new_tangal = ''
    for idx, t in enumerate(tgl_list[::-1]):
        if idx != 0:
            new_tangal+= '/'
        new_tangal += t
    return new_tangal