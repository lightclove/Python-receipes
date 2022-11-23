from pprint import pprint

memo = dict()
# data = dict()
result = list()
for line in open('lsusb_-t_source.txt', 'r'):
    line = line.replace('\n', '').split(' ')
    try:
        if line[0] == '/:':
            memo['bus'] = line[1].split('=')[1]
            indent = 0
            dev_dict = False
        else:
            memo['previous_indent'] = indent
            memo['previous_device'] = dev_dict
            indent = line.index('|__')
            dev_dict = {'device': line[indent + 1].split('=')[1],
                        'class': line[indent + 2].split('=')[1],
                        'bus': memo['bus']}
            if 'hub' in dev_dict['class'].lower():
                dev_dict['input'] = list()
            if not memo['previous_device']:
                # data[memo['bus']] = [dev_dict]
                result.append(dev_dict)
            else:
                if indent > memo['previous_indent']:
                    memo[memo['previous_indent']] = memo['previous_device']
                    memo['previous_device']['input'].append(dev_dict)
                else:
                    if indent - 4 == 0:
                        # data[memo['bus']].append(dev_dict)
                        result.append(dev_dict)
                    else:
                        memo[indent - 4]['input'].append(dev_dict)
    except Exception as e:
        print(e)

# pprint(memo)
pprint(result)
