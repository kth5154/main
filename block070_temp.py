import sys
import PyQt5.QtWidgets as qtwid
from PyQt5.QtGui import QIcon
import subprocess as sb
import wmi
import os, signal
import time
import win32gui, win32process, psutil
from pywinauto import findwindows
from pywinauto import application
import pyautogui
import concurrent.futures
from functools import partial
from PyQt5.QtCore import *

blockratio ='50%'
num070 = ''

# 작업 전 기존 log 파일 삭제
def del_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

# 기존 프로그램 종료
def ps_kill(process_name):
    ps = findwindows.find_elements()
    for ps_name in ps :
        if str(ps_name).find(process_name) > 0 :
            os.kill(ps_name.process_id,signal.SIGINT) 
            time.sleep(2)   

def find_dest():
    read_log = 'D:\call_block.txt'
    with open(read_log, 'r', encoding='UTF-8') as f :
        while True:
            read_lines = f.readline()
            if not read_lines:
                break
            read_lines = read_lines.strip()
            new_line = read_lines.split(' ')
            for i in range(len(new_line)):
                if new_line[i] == '(DEST':
                    temp_str= str(new_line[i+1])
                    temp_str= temp_str.replace(')','')
                    #print(temp_str)
                    return temp_str
                    break

def find_ofrt(DEST):
    read_log = 'D:\call_block.txt'
    with open(read_log, 'r', encoding='UTF-8') as f :
        while True:
            read_lines = f.readline()
            if not read_lines:
                break
            read_lines = read_lines.strip()
            new_line = read_lines.split(' ')
            for i in range(len(new_line)):
                #print(i, new_line[i])
                if new_line[i] == 'ALL070' and new_line[i+1] == DEST and len(new_line) > 3 :
                    temp_str = str(new_line[i+4])
                    temp_str = temp_str.replace(')','')
                    #print(new_line[i+3], temp_str)
                    return str(new_line[i+3]), str(temp_str)
                    break
                
def CHK_SSW(OFR_DEST):
    read_log = 'D:\call_block.txt'
    #print(OFR_DEST)
    with open(read_log, 'r', encoding='UTF-8') as f :
        while True:
            read_lines = f.readline()
            if not read_lines:
                break
            read_lines = read_lines.strip()
            new_line = read_lines.split(' ')
            for i in range(len(new_line)):
                if new_line[0] == OFR_DEST and len(new_line) > 4 :
                    temp_str = str(new_line[3])
                    temp_str1 = str(new_line[0])
                    temp_str2 = str(new_line[1])
                    if temp_str.find('ABX2') > 0: 
                        return 'ABX2'
                        break
                    elif temp_str.find('ABX3') > 0: 
                        return 'ABX3'
                        break
                    elif temp_str.find('ABX4') > 0: 
                        return 'ABX4'
                        break
                    elif temp_str.find('TBX5') > 0: 
                        return 'TBX5'
                        break
                    elif temp_str.find('C5SSW1') > 0: 
                        return 'C5SSW1'
                        break
                    elif temp_str.find('C5SSW2') > 0: 
                        return 'C5SSW2'
                        break
                    elif temp_str.find('C5ABS1') > 0: 
                        return 'C5ABS1'
                        break
                    else:
                        if temp_str1[0:1] == '6' and temp_str2.find('CND') > 0 :
                            print(temp_str1)
                            if temp_str1 == '650' or temp_str1 == '651' or temp_str1 == '652':
                                return 'ABX2'
                                break                                
                            elif temp_str1 == '655' or temp_str1 == '656' or temp_str1 == '657':
                                return 'ABX3'
                                break                                      
                            elif temp_str1 == '660' or temp_str1 == '661' or temp_str1 == '662':
                                return 'ABX4'
                                break                                      
                            elif temp_str1 == '665' or temp_str1 == '666' or temp_str1 == '667':
                                return 'TBX5'
                                break                                      
                            elif temp_str1 == '670' or temp_str1 == '671' or temp_str1 == '672':
                                return 'C5SSW1'
                                break 
                            elif temp_str1 == '675' or temp_str1 == '676' or temp_str1 == '677':
                                return 'C5SSW2'
                                break  
                            elif temp_str1 == '680' or temp_str1 == '681' or temp_str1 == '682':
                                return 'C5ABS1'
                                break                                                                                            
                        else:    
                            return 'C4SSW2_NONE'
                            break

