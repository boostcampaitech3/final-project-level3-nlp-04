# TODO: inference.py에서 출력하는 정보를 list로 저장해서 필요한 정보만을 출력하기

# 'B-DAT', 'B-DUR', 'B-LOC', 'B-MNY', 'B-NOH', 'B-ORG', 'B-PER', 'B-PNT', 'B-POH', 'B-TIM'
# 'I-DAT', 'I-DUR', 'I-LOC', 'I-MNY', 'I-NOH', 'I-ORG', 'I-PER', 'I-PNT', 'I-POH', 'I-TIM'
# 'O'

# 이 중에서 우리가 사용할만한 정보 1) PER(인물), 기관(ORG), 지명(LOC)

def extract_info(texts, tags):

    end_point = len(texts)
    flag = 'O'
    # info_dict = {'LOC': [], 'PER': [], 'ORG': []}
    info_dict = {'LOC': [], 'PER': [], 'ORG': [], 'DAT': [], 'DUR': [], 'MNY': [], 'NOH': [], 'PNT': [], 'POH': [], 'TIM': [], 'O': []}

    box = []
    concat = False

    for i, (text, tag) in enumerate(zip(texts, tags)):
        if i == end_point - 1:
            if box:
                info_dict[flag].append(''.join(box).replace('##', ''))
                pass

        if tag[0] == 'B':
            if concat:
                box.append(text)
            else:
                box = [text]
            continue

        elif tag[0] == 'I':
            if text == '_':
                box.append(' ')
            else:
                box.append(text)
            flag = tag[-3:]

        elif tag[0] == 'O':
            if box:
                if tags[i + 1][-3:] != flag:
                    if flag == 'O':
                        continue
                    info_dict[flag].append(''.join(box).replace('##', ''))
                    box = []
                    concat = False
                else:
                    box.append(" ")
                    concat = True

            else:
                continue

    return info_dict        


def extract_info2(texts, tags):
    
    flag = 'O'
    info_dict = {'LOC': [], 'PER': [], 'ORG': [], 'DAT': [], 'DUR': [], 'MNY': [], 'NOH': [], 'PNT': [], 'POH': [], 'TIM': [], 'O': []}
    box = []
    for text, tag in zip(texts, tags):

        if tag[0] == 'B':
            box = [text]
            continue

        elif tag[0] == 'I':
            box.append(text)
            flag = tag[-3:]
            
        elif tag[0] == 'O':
            if box:
                info_dict[flag].append(''.join[box].replace('##', ''))
                print(box)
                box = []
            else:
                continue
    
    return info_dict
