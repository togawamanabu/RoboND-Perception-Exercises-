# Import PCL module
import pcl

# Load Point Cloud file
cloud = pcl.load_XYZRGB('tabletop.pcd')


# Voxel Grid filter
vox = cloud.make_voxel_grid_filter()

LEAF_SIZE = 0.01

vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)

cloud_filterd = vox.filter()
filename = 'voxel_downsampled.pcd'
pcl.save(cloud_filterd, filename)

# PassThrough filter
passthrough = cloud_filterd.make_passthrough_filter()

filter_axis = 'z'
passthrough.set_filter_field_name(filter_axis)
axis_min = 0.6
axis_max = 1.1
passthrough.set_filter_limits (axis_min, axis_max)

cloud_filtered = passthrough.filter()
filename = 'pass_through_filtered.pcd'
pcl.save(cloud_filtered, filename)

# RANSAC plane segmentation
seg = cloud_filtered.make_segmenter()

#set the model wisht to fit
seg.set_model_type(pcl.SACMODEL_PLANE)
seg.set_method_type(pcl.SAC_RANSAC)

max_distance = 0.01
seg.set_distance_threshold(max_distance)

inliers, coefficients = seg.segment()

# Extract inliers

extracted_inliners = cloud_filtered.extract(inliers, negative=False)
filename = 'extracted_inliners.pcd'
pcl.save(extracted_inliners, filename)

# Extract outliers
extracted_outliers = cloud_filtered.extract(inliers, negative=True)
filename = 'extracted_outliers.pcd'
pcl.save(extracted_outliers, filename)