def find_finalrte(SSWNUM, b_ratio):
    if b_ratio == '100%' or SSWNUM == 'C4SSW2_NONE':
        return 1000
    else:
        if SSWNUM == 'ABX2' and b_ratio =='50%' : return 650
        if SSWNUM == 'ABX2' and b_ratio =='75%' : return 651
        if SSWNUM == 'ABX2' and b_ratio =='87.5%' : return 652
        
        if SSWNUM == 'ABX3' and b_ratio =='50%' : return 655
        if SSWNUM == 'ABX3' and b_ratio =='75%' : return 656
        if SSWNUM == 'ABX3' and b_ratio =='87.5%' : return 657

        if SSWNUM == 'ABX4' and b_ratio =='50%' : return 660
        if SSWNUM == 'ABX4' and b_ratio =='75%' : return 661
        if SSWNUM == 'ABX4' and b_ratio =='87.5%' : return 662
    
        if SSWNUM == 'TBX5' and b_ratio =='50%' : return 665
        if SSWNUM == 'TBX5' and b_ratio =='75%' : return 666
        if SSWNUM == 'TBX5' and b_ratio =='87.5%' : return 667

        if SSWNUM == 'C5SSW1' and b_ratio =='50%' : return 670
        if SSWNUM == 'C5SSW1' and b_ratio =='75%' : return 671
        if SSWNUM == 'C5SSW1' and b_ratio =='87.5%' : return 672

        if SSWNUM == 'C5SSW2' and b_ratio =='50%' : return 675
        if SSWNUM == 'C5SSW2' and b_ratio =='75%' : return 676
        if SSWNUM == 'C5SSW2' and b_ratio =='87.5%' : return 677

        if SSWNUM == 'C5ABS1' and b_ratio =='50%' : return 680
        if SSWNUM == 'C5ABS1' and b_ratio =='75%' : return 681
        if SSWNUM == 'C5ABS1' and b_ratio =='87.5%' : return 682

def CHKRESULT():
    read_log = 'D:\call_block.txt'
    with open(read_log, 'r', encoding='UTF-8') as f :
        while True:
            read_lines = f.readline()
            if not read_lines:
                break
            read_lines = read_lines.strip()
            if read_lines == 'TUPLE REPLACED':
                return 'True'
                break

def CHKRESULT_TELCO():
    read_log = 'D:\call_block.txt'
    with open(read_log, 'r', encoding='UTF-8') as f :
        while True:
            read_lines = f.readline()
            if not read_lines:
                break
            read_lines = read_lines.strip()
            if read_lines == '>ACCEPTED':
                return 'True'
                break
            
def CHKRESULT_TELCO1():
    read_log = 'D:\call_block.txt'
    with open(read_log, 'r', encoding='UTF-8') as f :
        while True:
            read_lines = f.readline()
            if not read_lines:
                break
            read_lines = read_lines.strip()
            #print(read_lines)
            if read_lines.find('SUCCESS') > 1:            
#            if read_lines == 'RESULT = SUCCESS':
                return 'True'
                break            
      
