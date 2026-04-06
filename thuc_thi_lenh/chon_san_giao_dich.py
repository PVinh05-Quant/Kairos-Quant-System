from utils.doc_cau_hinh import lay_cau_hinh_giao_dich

def chon_san_tot_nhat(symbol):

    config = lay_cau_hinh_giao_dich()
    uu_tien = config.get('san_giao_dich_chinh', 'binance')
    return uu_tien