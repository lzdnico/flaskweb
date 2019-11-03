n = 5
flags= ['1','2','3','4','5']
lists = [[], ['V4 杭港 BGP PCCW原生本地 2倍'], ['V4 深港 BGP ALI商业广播 5倍', 'V4 深新 BGP Ali商业解锁 5倍', 'V4 沪港 BGP ALI商业广播 5倍', 'V4 沪新 BGP Ali商业解锁 5倍', 'V4 杭港 BGP ALI商业广播 5倍', 'V4 杭新 BGP Ali商业解锁 5倍', 'V4 京港 BGP ALI商业广播 5倍', 'V4 京新 BGP Ali商业解锁 5倍'], ['企业专线 深港 03 专线直连 10倍', '企业专线 深港 02 专线直连 10倍', '企业专线 深港 01 专线直连 10倍', '企业专线 沪港 03 专线直连 10倍', '企业专线 沪港 02 专线直连 10倍', '企业专线 沪港 01 专线直连 10倍']]
clashgroup = ''
clashname = ''
for i in range(len(lists)):
    if i == 0:
        continue
    print(lists[i])
    print(str(lists[i]))
    #clashgroup  += '- { name: "'+ str(lists[i]) + '", type: "select", "proxies": '  + '}\n'
    clashgroup  += '- name: "{name}", type: "select", "proxies": '.format(name=str(flags[i])) + str(lists[i]) + '}\n'
print(clashgroup)