def codeblock_c4(blocked070, blockedratio):
    # 노텔 C4#2 SecureCRT 선언
    tab_name = ''
    tab_num = ''
    CRT_NAME = ' ' + 'C4_SSW2_CBM'
    S_SSW = '\"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe\" ' + '/S' + CRT_NAME

    ps_kill('C4_SSW2_CBM - SecureCRT')
    # Secure CRT 실행 (10초 timeout )
    proc = sb.Popen(S_SSW,shell=True,text=True)
    try:
        out, errs = proc.communicate(timeout=10)
    except sb.TimeoutExpired:
        proc.kill()

    # 프로세스 명칭 중 C4_SSW2_CBM - SecureCRT을 가진 프로세스를 찾아서 명령어 수행
    ps = findwindows.find_elements()
    app = application.Application(backend='uia')

    for ps_name in ps :
        if str(ps_name).find('C4_SSW2_CBM - SecureCRT') > 1 :
            app.connect(process=ps_name.process_id)
            dlg = app['C4_SSW2_CBM - SecureCRT']
            #dlg.print_control_identifiers()
            send_cmd = 'pos all070 ' + blocked070 + ' ' + blocked070
            dlg['Pane'].type_keys(r'table facode; format pack; verify off; {ENTER}', with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys(send_cmd, with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            time.sleep(3)    
            dlg.exists(timeout=5)
            dlg['Pane'].type_keys(r'table farte; format pack; verify off; {ENTER}', with_spaces=True)   #명령어 수행]
            res_dest = find_dest()
            time.sleep(3) 
            send_rte = 'pos all070 ' + str(res_dest)
            dlg.exists(timeout=5)
            #print(send_rte)      
            dlg['Pane'].type_keys(send_rte, with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            dlg.exists(timeout=5)        
            time.sleep(3)        
            tab_name, tab_num = find_ofrt(res_dest)
            send_ofrt = 'table ' + tab_name + ';format pack'
            send_ofrtnum = 'pos ' + tab_num
            dlg.exists(timeout=5)        
            dlg['Pane'].type_keys(send_ofrt, with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행                
            dlg.exists(timeout=5)  
            time.sleep(3)                
            dlg['Pane'].type_keys(send_ofrtnum, with_spaces=True)   #명령어 수행        
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행        
            time.sleep(3)
            ssw_info = CHK_SSW(tab_num)
            time.sleep(3)
            dlg.exists(timeout=5)
            print('차단번호: ', blocked070)
            print('SSW INFO: ', ssw_info)
            print('차단 비율: ',blockratio.text())
            result_rte = find_finalrte(str(ssw_info), str(blockedratio))
            dlg['Pane'].type_keys(r'quit all; {ENTER}', with_spaces=True)   #명령어 수행]     
            time.sleep(3)                     
            dlg['Pane'].type_keys(r'table facode; format pack; verify off; {ENTER}', with_spaces=True)   #명령어 수행]            
            send_result = 'rep ALL070 ' + str(blocked070) + ' ' + str(blocked070) + ' RTE MM 11 11 DEST ' + str(result_rte) +' '
            send_result2 = 'CLASS NATL AMAXLAID DACOM070 $ $'
            dlg.exists(timeout=5) 
            time.sleep(3)                               
            dlg['Pane'].type_keys(send_result, with_spaces=True)   #명령어 수행        
            dlg['Pane'].type_keys('{+}', with_spaces=True)   #명령어 수행                    
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행 
            dlg.exists(timeout=5) 
            time.sleep(1)                     
            dlg['Pane'].type_keys(send_result2, with_spaces=True)   #명령어 수행        
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행  
            dlg.exists(timeout=5)                        
            time.sleep(3)                  
            dlg['Pane'].type_keys('logout', with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            dlg.exists(timeout=5)                        
            time.sleep(10)                  
            dlg['Pane'].type_keys('exit', with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            time.sleep(10)      
            os.kill(ps_name.process_id,signal.SIGINT)
            c4result= CHKRESULT()
            if c4result == 'True' :
                #print(c4result)
                return 'COMPLETE_C4'
            else : return 'NOT_COMPLETE_C4'
            del_file('D:\call_block.txt')
            #print(f"{ps_name} / 프로세스 : {ps_name.process_id}")07040669718
            break

def coderemove_c4(blocked070, blockedratio):
    # 노텔 C4#2 SecureCRT 선언
    tab_name = ''
    tab_num = ''
    CRT_NAME = ' ' + 'C4_SSW2_CBM'
    S_SSW = '\"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe\" ' + '/S' + CRT_NAME

    ps_kill('C4_SSW2_CBM - SecureCRT')
    # Secure CRT 실행 (10초 timeout )
    proc = sb.Popen(S_SSW,shell=True,text=True)
    try:
        out, errs = proc.communicate(timeout=10)
    except sb.TimeoutExpired:
        proc.kill()

    # 프로세스 명칭 중 C4_SSW2_CBM - SecureCRT을 가진 프로세스를 찾아서 명령어 수행
    ps = findwindows.find_elements()
    app = application.Application(backend='uia')

    for ps_name in ps :
        if str(ps_name).find('C4_SSW2_CBM - SecureCRT') > 1 :
            app.connect(process=ps_name.process_id)
            dlg = app['C4_SSW2_CBM - SecureCRT']
            #dlg.print_control_identifiers()
            temp_070 = '0' + str(int(blocked070) - 1)
            send_cmd = 'pos all070 ' + temp_070 + ' ' + temp_070
            dlg['Pane'].type_keys(r'table facode; format pack; verify off; {ENTER}', with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys(send_cmd, with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            time.sleep(1)    
            dlg.exists(timeout=5)
            res_dest = find_dest()
            time.sleep(3)    
            dlg.exists(timeout=5)

            print('차단 해제 번호: ', blocked070)

            send_result = 'rep ALL070 ' + str(blocked070) + ' ' + str(blocked070) + ' RTE MM 11 11 DEST ' + str(res_dest) +' '
            send_result2 = 'CLASS NATL AMAXLAID DACOM070 $ $'
            dlg.exists(timeout=5) 
            time.sleep(3)                               
            dlg['Pane'].type_keys(send_result, with_spaces=True)   #명령어 수행        
            dlg['Pane'].type_keys('{+}', with_spaces=True)   #명령어 수행                    
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행 
            dlg.exists(timeout=5) 
            time.sleep(1)                     
            dlg['Pane'].type_keys(send_result2, with_spaces=True)   #명령어 수행        
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행  
            dlg.exists(timeout=5)                        
            time.sleep(3)                  
            dlg['Pane'].type_keys('logout', with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            dlg.exists(timeout=5)                        
            time.sleep(10)                  
            dlg['Pane'].type_keys('exit', with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            time.sleep(10)      
            os.kill(ps_name.process_id,signal.SIGINT)
            c4result= CHKRESULT()
            if c4result == 'True' :
                #print(c4result)
                return 'COMPLETE_C4'
            else : return 'NOT_COMPLETE_C4'
            del_file('D:\call_block.txt')
            #print(f"{ps_name} / 프로세스 : {ps_name.process_id}")07040669718
            break

def codeblock_telco(blocked070, blockedratio, telconum):
    
    sswname = ''
    # 텔코SSW SecureCRT 선언
    if telconum == '1':  
        CRT_NAME = ' ' + 'TELCO_GSN1_OMP'
        sswname = 'TELCO_GSN1_OMP - SecureCRT'
    if telconum == '2':  
        CRT_NAME = ' ' + 'TELCO_GSN2_OMP'
        sswname = 'TELCO_GSN2_OMP - SecureCRT'        
    if telconum == '3':  
        CRT_NAME = ' ' + 'TELCO_GSN3_OMP'
        sswname = 'TELCO_GSN3_OMP - SecureCRT'        
    if telconum == '4':  
        CRT_NAME = ' ' + 'TELCO_TJN4_OMP'
        sswname = 'TELCO_TJN4_OMP - SecureCRT' 
    if telconum == '5':
        CRT_NAME = ' ' + 'TELCO_TJN5_OMP'
        sswname = 'TELCO_TJN5_OMP - SecureCRT'
    if telconum == '6':
        CRT_NAME = ' ' + 'TELCO_ANY6_OMP'
        sswname = 'TELCO_ANY6_OMP - SecureCRT'        
    if telconum == '7':
        CRT_NAME = ' ' + 'TELCO_ANY7_OMP'
        sswname = 'TELCO_ANY7_OMP - SecureCRT'
        
    S_SSW = '\"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe\" ' + '/S' + CRT_NAME
    ps_kill(CRT_NAME)
    # Secure CRT 실행 (10초 timeout )
    proc = sb.Popen(S_SSW,shell=True,text=True)
    try:
        out, errs = proc.communicate(timeout=10)
    except sb.TimeoutExpired:
        proc.kill()
        
    # 프로세스 명칭 중 C4_SSW2_CBM - SecureCRT을 가진 프로세스를 찾아서 명령어 수행
    ps = findwindows.find_elements()
    app = application.Application(backend='uia')
    tresult2 = 'False'
    cnt = 7
    tresult = 'False'
    tresult3 = 'False'
    
    for ps_name in ps :
        if str(ps_name).find(sswname) > 1 :
            app.connect(process=ps_name.process_id)
            dlg = app[sswname]
            #dlg.print_control_identifiers()
            time.sleep(1) 
            dlg.exists(timeout=5)                                
            send_discmd = 'dis-pfx     ' + blocked070
            dlg['Pane'].type_keys(send_discmd, with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{;}', with_spaces=True)   #명령어 수행                                
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            time.sleep(3)  
            tresult = CHKRESULT_TELCO1()
            if tresult != 'True' : 
                while True:
                    print('차단번호: ', blocked070)
                    print('SSW INFO: TELCO_C4_SSW#', telconum)
                    print('차단 비율: ',blockratio.text())
                    send_cmd070 = 'copy-pfx     ' + blocked070[0:cnt]                  
                    dlg['Pane'].type_keys(send_cmd070, with_spaces=True)   #명령어 수행
                    dlg['Pane'].type_keys('{,}', with_spaces=True)   #명령어 수행                                                    
                    dlg['Pane'].type_keys(blocked070, with_spaces=True)   #명령어 수행                    
                    dlg['Pane'].type_keys('{;}', with_spaces=True)   #명령어 수행                                
                    dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행  
                    time.sleep(3) 
                    dlg.exists(timeout=5) 
                    dlg['Pane'].type_keys(send_discmd, with_spaces=True)   #명령어 수행
                    dlg['Pane'].type_keys('{;}', with_spaces=True)   #명령어 수행                                
                    dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
                    time.sleep(3)  
                    tresult2 = CHKRESULT_TELCO1()
                    cnt = cnt - 1                                      
                    if tresult2 == 'True' or cnt == 4 : 
                        break

            send_cmd = 'chg-pfx     ' + blocked070 + ',,,,,,,,,,,,,' + blockedratio
            dlg['Pane'].type_keys(send_cmd, with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{;}', with_spaces=True)   #명령어 수행                                
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            time.sleep(3)
            dlg.exists(timeout=5)            
            send_pass = 'rktks1004'
            dlg['Pane'].type_keys(send_pass, with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            time.sleep(3)      
            dlg.exists(timeout=5)    
            dlg['Pane'].type_keys(send_discmd, with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{;}', with_spaces=True)   #명령어 수행                                
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            time.sleep(3)      
            dlg.exists(timeout=5)                        
            dlg['Pane'].type_keys('exit', with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            time.sleep(3)  

            os.kill(ps_name.process_id,signal.SIGINT)
            tresult3 = CHKRESULT_TELCO1()
            if tresult3 == 'True' and (tresult2 == 'True' or tresult == 'True') :
                #print(tresult2)
                return 'COMPLETE_C4'
            else : return 'NOT_COMPLETE_C4'
            del_file('D:\call_block.txt')
            break


def coderemove_telco(blocked070, blockedratio, telconum):
    
    sswname = ''
    # 텔코SSW SecureCRT 선언
    if telconum == '1':  
        CRT_NAME = ' ' + 'TELCO_GSN1_OMP'
        sswname = 'TELCO_GSN1_OMP - SecureCRT'
    if telconum == '2':  
        CRT_NAME = ' ' + 'TELCO_GSN2_OMP'
        sswname = 'TELCO_GSN2_OMP - SecureCRT'        
    if telconum == '3':  
        CRT_NAME = ' ' + 'TELCO_GSN3_OMP'
        sswname = 'TELCO_GSN3_OMP - SecureCRT'        
    if telconum == '4':  
        CRT_NAME = ' ' + 'TELCO_TJN4_OMP'
        sswname = 'TELCO_TJN4_OMP - SecureCRT' 
    if telconum == '5':
        CRT_NAME = ' ' + 'TELCO_TJN5_OMP'
        sswname = 'TELCO_TJN5_OMP - SecureCRT'
    if telconum == '6':
        CRT_NAME = ' ' + 'TELCO_ANY6_OMP'
        sswname = 'TELCO_ANY6_OMP - SecureCRT'        
    if telconum == '7':
        CRT_NAME = ' ' + 'TELCO_ANY7_OMP'
        sswname = 'TELCO_ANY7_OMP - SecureCRT'
        
    S_SSW = '\"C:\Program Files\VanDyke Software\SecureCRT\SecureCRT.exe\" ' + '/S' + CRT_NAME
    ps_kill(CRT_NAME)
    # Secure CRT 실행 (10초 timeout )
    proc = sb.Popen(S_SSW,shell=True,text=True)
    try:
        out, errs = proc.communicate(timeout=10)
    except sb.TimeoutExpired:
        proc.kill()
        
    # 프로세스 명칭 중 C4_SSW2_CBM - SecureCRT을 가진 프로세스를 찾아서 명령어 수행
    ps = findwindows.find_elements()
    app = application.Application(backend='uia')
    tresult2 = 'False'
    cnt = 7
    tresult = 'False'
    tresult3 = 'False'
    
    for ps_name in ps :
        if str(ps_name).find(sswname) > 1 :
            app.connect(process=ps_name.process_id)
            dlg = app[sswname]
            #dlg.print_control_identifiers()
            time.sleep(1) 
            dlg.exists(timeout=5)                                
            send_discmd = 'dis-pfx     ' + blocked070
            dlg['Pane'].type_keys(send_discmd, with_spaces=True)   #명령어 수행
            dlg['Pane'].type_keys('{;}', with_spaces=True)   #명령어 수행                                
            dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
            time.sleep(3)  
            tresult = CHKRESULT_TELCO1()
            if tresult == 'True' : 
                while True:
                    print('차단 해제번호: ', blocked070)
                    print('SSW INFO: TELCO_C4_SSW#', telconum)
                    send_cmd070 = 'del-pfx     ' + blocked070  
                    time.sleep(3) 
                    dlg.exists(timeout=5)                     
                    dlg['Pane'].type_keys(send_cmd070, with_spaces=True)   #명령어 수행
                    dlg['Pane'].type_keys('{;}', with_spaces=True)   #명령어 수행                                
                    dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
                    time.sleep(3)                                     
                    dlg.exists(timeout=5) 
                    send_pass = 'rktks1004'
                    dlg['Pane'].type_keys(send_pass, with_spaces=True)   #명령어 수행
                    dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
                    time.sleep(3) 
                    dlg.exists(timeout=5)                     
                    dlg['Pane'].type_keys(send_discmd, with_spaces=True)   #명령어 수행
                    dlg['Pane'].type_keys('{;}', with_spaces=True)   #명령어 수행                                
                    dlg['Pane'].type_keys('{ENTER}', with_spaces=True)   #명령어 수행
                    time.sleep(3) 
                    dlg.exists(timeout=5)            
                    tresult2 = CHKRESULT_TELCO1()
                    if tresult2 == 'True': 
                        break

            os.kill(ps_name.process_id,signal.SIGINT)
            tresult3 = CHKRESULT_TELCO1()
            if tresult3 == 'True' and (tresult2 == 'True' or tresult == 'True') :
                #print(tresult2)
                return 'COMPLETE_C4'
            else : return 'NOT_COMPLETE_C4'
            del_file('D:\call_block.txt')
            break

# 차단 쓰레드
class Thread1(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        
    def run(self):
        global num070
        global blockratio
        num070 = self.parent.te_query.toPlainText()
        blockratio = self.parent.list_item.currentItem()
        if len(num070) == 11 and num070[0:3] == '070':
            #blockratio = self.list_item.currentItem()
            if (blockratio == ''): blockratio = '50%'
            c4result = codeblock_c4(str(num070), str(blockratio.text()))
            if c4result == 'COMPLETE_C4' :
                self.parent.lb_c42.setStyleSheet("color: blue;"
                                            "font-weight: bold;")   
#                self.parent.lb_c42.repaint()                 

            #텔코 C4#1 차단
            if c4result == 'COMPLETE_C4' :                
                time.sleep(3)
                telco_result1 = codeblock_telco(str(num070), str(blockratio.text()),'1')
                if telco_result1 == 'COMPLETE_C4' :
                    self.parent.lb_telco1.setStyleSheet("color: blue;"
                                            "font-weight: bold;")  
 #                   self.parent.lb_telco1.repaint()                    

            #텔코 C4#2 차단                    
            if telco_result1 == 'COMPLETE_C4' :
                time.sleep(3)
                telco_result2 = codeblock_telco(str(num070), str(blockratio.text()),'2')
                if telco_result2 == 'COMPLETE_C4' :
                    self.parent.lb_telco2.setStyleSheet("color: blue;"
                                            "font-weight: bold;")
    #                self.parent.lb_telco2.repaint()

            if telco_result2 == 'COMPLETE_C4' :
                #텔코 C4#3 차단
                time.sleep(3)
                telco_result3 = codeblock_telco(str(num070), str(blockratio.text()),'3')
                if telco_result3 == 'COMPLETE_C4' :
                    self.parent.lb_telco3.setStyleSheet("color: blue;"
                                            "font-weight: bold;") 
   #                 self.parent.lb_telco3.repaint()                    
                    
            if telco_result3 == 'COMPLETE_C4' :
                #텔코 C4#4 차단
                time.sleep(3)
                telco_result4 = codeblock_telco(str(num070), str(blockratio.text()),'4')
                if telco_result4 == 'COMPLETE_C4' :
                    self.parent.lb_telco4.setStyleSheet("color: blue;"
                                            "font-weight: bold;") 
     #               self.parent.lb_telco4.repaint()                    
                    
            if telco_result4 == 'COMPLETE_C4' :
                #텔코 C4#5 차단
                time.sleep(3)
                telco_result5 = codeblock_telco(str(num070), str(blockratio.text()),'5')
                if telco_result5 == 'COMPLETE_C4' :
                    self.parent.lb_telco5.setStyleSheet("color: blue;"
                                            "font-weight: bold;") 
      #              self.parent.lb_telco5.repaint()                    

            if telco_result5 == 'COMPLETE_C4' :                
                #텔코 C4#6 차단
                time.sleep(3)
                telco_result6 = codeblock_telco(str(num070), str(blockratio.text()),'6')
                if telco_result6 == 'COMPLETE_C4' :
                    self.parent.lb_telco6.setStyleSheet("color: blue;"
                                            "font-weight: bold;") 
        #            self.parent.lb_telco6.repaint()                    

            if telco_result6 == 'COMPLETE_C4' :
                #텔코 C4#7 차단
                time.sleep(3)
                telco_result7 = codeblock_telco(str(num070), str(blockratio.text()),'7')
                if telco_result7 == 'COMPLETE_C4' :
                    self.parent.lb_telco7.setStyleSheet("color: blue;"
                                            "font-weight: bold;") 

# 차단 해제 쓰레드
class Thread2(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        
    def run(self):
        global num070
        global blockratio
        num070 = self.parent.te_query.toPlainText()
        blockratio = self.parent.list_item.currentItem()
        if len(num070) == 11 and num070[0:3] == '070':
            #blockratio = self.list_item.currentItem()
            if (blockratio == ''): blockratio = '0%'
            c4result = coderemove_c4(str(num070), str(blockratio.text()))
            if c4result == 'COMPLETE_C4' :
                self.parent.lb_c42.setStyleSheet("color: limegreen;"
                                            "font-weight: bold;")   
#                self.parent.lb_c42.repaint()                 

            #텔코 C4#1 차단
            if c4result == 'COMPLETE_C4' :                
                time.sleep(3)
                telco_result1 = coderemove_telco(str(num070), str(blockratio.text()),'1')
                if telco_result1 == 'COMPLETE_C4' or telco_result1 == 'NOT_COMPLETE_C4':
                    self.parent.lb_telco1.setStyleSheet("color: limegreen;"
                                            "font-weight: bold;")  
 #                   self.parent.lb_telco1.repaint()                    

            #텔코 C4#2 차단                    
            if telco_result1 == 'COMPLETE_C4' or telco_result1 == 'NOT_COMPLETE_C4':
                time.sleep(3)
                telco_result2 = coderemove_telco(str(num070), str(blockratio.text()),'2')
                if telco_result2 == 'COMPLETE_C4' or telco_result2 == 'NOT_COMPLETE_C4':
                    self.parent.lb_telco2.setStyleSheet("color: limegreen;"
                                            "font-weight: bold;")
    #                self.parent.lb_telco2.repaint()

            if telco_result2 == 'COMPLETE_C4' or telco_result2 == 'NOT_COMPLETE_C4':
                #텔코 C4#3 차단
                time.sleep(3)
                telco_result3 = coderemove_telco(str(num070), str(blockratio.text()),'3')
                if telco_result3 == 'COMPLETE_C4' or telco_result3 == 'NOT_COMPLETE_C4':
                    self.parent.lb_telco3.setStyleSheet("color: limegreen;"
                                            "font-weight: bold;") 
   #                 self.parent.lb_telco3.repaint()                    
                    
            if telco_result3 == 'COMPLETE_C4' or telco_result3 == 'NOT_COMPLETE_C4':
                #텔코 C4#4 차단
                time.sleep(3)
                telco_result4 = coderemove_telco(str(num070), str(blockratio.text()),'4')
                if telco_result4 == 'COMPLETE_C4' or telco_result4 == 'NOT_COMPLETE_C4':
                    self.parent.lb_telco4.setStyleSheet("color: limegreen;"
                                            "font-weight: bold;") 
     #               self.parent.lb_telco4.repaint()                    
                    
            if telco_result4 == 'COMPLETE_C4' or telco_result4 == 'NOT_COMPLETE_C4':
                #텔코 C4#5 차단
                time.sleep(3)
                telco_result5 = coderemove_telco(str(num070), str(blockratio.text()),'5')
                if telco_result5 == 'COMPLETE_C4' or telco_result5 == 'NOT_COMPLETE_C4':
                    self.parent.lb_telco5.setStyleSheet("color: limegreen;"
                                            "font-weight: bold;") 
      #              self.parent.lb_telco5.repaint()                    

            if telco_result5 == 'COMPLETE_C4' or telco_result5 == 'NOT_COMPLETE_C4':                
                #텔코 C4#6 차단
                time.sleep(3)
                telco_result6 = coderemove_telco(str(num070), str(blockratio.text()),'6')
                if telco_result6 == 'COMPLETE_C4' or telco_result6 == 'NOT_COMPLETE_C4':
                    self.parent.lb_telco6.setStyleSheet("color: limegreen;"
                                            "font-weight: bold;") 
        #            self.parent.lb_telco6.repaint()                    

            if telco_result6 == 'COMPLETE_C4' or telco_result6 == 'NOT_COMPLETE_C4':
                #텔코 C4#7 차단
                time.sleep(3)
                telco_result7 = coderemove_telco(str(num070), str(blockratio.text()),'7')
                if telco_result7 == 'COMPLETE_C4' or telco_result7 == 'NOT_COMPLETE_C4':
                    self.parent.lb_telco7.setStyleSheet("color: limegreen;"
                                            "font-weight: bold;") 
        #            self.parent.lb_telco7.repaint()                    
#        else:
#            self.parent.QMessageBox.information(self,'알람','070번호를 정확하게 입력해주세요!!!')   

class MainWindow(qtwid.QMainWindow):
    def __init__(self):
        super().__init__()
        self.te_query = qtwid.QTextEdit(self)
        self.btn_confirm = qtwid.QPushButton('차단시작',self)
        self.btn_confirm1 = qtwid.QPushButton('해제시작',self)        
        self.lb_query = qtwid.QLabel('차단할 070번호를 입력해주세요 : ',self)
        self.list_item = qtwid.QListWidget(self)
        self.lb_item = qtwid.QLabel('차단 비율을 선택해주세요(기본: 50%)', self)
        self.lb_c42 = qtwid.QLabel('노텔_C4#2', self)
        self.lb_telco1 = qtwid.QLabel('텔코시외1', self)        
        self.lb_telco2 = qtwid.QLabel('텔코시외2', self)        
        self.lb_telco3 = qtwid.QLabel('텔코시외3', self)                        
        self.lb_telco4 = qtwid.QLabel('텔코시외4', self)
        self.lb_telco5 = qtwid.QLabel('텔코시외5', self)
        self.lb_telco6 = qtwid.QLabel('텔코시외6', self)          
        self.lb_telco7 = qtwid.QLabel('텔코시외7', self)     
        
        self.setWindowIcon(QIcon('D:\pyhon-test\phone.png'))
        self.Initialize()
        
    def Initialize(self):
        self.setWindowTitle('호 폭주 유발 070번호 착신 차단 Tool')
        
        self.resize(600,300)
        
        groupBox = qtwid.QGroupBox(' 완료여부 (차단완료: 파란색, 해제완료: 연두색) ', self)
        groupBox.move(20,200)
        groupBox.resize(550,80)
        groupBox.setStyleSheet("color: darkorange;"
                               "font-weight: bold;")
        
        self.lb_c42.move(50,220)
        self.lb_c42.resize(70,20)
        self.lb_c42.setStyleSheet("color: black;"
                                    "font-weight: bold;")

        self.lb_telco1.move(140,220)
        self.lb_telco1.resize(60,20)
        self.lb_telco1.setStyleSheet("color: black;"
                                    "font-weight: bold;")        

        self.lb_telco2.move(225,220)
        self.lb_telco2.resize(60,20)
        self.lb_telco2.setStyleSheet("color: black;"
                                    "font-weight: bold;") 

        self.lb_telco3.move(305,220)
        self.lb_telco3.resize(60,20)
        self.lb_telco3.setStyleSheet("color: black;"
                                    "font-weight: bold;") 

        self.lb_telco4.move(385,220)
        self.lb_telco4.resize(100,20)
        self.lb_telco4.setStyleSheet("color: black;"
                                    "font-weight: bold;") 

        self.lb_telco5.move(465,220)
        self.lb_telco5.resize(100,20)
        self.lb_telco5.setStyleSheet("color: black;"
                                    "font-weight: bold;") 

        self.lb_telco6.move(50,250)
        self.lb_telco6.resize(100,20)
        self.lb_telco6.setStyleSheet("color: black;"
                                    "font-weight: bold;") 
        self.lb_telco7.move(140,250)
        self.lb_telco7.resize(100,20)
        self.lb_telco7.setStyleSheet("color: black;"
                                    "font-weight: bold;") 
        
        self.lb_query.move(20,20)
        self.lb_query.resize(190,30)
        self.lb_query.setStyleSheet("color: dodgerblue;"
                                    "font-weight: bold;")
        self.te_query.move(260,20)
        self.te_query.resize(200,30)
        self.btn_confirm.move(490,20)
        self.btn_confirm.resize(80,65)
        self.btn_confirm.setStyleSheet("color: dodgerblue;"
                                       "font-weight: bold;")
        self.btn_confirm.clicked.connect(self.Btn_confirmClick)
        
        self.btn_confirm1.move(490,100)
        self.btn_confirm1.resize(80,65)
        self.btn_confirm1.setStyleSheet("color: green;"
                                       "font-weight: bold;")    
        self.btn_confirm1.clicked.connect(self.Btn_confirmClick1)            
        
        self.lb_item.move(20, 80)
        self.lb_item.resize(230,30)
        self.lb_item.setStyleSheet("color: seagreen;"
                                   "font-weight: bold;")        
        self.list_item.move(260,85)
        self.list_item.resize(200,80)
        self.list_item.addItem('50%')
        self.list_item.addItem('75%')
        self.list_item.addItem('87.5%')
        self.list_item.addItem('100%')
        blockratio = '50%'        
        self.list_item.setCurrentRow(0)  
    
    def Btn_confirmClick(self):
        thr1 = Thread1(self)
        #thr1 = Thread1(self)
        #self.btn_confirm.clicked.connect(self.worker1.Btn_confirmClick)
        self.num070 = self.te_query.toPlainText()
        self.blockratio = self.list_item.currentItem()
        #self.thr1.blockratio = self.list_item.currentItem() 
        if len(self.num070) == 11 and self.num070[0:3] == '070':
            time.sleep(1)
            thr1.start()
        else:
            qtwid.QMessageBox.information(self,'알람','070번호를 정확하게 입력해주세요!!!') 

    def Btn_confirmClick1(self):
        thr2 = Thread2(self)
        #thr1 = Thread1(self)
        #self.btn_confirm.clicked.connect(self.worker1.Btn_confirmClick)
        self.num070 = self.te_query.toPlainText()
        self.blockratio = self.list_item.currentItem()
        #self.thr1.blockratio = self.list_item.currentItem() 
        if len(self.num070) == 11 and self.num070[0:3] == '070':
            time.sleep(1)
            thr2.start()
        else:
            qtwid.QMessageBox.information(self,'알람','070번호를 정확하게 입력해주세요!!!') 

        #thr1.start()

#        self.timer = QTimer()
#        self.timer.setInterval(100)
#        self.timer.timeout.connect(self.worker1.Btn_confirmClick)
#        self.timer.start()
                
    def Lbox_itemSelectionChange(self):
            global blockratio        
            blockratio = self.list_item.currentItem()
            if (blockratio==None):
                blockratio = '50%'

def main():
    app = qtwid.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec_()

resmw = main()
