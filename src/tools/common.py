# The scale to display the image in Designer
design_scale = 0.45
# The resolution of the template images
design_resolution = 200
# The resolution at which to extract images from PDF, for indexing. Smaller is quicker, but blurry
index_resolution = 100
# A calculated scale for the indexer. Ensures fields line up properly
index_scale = design_scale * design_resolution / index_resolution
# The scaling factor for "IndexViews" is always the Design scale
widget_scale = design_scale
# Border around the indexing thumbnail
little_crop_border = 10
# The scale at which to display the indexing thumbnail.
little_widget_scale = 1.5
# The folder containing template images, json, and csv descriptors
template_folder = r"C:\_PV\forms3"
