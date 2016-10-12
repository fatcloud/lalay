#! /usr/bin/env python3

# 這個函數會把 text 裡面的字用 cutter list 裡的字元切開，放進一個 list 以後回傳
def cut_into_pieces(text, cutter_list):

    tokens = []
    token = ""

    for char in text:
        if char not in cutter_list:
            token += char
        else:
            if token != "":
                tokens.append(token)
            token = ""
            tokens.append(char)

    if token != "":
        tokens.append(token)

    return tokens


# ========================= 任務一：處理空白和逗號 ============================
# 刪除所有夾雜在中文內的空白，並將逗號從小寫改大寫
# 這裡的作法是把整串字沿著所有的空白和逗號切開，並紀錄遇到該符號前到底讀到的是英文還是中文
# 背景文字 (context) 是中文的情況下才去做處理
def fix_space_and_comma(paragraph):

    tokens = cut_into_pieces(paragraph, [',', ' '])

    paragraph_out = ""
    context_is_chinese = False

    replacer = {' '  : '' ,     # 空白轉成無字元
                '\t' : '' ,     # tab 也轉成無字元
                ','  : '，'}    # 小寫逗點轉成大寫

    for token in tokens:
        # 以下視情況切換中英模式：都字母的話當然英文，Unicode 數字超過一萬八成是中文
        
        unicode_last_char = ord(token[-1:])
        if unicode_last_char in range(65,91) or unicode_last_char in range(97,123):
            context_is_chinese = False
        
        elif unicode_last_char > 10000:
            context_is_chinese = True
            
        elif context_is_chinese and token in replacer:
            # token 非中非英而是符號，而且背景是中文的情況下，把空白刪除，並且把小寫逗點換大寫
            token = replacer[token]
        
        # 把處理完的 token 接上 clean_paragraph
        paragraph_out += token

    return paragraph_out


# ====================== 任務二：見到中文標點符號就換行 ========================
# 補了一個小條件：一行要超過五個字
def newlines_on_delimiter(paragraph):

    delimiter = ['，', '。', '、']
    min_line_length = 5

    paragraph_out = ""
    line = ""

    tokens = cut_into_pieces(paragraph, delimiter)
    for token in tokens:
        line += token
        if token in delimiter and len(line) > min_line_length:
            paragraph_out = paragraph_out + line + '\n'
            line = ""

    return paragraph_out


# ====================== 任務三：取代所有的括弧 ========================

def fix_parentheses(paragraph):
    paragraph_out = ""
    
    replacer = { '(' : '\ (',
                 ')' : ')\ '}
    tokens = cut_into_pieces(paragraph, replacer.keys())
    for token in tokens:
        if token in replacer.keys():
            paragraph_out += replacer[token]
        else:
            paragraph_out += token

    return paragraph_out



# ================== beautify 就是把所有的任務執行一遍 ========================

def beautify(paragraph):
    # 任務一：中文間的空白以及逗點大小寫
    paragraph = fix_space_and_comma(paragraph)
    
    # 任務二：見到標點符號就分割成新的空行
    paragraph = newlines_on_delimiter(paragraph)
    
    # 任務三：把括弧取代掉
    paragraph = fix_parentheses(paragraph)
    
    return paragraph




# ============ 找出 directory 底下所有的 docx 檔，全部 beautify 並輸出 ==============

def process_all_docx(directory):

    import docx
    from os import listdir, getcwd

    # 在所在的資料夾裡尋找 docx 檔案名，也接受大寫 DOCX
    # 接著排除掉第一個字是 . 的檔案（通常是暫存的隱藏檔）
    all_docx_names = [f for f in listdir(directory) if f.lower()[-5:] == '.docx']
    docx_names     = [f for f in all_docx_names if f[0] is not '.']


    # 沒有找到要處理的檔案時回報錯誤
    if len(docx_names) == 0:
        print("No docx file is found at", getcwd())
        print("Please put your file here with me.")
        exit()


    # 正常開工
    for filename in docx_names:
        # 打開目標 docx 檔
        doc = docx.Document(filename)
        
        # 打開要寫入的檔案
        f = open(filename + ".txt", "w")
        
        # 讀取所有的段落
        for paragraph in doc.paragraphs:
            
            # 把每個段落都拿來美容
            p = beautify(paragraph.text)
            
            # 輸出一個空行，再把整個段落裡所有的文字都輸出到檔案裡
            print("", file=f)
            print(p, file=f)
                
        # 關閉輸出完成的檔案
        f.close()


    # 正常完工
    print("Process finished. Totally", len(docx_names), "files were processed")




if __name__ == '__main__':
    import sys

    input_directory = '.'
        
    process_all_docx(input_directory)

