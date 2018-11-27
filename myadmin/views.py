from django.shortcuts import render, redirect, render_to_response, HttpResponse
import re
from django.http import JsonResponse
import json
from pymongo import MongoClient
import time

# Create your views here.
to_do_list = [

    {'task': '任务一', 'process': False},
    {'task': '任务二', 'process': True},
]


def mongo_init():
    global mongo_use
    mongo_client = MongoClient('localhost', 27017)
    mongo_db = mongo_client['CLuo_Admin_App']
    mongo_use = mongo_db['myadmin']
    return mongo_use


def home(request):

    to_do = {'to_do_list': to_do_list}
    if request.method == 'POST':
        if request.POST['to_do'].strip() == '':
            to_do['errno'] = '警告！ 您输入的为空值'
            return render(request, 'myadmin/home.html', to_do)
        else:
            to_do['errno'] = '添加成功'
            to_do['to_do_list'].append(
                {'task': request.POST['to_do'], 'process': False})
            print(to_do)
            return render(request, 'myadmin/home.html', to_do)
    elif request.method == 'GET':
        return render(request, 'myadmin/home.html', to_do)


def about(request):
    return render(request, 'myadmin/about.html')


def edit(request, forloop_counter):
    to_do = {'to_do_list': to_do_list}
    if request.method == 'POST':
        if request.POST['edit_task'].strip() == '':
            to_do['errno'] = '警告！ 您输入的为空值'
            return render(request, 'myadmin/edit.html', to_do)
        else:
            to_do['errno'] = '添加成功'
            to_do_list[int(forloop_counter) -
                       1]['task'] = request.POST['edit_task']
            print(to_do)
            return redirect('myadmin:home', to_do)
    else:
        content = {'edit_task': to_do_list[int(forloop_counter) - 1]['task']}
        return render(request, 'myadmin/edit.html', content)


def delete(request, forloop_counter):
    to_do_list.pop(int(forloop_counter) - 1)
    return redirect('myadmin:home')


def cross(requset, forloop_counter):
    print(forloop_counter)
    print(requset.POST['process'])
    if int(requset.POST['process']) == 1:

        to_do_list[int(forloop_counter) - 1]['process'] = False
        return redirect('myadmin:home')
    else:
        to_do_list[int(forloop_counter) - 1]['process'] = True
        return redirect('myadmin:home')


# def sdahkd(cloud_text):
# 	re_compile = re.compile('https://pan.b.*?\\r', re.S)
# 	# 所有账号含密码的字符串
#     cloud_lines = re.findall(re_compile, cloud_text)
# 	print(cloud_lines)
# 	for i in cloud_lines:
# 		i = ''.join(i.split())
#         url = re.search("(https:.*?)/", i).group(1)
#         print(url)
#         pwd = re.search('提取码(.*?)复', i).group(1)
#         print(pwd)
#     return 1


def savecloud_from_text(request):
    """
    保存网盘
    """
    # 提取初始化账户信息
    # 格式为{'account':xxx,'process': None,}
    global savecloud_from_text_data
    mongo_use = mongo_init()
    try:
        account_m = mongo_use.find_one({'_id': 'admin'})['account']
        print(account_m)
    except Exception as e:
        # 数据库账号信息
        account_m = {'_id': 'admin', 'account': ''}
        mongo_use.insert_one(account_m)
        savecloud_from_text()
    if request.method == 'GET':
        data = {'info': account_m}
        return render(request, 'myadmin/savecloud_from_text.html', data)
    else:
        # post请求内的账号信息
        account_p = request.POST.get('account')
        if not account_p == account_m:
            try:
                mongo_use.update_one({'account': account_m}, {
                                 '$set': {'account': account_p}})
                print('账号保存成功')
            except Exception as e:
                print('账号保存失败： %s' % (e))
        cloud_text = request.POST.get('cloud_text')
        info = {
            'account': account_p,
            'process': 'null',
        }
        data = {'info': info}
        while True:
        	print('111111')
        	time.sleep(1)
        return JsonResponse(data, content_type='application/json')
    savecloud_from_text_data = data


def check_saveonecloud(request):
    """
    检测任务监督
    """
    return JsonResponse(savecloud_from_text_data, content_type='application/json')
