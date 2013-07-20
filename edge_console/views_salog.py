# Create your views here.
# encoding:utf-8

from commons import *
from edge_console.models import *

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def salog_analysis(request):
    """  故障分析统计
    Args:
        end_time: 数据库中记录的处理完故障结束时间
    """

    if not request.user.is_staff:
        return HttpResponse('please <a href="/">login</a> first')

    months = []
    years  = []
    record_types = []
    for t in Salog.objects.all():
        months.append(t.end_time.strftime('%m'))
        years.append(t.end_time.strftime('%Y'))
        record_types.append(t.record_type)
    months = sorted(list(set(months)))
    years = sorted(list(set(years)))
    record_types = sorted(list(set(record_types)))
    color = ['color:#049cdb','color:#46a546','color:#9d261d','color:#f89406',
             'color:#c3325f','color:#7a43b6','color:#FF4500','color:#FF00FF',
             'color:#FF0000','color:#0000FF','color:#4B0082','color:#800000',
             'color:#000080','color:#808000','color:#800080','color:#20B2AA',
             'color:#DEB887','color:#D2691E','color:#FF7F50','color:#DC143C',
             'color:#B8860B','color:#006400','color:#FF69B4','color:#CD5C5C',
             ]
    i = 0
    color_i = 0
    type_color = {}
    while True:
        if i < len(record_types):
            type_color[record_types[i]] = color[color_i]
            i += 1
            color_i += 1
            if color_i >= len(color):
                color_i = 0
        else :
            break

    try:
        if months:
            selected_month = request.GET.get('month',months[-1])
            selected_year = request.GET.get('year',years[-1])
            selected_values = Salog.objects.filter(end_time__month=selected_month,end_time__year=selected_year)
            mon = months.index(selected_month)
        else :
            selected_month = 0
            selected_year = 0
            mon = 0
        if mon-1 >= 0:
            last_month = months[mon - 1]
            last_month_values = Salog.objects.filter(end_time__month=last_month,end_time__year=selected_year)
        else :
            last_month = 0
            last_month_values = []
        if mon+1 < len(months):
            next_month = months[mon + 1]
            next_month_values = Salog.objects.filter(end_time__month=next_month,end_time__year=selected_year)
        else :
            next_month = 0
            next_month_values = []
    except Exception, e:
        pass

    record_dict = {}
    record_lists = []        
    for r in selected_values:
        if r.record_type not in record_dict:
           record_dict[r.record_type] = 1
           record_lists.append(r.record_type)
        else :
           record_dict[r.record_type] += 1
    record_lists.append('汇总')
    
    last_record_dict = {}
    last_record_lists = []
    for r in last_month_values:
        if r.record_type not in last_record_dict:
           last_record_dict[r.record_type] = 1
           last_record_lists.append(r.record_type)
        else :
           last_record_dict[r.record_type] += 1
    last_record_lists.append('汇总')
    
    next_record_dict = {}
    next_record_lists = []
    for r in next_month_values:
        if r.record_type not in next_record_dict:
           next_record_dict[r.record_type] = 1
           next_record_lists.append(r.record_type)
        else :
           next_record_dict[r.record_type] += 1
    next_record_lists.append('汇总')

    total = {}
    current_sum = 0
    for y in record_dict:
        current_sum += record_dict[y]
    record_dict['汇总'] = current_sum
    total['汇总'] = record_dict

    last_total = {}
    last_sum = 0
    for y in last_record_dict:
        last_sum += last_record_dict[y]
    last_record_dict['汇总'] = last_sum
    last_total['汇总'] = last_record_dict

    next_total = {}
    next_sum = 0
    for y in next_record_dict:
        next_sum += next_record_dict[y]
    next_record_dict['汇总'] = next_sum
    next_total['汇总'] = next_record_dict

    operator_dict = {}
    for s in selected_values:
        if s.operator not in operator_dict:
            operator_dict[s.operator] = 1
        else :
            operator_dict[s.operator] += 1
    
    last_operator_dict = {}
    for s in last_month_values:
        if s.operator not in last_operator_dict:
            last_operator_dict[s.operator] = 1
        else :
            last_operator_dict[s.operator] += 1
    
    next_operator_dict = {}
    for s in next_month_values:
        if s.operator not in next_operator_dict:
            next_operator_dict[s.operator] = 1
        else :
            next_operator_dict[s.operator] += 1

    operators = []
    salog_data = {}
    for t in selected_values:
        z = t.operator
        dicts = {}
        if z not in operators:
            for u in selected_values:
                if u.operator == z:
                    if u.record_type not in dicts:
                        dicts[u.record_type] = 1
                    else :
                        dicts[u.record_type] += 1
                else :
                    continue
            operators.append(z)
            dicts['汇总'] = operator_dict[z]
            salog_data[z] = dicts
    
    last_operators = []
    last_salog_data = {}
    for t in last_month_values:
        z = t.operator
        dicts = {}
        if z not in last_operators:
            for u in last_month_values:
                if u.operator == z:
                    if u.record_type not in dicts:
                        dicts[u.record_type] = 1
                    else :
                        dicts[u.record_type] += 1
                else :
                    continue
            last_operators.append(z)
            dicts['汇总'] = last_operator_dict[z]
            last_salog_data[z] = dicts
    
    next_operators = []
    next_salog_data = {}
    for t in next_month_values:
        z = t.operator
        dicts = {}
        if z not in next_operators:
            for u in next_month_values:
                if u.operator == z:
                    if u.record_type not in dicts:
                        dicts[u.record_type] = 1
                    else :
                        dicts[u.record_type] += 1
                else :
                    continue
            next_operators.append(z)
            dicts['汇总'] = next_operator_dict[z]
            next_salog_data[z] = dicts


    return render_to_response('console/salog/salog_analysis.html',{
                'salog_data':salog_data,
                'last_salog_data':last_salog_data,
                'next_salog_data':next_salog_data,
                'total':total,
                'last_total':last_total,
                'next_total':next_total,
                'record_lists':record_lists,
                'last_record_lists':last_record_lists,
                'next_record_lists':next_record_lists,
                'selected_month':selected_month,
                'next_month':next_month,
                'last_month':last_month,
                'selected_year':selected_year,
                'months':months,
                'years':years,
                'type_color':type_color,
                }, context_instance=RequestContext(request))


