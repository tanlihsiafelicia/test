create_light(loaded_data, lgt_key)
	for key , vlaue in loaded_data['attr_dict'].items():
		if key == lgt_key:
			node_type = value.get(nodetype)
			and the rest of the code