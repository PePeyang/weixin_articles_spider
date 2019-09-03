
"""
1. 出错return原样
2. general_msg_list不是字符串return 原样
3. list无内容return原样
4. 成功有内容的return load_list
"""
def list_parse(load_res_dict):
    # print(type(load_res_dict['general_msg_list']))
    load_list = {
        'list': []
    }
    if not load_res_dict['ret'] == 0:
        print('- 访问出错了，应该是cookie过期')
        return load_list
    elif load_res_dict['can_msg_continue'] != 1:
        print('- 不能再获取了，应该是后面没有了')
        return load_list
    else:
        load_list = eval(load_res_dict['general_msg_list'])
        return load_list

"""
return list
具体结构见items/list_items2.json

TODO 存入biz 公众号名字 发表时间
"""
def list_into_dbdata(obj, enname, chname):
    list_lo = obj['list']
    list_db = list()
    if not isinstance(list_lo, list):
        print('list_lo 不是list类型， 前面一步转错了')
        print(list_lo)
        return None
    else:
        pass

    if len(list_lo) > 0:
        for big_li in list_lo:
            big_item = {}
            big_item['is_multi_app_msg_item_list'] = 'NO'
            # 可能没有app_msg_ext_info
            if 'app_msg_ext_info' in big_li.keys():
                print('有app_msg_ext_info')
                big_item['enname'] = enname
                big_item['chname'] = chname
                for b_key, b_value in big_li['app_msg_ext_info'].items():

                    if b_key == 'content_url' or b_key == 'cover' or b_key == 'source_url':
                        big_item[b_key] = b_value.replace('\\', '')
                    # elif (b_key == 'multi_app_msg_item_list') and (len(b_value) > 0):
                    #     for small_li in b_value:
                    #         # print(small_li)
                    #         small_item = {}
                    #         small_item['is_multi_app_msg_item_list'] = 'YES'
                    #         for s_key, s_value in small_li.items():
                    #             if s_key == 'content_url' or s_key == 'cover' or s_key == 'source_url':
                    #                 s_value = s_value.replace('\\', '')
                    #             small_item[s_key] = s_value
                    #         list_db.append(small_item)
                    elif b_key == 'multi_app_msg_item_list' or b_key == 'digest' or b_key == 'author' or b_key == 'title':
                        big_item[b_key] = b_value

                list_db.append(big_item)
        print(len(list_db))
        return list_db
    else:
        print('list_lo list为空')
        print(list_lo)
        return None
