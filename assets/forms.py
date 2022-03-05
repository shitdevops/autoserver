# _*_ coding:utf-8 _*_
# By:赵先宇
from django import forms
from repository import models


class ChangeBusinessForm(forms.Form):
    busid = forms.IntegerField(label='业务线ID')
    name = forms.CharField(label='业务线名称')
    memo = forms.CharField(label='备注', max_length=255, widget=forms.Textarea, required=False)


class AddBusinessForm(forms.Form):
    name = forms.CharField(label='业务线名称')
    memo = forms.CharField(label='备注', max_length=255, widget=forms.Textarea, required=False)


class AddIdcForm(forms.Form):
    name = forms.CharField(label='机房名称')
    memo = forms.CharField(label='备注', max_length=255, widget=forms.Textarea, required=False)


class ChangeIdcForm(forms.Form):
    idc_id = forms.IntegerField(label='机房ID')
    name = forms.CharField(label='机房名称')
    memo = forms.CharField(label='备注', max_length=255, widget=forms.Textarea, required=False)


class ChangeAssetForm(forms.Form):
    created_by_choice = (
        ('auto', '自动添加'),
        ('manual', '手工录入'),
    )
    asset_status = (
        (0, '在线'),
        (1, '下线'),
        (2, '未知'),
        (3, '故障'),
        (4, '备用'),
    )
    asset_id = forms.IntegerField(label='资产ID')
    created = forms.ChoiceField(label='添加方式', choices=created_by_choice)
    status = forms.ChoiceField(label='状态', choices=asset_status)
    memo = forms.CharField(label='备注', max_length=255, widget=forms.Textarea, required=False)
    business_id = forms.IntegerField(label='所属业务线')
    idc_id = forms.IntegerField(label='所属机房')


class AddAssetForm(forms.Form):
    # asset_name = forms.CharField(label='资产名称', max_length=64)
    status = forms.IntegerField(label='设备状态')
    created = forms.CharField(label='添加方式')
    memo = forms.CharField(label='备注', max_length=255, widget=forms.Textarea, required=False)
    hostname = forms.CharField(label='主机名', max_length=128)
    os_platform = forms.CharField(label='系统', max_length=16, required=False)
    os_version = forms.CharField(label='系统版本', max_length=16, required=False)
    sn = forms.CharField(label='SN号', max_length=64)
    manufacturer = forms.CharField(label='制造商', max_length=64, required=False)
    model = forms.CharField(label='型号', max_length=64, required=False)
    cpu_count = forms.IntegerField(label='CPU个数', required=False)
    cpu_physical_count = forms.IntegerField(label='CPU物理个数', required=False)
    cpu_model = forms.CharField(label='CPU型号', max_length=128, required=False)
    tag = forms.CharField(label='标签', max_length=125, required=False)
    business_id = forms.IntegerField(label='所属业务线', required=False)
    idc_id = forms.IntegerField(label='所属机房', required=False)