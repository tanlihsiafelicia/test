
import maya.cmds as cmds


# File output and Metadata settings
cmds.setAttr("defaultArnoldDriver.mergeAOVs", 1) # Merge AOV
cmds.setAttr("defaultRenderGlobals.extensionPadding", 4) # Frame padding

# Start and End frame
cmds.setAttr("defaultRenderGlobals.startFrame", 101) # Set start frame
cmds.setAttr("defaultRenderGlobals.endFrame", 110) # Set end frame
cmds.setAttr("CAM_Shape1.mask", 1) # Enable alpha channel (Mask)

# Sampling
cmds.setAttr("defaultArnoldRenderOptions.AASamples", 8) # Camera (AA)
cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 3) # Diffuse
cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", 6) # Specular
cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", 3) # Transmission
cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", 3) # SSS
cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples", 2) # Volume indirect

# Clamping
cmds.setAttr("defaultArnoldRenderOptions.use_sample_clamp", 1) # Enable Clamp AA samples 
cmds.setAttr("defaultArnoldRenderOptions.use_sample_clamp_AOVs", 1) # Enable Affect AOVs
cmds.setAttr("defaultArnoldRenderOptions.AASampleClamp", 2) # AA Clamp value
cmds.setAttr("defaultArnoldRenderOptions.indirectSampleClamp", 2) # Indirect clamp value

# Motion Blur
cmds.setAttr("defaultArnoldRenderOptions.motion_blur_enable", 1) # Enable motion blur
cmds.setAttr("defaultArnoldRenderOptions.motion_frames", 0.02) # Motion blur length value

