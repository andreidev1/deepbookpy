"""Parse response of asset type"""

def parse_struct(response):
        response = response.replace('0xdee9::clob_v2::Pool<', '').replace(">", '').split(',')
        return [el.strip() for el in response]