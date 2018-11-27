from django.shortcuts import render, redirect, render_to_response, HttpResponse
import re
from django.http import JsonResponse
import json

# Create your views here.
to_do_list = [

    {'task': '任务一', 'process': False},
    {'task': '任务二', 'process': True},
]


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
    if request.method == 'GET':
        content = {'account': 11111, 'cloud_text': '222'}
        return render(request, 'myadmin/savecloud_from_text.html', {'info': content})
    else:
        print(request.POST)
        print(request.POST.get('account'))
        print(request.POST.get('cloud_text'))
        content = {}
        content['account'] = request.POST.get('account')
        content['cloud_text'] = request.POST.get('cloud_text')
        print('34234', JsonResponse(
            {"info": content}, content_type='application/json'))
        # return HttpResponse(json.dumps({"info": content}), content_type='application/json')
        return JsonResponse({"info": content}, content_type='application/json')
