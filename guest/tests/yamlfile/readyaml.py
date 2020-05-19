import yaml

f=open('addevent.yaml',encoding='utf-8')
res=yaml.full_load(f)
print(res)