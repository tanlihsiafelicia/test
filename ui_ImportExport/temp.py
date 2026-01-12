ctrl_shape_list = ['nurbsCircle1','nurbsCircle2']

ctrl_attr_name = ['nurbsCircle1.Custom_Attr_1',
                  'nurbsCircle1.rotateX',
                  'nurbsCircle1.rotateY',
                  'nurbsCircle1.rotateZ',
                  'nurbsCircle1.scaleX',
                  'nurbsCircle1.scaleY',
                  'nurbsCircle1.scaleZ',
                  'nurbsCircle1.translateX',
                  'nurbsCircle1.translateY',
                  'nurbsCircle1.translateZ',
                  'nurbsCircle1.visibility',
				  'nurbsCircle2.Custom_Attr_2',
                  'nurbsCircle2.rotateX',
                  'nurbsCircle2.rotateY',
                  'nurbsCircle2.rotateZ',
                  'nurbsCircle2.scaleX',
                  'nurbsCircle2.scaleY',
                  'nurbsCircle2.scaleZ',
                  'nurbsCircle2.translateX',
                  'nurbsCircle2.translateY',
                  'nurbsCircle2.translateZ',
                  'nurbsCircle2.visibility']


for trans in ctrl_shape_list:
    temp_list = []
    for attr in ctrl_attr_name:
        temp_list.append(attr)
    print(temp_list)
