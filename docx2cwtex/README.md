# Docx to cwTex

## 概述

process_all_docx.py 這支程式目前的功能是

1. 讀取 docx 檔中的文字，拿掉中文間多餘的空格、小寫逗點換大寫逗點、遇到標點符號就換行

2. 將 「()」 取代為 「\ ()\ 」，也就是 \+空格+( )+\+空格

只要把待處理的 docx 檔直接丟進 docx2cwtex 這個資料夾，然後執行

    python process_all_docx.py

它就會自動處理所有檔名為 xxx.docx 的文件，並且把輸出結果存在 xxx.docx.txt 裡



## 環境

這支程式是在 python 3.5 的環境下撰寫及測試，
其執行依賴 python-docx 這個套件，
此套件可以透過 pip 工具安裝：

    python -m pip install python-docx

如果沒有 pip 可以先用 easy_install 安裝 pip

    python -m easy_install pip



