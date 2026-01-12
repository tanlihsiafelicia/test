# VER1
# Check if scene WITHOUT namespace in scene:
# 		Iterate and check through each key if individual light exist in scene:
# 			If light EXIST:
# 				Import attributes and animation
# 			Else if NOT EXIST:
# 				Recreate light then import attributes and animation
	
# 	Else if scene WITH namespace in scene:
# 		Add namespace and iterate and check through each key if individual light exist in scene:

# 	light rig WITH namespace exist in scene


# VER2
# 	Check if light rig WITHOUT namespace exist in scene
# 	If light rig EXIST:
# 		If  WITH namespace:
# 			Import WITH namespace
# 			Import WITHOUT namespace

# 		If WITHOUT namespace:
# 			Import WITHOUT namespce

# 	If light rig NOT EXIST:
# 		Recreate light rig & import WITHOUT namespace


# VER3
# If NO namespace selected:
# 	Iterate through json file to compare and check for light existence in scene:
# 		If light does NOT EXIST:
# 			Recreate light
	
# 	Iterate again to reconfirm light existence:
# 		If light EXIST:
# 			Set attribute and import animation

# Else if GOT namespace selected:
# 	Iterate through json file to compare and check for light existence in scene:
# 		If light EXIST:
# 			Set attribute and import animation
# 		If light does NOT EXIST:
# 			No nothing

