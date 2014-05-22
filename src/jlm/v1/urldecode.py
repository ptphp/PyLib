import urllib

def urldecode(query):
    d = {}
    a = query.split('&')
    for s in a:
        if s.find('='):
            k, v = map(urllib.unquote, s.split('='))
            try:
                d[k].append(v)
            except KeyError:
                d[k] = v

    return d

if __name__ == '__main__':
    str = """title=name&taxonomy_catalog%5Bund%5D%5B%5D=177&field_vendor%5Bund%5D=8&field_description_1%5Bund%5D%5B0%5D%5Bvalue%5D=Description_1&changed=&form_build_id=form-CB0hbTiWtWxditpjJ061qW7TWsWqMWUFNXz4YKJg3dw&form_token=L5bpClXSTkbmOECOPZLjBdJsI2hUL2C0miY5a0_bHHU&form_id=product_node_form&field_description_2%5Bund%5D%5B0%5D%5Bvalue%5D=Description_1&model=sku&list_price=0&cost=0&sell_price=0&shippable=1&weight=0&weight_units=lb&dim_length=0&dim_width=0&dim_height=0&length_units=in&pkg_qty=1&ordering=0&gc_salable=1&shipping_type=&shipping_address%5Bfirst_name%5D=&shipping_address%5Blast_name%5D=&shipping_address%5Bcompany%5D=&shipping_address%5Bstreet1%5D=&shipping_address%5Bstreet2%5D=&shipping_address%5Bcity%5D=&shipping_address%5Bzone%5D=0&shipping_address%5Bcountry%5D=840&shipping_address%5Bpostal_code%5D=&shipping_address%5Bphone%5D=&usps%5Bcontainer%5D=VARIABLE&ups%5Bpkg_type%5D=02&menu%5Blink_title%5D=&menu%5Bdescription%5D=&menu%5Bparent%5D=main-menu%3A0&menu%5Bweight%5D=0&log=&path%5Balias%5D=&comment=2&name=logic&date=&status=1&promote=1&additional_settings__active_tab=edit-base&op=Save"""
    #print urldecode(str)["cityinfo"][0].decode("utf-8").encode("gb2312")
    #print urldecode(str)["button"][0].decode("utf-8").encode("gb2312")
    dict = urldecode(str)
    print dict
    for row in dict:
        print dict['row']
        
