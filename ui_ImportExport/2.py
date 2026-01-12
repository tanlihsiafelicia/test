	if insert_namespace == '': # WITHOUT namespace
		print('WITHOUT namespace')
		# Iterate and check for light existence in scene, if none, recreate light (WITHOUT namespace)
		for key, value in read_json_file['attribute_dict'].items():
			lgtrig_exist = cmds.objExists(key) # Checks scene and compare with json (NO namespace)

			if not lgtrig_exist: # If light rig NOT EXIST in scene
				print(f'{key}: light NOTTTTTTTTTTTTTTT EXIST, WITHOUT namespace')
				creating_create_light	= create_light(read_json_file)
				creating_create_curve	= create_curve(read_json_file)
				creating_custom_attr	= create_custom_attr(read_json_file)
				setting_pivot			= set_pivot(read_json_file)

		# 2nd Iteration after all lights exist, set attribute & import animation
		for key, value in read_json_file['attribute_dict'].items():
			if lgtrig_exist: # If light rig NOW EXIST in scene
				print('########################################################################################')
				print('light EXIST with namespace')
				seting_attr 			= set_attribute(read_json_file)
				import_anim 			= import_animExport(animExport_file_path)

	else: # WITH namespace
		print('WITH namespace')
		# Iterate and check for light existence in scene, if none, recreate light (WITH namespace)
		for key, value in added_namespace['attribute_dict'].items():
			namespace_lgtrig_exist = cmds.objExists(key) # Checks scene and compare with json (WITH namespace)

			if namespace_lgtrig_exist: # If namespace light rig NOT EXIST in scene
				print('light EXIST with namespace')
				set_attr 		= set_attribute(added_namespace)
				import_anim 	= import_animExport(animExport_file_path)
			
			else:
				print(f'{key} does not exist in scene.')