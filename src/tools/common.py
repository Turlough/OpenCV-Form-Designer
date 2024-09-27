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
little_crop_border = 30
# The scale at which to display the indexing thumbnail.
little_widget_scale = 1.5
# The folder containing template images, json, and csv descriptors
template_folder = r"O:\RESOURCE\ifac_dairygold\forms"
# FIXME This should be a calculated value
num_pages = 15
# FIXME. Why the slight scale difference? Rounding errors?
magic_number = 1.012
# pdf in-mem page extractor. For Windows, point to the "bin" folder
poppler_path = r"\\dddata\output\RESOURCE\ifac_dairygold\poppler-24.07.0\Library\bin"
# Default path for the file picker
pv_export_folder = r"O:\IFAC-DairygoldMilkSupplierCensus\EXPORT"
