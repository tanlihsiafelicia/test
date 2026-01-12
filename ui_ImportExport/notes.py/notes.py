# create ui (done)
# let user select path where to import/ export json file
# add ctrller (done), 
# custom attributes (dont forget to recreate/ add back during import/ recreation process) and keyframes if any

# change to let user select and capture user input (done)
# file_name (done)
# file_path (done)
# capture user selected namespace (done)

# expand
# add to capture curves/ ctrl; shape & transform nodes (done)
# curves attributes (done)
# add into combined_dict (done)
    # check why curve transform and group nodes arent captured! (done)



# CHECK!
# when executing 'import'
# File "<string>", line 208, in cue_import
# AttributeError: 'NoneType' object has no attribute 'text'



# in new scene
# recreate curve, create keyframe animation then try to recreate it before importing into main code

    # getAttr of curves
    # recreate curve
    # add to new sub catergory of combined_dict


# cue_import
# def import
#     def adding_namespace - check and add condition for added keys
#         sample
#         elif key2 == 'file_attached':
#     				namespaced_key2[key2] = value2

#     def set_attribute - check and add condition for added keys
#         sample
#         elif key2 == 'file_attached':
#             continue



# recreate curve (done)
# close curve (done)

# rebuild curve (done)
#     match spans qty to json (done)
#     rematch/ reapply the cv positions back onto the curve (done)
#     xform (done)

# restructure json custom_attr to nested dict (done)
# for loop to addAttr for multiple custom_attr

# check why aiarea lights but name under curve (done)



# EXPORT
# file path for anim export (done)

# IMPORT
# addAttr for custom attributes added




# FEEDBACK
# - if there is no namespace/ reference, then if should recreate the light rig
# - check for ui to not require user to select namespace or select 'no namespace '

# findings
# if the exported has no namespace then it can import without namespace

# covered
# if no animation, still export without keyframe/ animExport (done)
# if there are no custom attribute, conditions to provide empty {} (done)
# custom settings for custom attribute type (done)


# bool OK
# float, min= 0, max= 0, defaultValue= 0
# integer, min= 0, max= 0, defaultValue= 0 
# enum, enumName= IK:FK:


# Check
# file -force -options "precision=8;intValue=17;nodeNames=1;verboseUnits=0;whichRange=1;range=0:40;options=keys;hierarchy=below;controlPoints=0;shapes=1;helpPictures=0;useChannelBox=0;copyKeyCmd=-animation objects -option keys -hierarchy below -controlPoints 0 -shape 1 " -typ "animExport" -pr -es "D:/Felicia/Script_D/ui_ImportExport/json/Anim_Expor3.anim";
# convert animExport to py (check settings)

1. export with namespace referenced, import with namespace referenced (OK)
2. export without namespace referenced, import without namespace referenced
3. export with namespace referenced, import WITHOUT namespace referenced

name space difference
# Traceback (most recent call last):
#   File "<string>", line 241, in cue_import
#   File "D:\Felicia/Script_D/ui_ImportExport\import_export_ui_015.py", line 1268, in main_import
#     import_anim 			= import_animExport(animExport_file_path)
#   File "D:\Felicia/Script_D/ui_ImportExport\import_export_ui_015.py", line 915, in import_animExport
#     cmds.select(select_worldnode())
#   File "D:\Felicia/Script_D/ui_ImportExport\import_export_ui_015.py", line 370, in select_worldnode
#     for d in descendent_list:
# TypeError: 'NoneType' object is not iterable