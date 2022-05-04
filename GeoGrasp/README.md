# GeoGrasp
GeoGrasp (Geometry-based method for computing grasping points on 3D point clouds) updated to work with Ubuntu 18.04, ROS Melodic and PCL 1.8. Based on original code updated by @yayaneath at https://github.com/yayaneath/GeoGrasp.

Find more details at: https://www.researchgate.net/publication/331358070_Fast_Geometry-based_Computation_of_Grasping_Points_on_Three-dimensional_Point_Clouds

# Requirements
The package has been tested on Ubuntu 18.04. GeoGrasp is wrapped in a ROS package with the following dependecies:

- ROS Melodic
- PCL 1.8

The rest of the dependencies (ROS packages) can be found at the `package.xml` file inside the GeoGrasp folder. In order to compile it, just clone this repository inside the `source` directory of your catkin workspace and execute `catkin_make`.

# Example of use

At `GeoGrasp/data` we have included two PCD files with two scenes. The `creeper-isolated.pcd` holds the 3D point cloud of a toy Creeper standing on a table. In contrast, `objects-example.pcd` contains a 3D point cloud in which there are multiple objets on a table. These clouds were captured with a Intel RealSense SR300 camera.

1. (If needed) Create a workspace (reference: http://wiki.ros.org/catkin/Tutorials/create_a_workspace).

```
source /opt/ros/melodic/setup.bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin_make
source devel/setup.bash
```

2. Clone this repository into your ~/catkin_ws/src/ folder and compile it.

```
cd ~/catkin_ws/src/
source devel/setup.bash
git clone https://github.com/ignpaub/GeoGrasp.git
cd ~/catkin_ws/
source devel/setup.bash
catkin_make
```

3. Execute it (several terminals are needed).

(If needed) Terminal 1 -> execute `roscore` to enable ROS.

```
source /opt/ros/melodic/setup.bash
roscore
```

(If needed) Terminal 2 -> publish the point cloud from a pcd file (we require a point cloud topic to process its data). After executing, we will be able to see *topic_name: /cloud_pcd* (`pcl_ros` ROS package is required for running this example). Some pcd files are provided in `GeoGrasp/Data/`.

```
cd ~/catkin_ws/
source devel/setup.bash
rosrun pcl_ros pcd_to_pointcloud src/GeoGrasp/data/objects-example.pcd 0.1 base
```

(For debugging purposes) Terminal 3 -> check if the point cloud is being published. With rostopic list, we localize the topic name and with echo we see the published data.

```
cd ~/catkin_ws/
source devel/setup.bash
rostopic list
rostopic echo /cloud_pcd
```

(For debugging purposes) Terminal 4 -> use rviz to check the how the point cloud visually is. In the graphic interface inside rviz, choose add -> by topic -> PointCloud2. Then, in Global Options -> Fixed Frame (write *base_link*). You will be able to see what is being published.

```
cd ~/catkin_ws/
source devel/setup.bash
rviz
```

Terminal 5 -> finally to test GeoGrasp, simply execute the test script `cloud_processor` included in the repository

```
cd ~/catkin_ws/
source devel/setup.bash
rosrun geograsp cloud_processor _topic:="/cloud_pcd"
```

See below an example of the computed points for the example PCD files:

<img src="GeoGrasp/data/creeper-isolated.png" width="400"> <img src="GeoGrasp/data/objects.png" width="445">

# Applied changes
1. PCL 1.8 changed some functions (comparing with PCL 1.7). Concretely the function pcl::geometry::distance().
We have to edit some code in `geograsp/lib/geograsp/GeoGrasp.cpp`. To avoid this type of error:

```
In file included from /home/ignacio/catkin_ws/src/GeoGrasp/geograsp/include/geograsp/GeoGrasp.h:14:0,
                 from /home/ignacio/catkin_ws/src/GeoGrasp/geograsp/lib/geograsp/GeoGrasp.cpp:1:
/usr/include/pcl-1.8/pcl/common/geometry.h: In instantiation of ‘float pcl::geometry::distance(const PointT&, const PointT&) [with PointT = Eigen::Map<Eigen::Matrix<float, 3, 1>, 0, Eigen::Stride<0, 0> >]’:
/home/ignacio/catkin_ws/src/GeoGrasp/geograsp/lib/geograsp/GeoGrasp.cpp:197:44:   required from here
/usr/include/pcl-1.8/pcl/common/geometry.h:62:33: error: ‘const class Eigen::Map<Eigen::Matrix<float, 3, 1>, 0, Eigen::Stride<0, 0> >’ has no member named ‘getVector3fMap’
       Eigen::Vector3f diff = p1.getVector3fMap () - p2.getVector3fMap ();
                              ~~~^~~~~~~~~~~~~~
/usr/include/pcl-1.8/pcl/common/geometry.h:62:56: error: ‘const class Eigen::Map<Eigen::Matrix<float, 3, 1>, 0, Eigen::Stride<0, 0> >’ has no member named ‘getVector3fMap’
       Eigen::Vector3f diff = p1.getVector3fMap () - p2.getVector3fMap ();                                                     ~~~^~~~~~~~~~~~~~
```

We comment all lines that include this function:
```
float objWidth = pcl::geometry::distance(this->firstGraspPoint.getVector3fMap(),
    this->secondGraspPoint.getVector3fMap())
```
And for each of the commented functions, we add two lines of code:
```
  Eigen::Vector3f new_diff = this->firstGraspPoint.getVector3fMap() - this->secondGraspPoint.getVector3fMap();
  float objWidth = new_diff.norm();
```

2. In `geograsp/CMakeLists.txt`, `target_link_libraries` must be updated. To avoid this linking error:
```
CMakeFiles/cloud_processor.dir/src/cloud_processor.cpp.o: In function `cloudCallback(boost::shared_ptr<sensor_msgs::PointCloud2_<std::allocator<void> > const> const&)':
cloud_processor.cpp:(.text+0x957): undefined reference to `pcl::visualization::PCLVisualizer::removeAllPointClouds(int)'
cloud_processor.cpp:(.text+0x970): undefined reference to `pcl::visualization::PCLVisualizer::removeAllShapes(int)'
cloud_processor.cpp:(.text+0xafc): undefined reference to `pcl::visualization::PCLVisualizer::spinOnce(int, bool)'
cloud_processor.cpp:(.text+0xb71): undefined reference to `pcl::visualization::PCLVisualizer::removeAllPointClouds(int)'
cloud_processor.cpp:(.text+0xb8a): undefined reference to `pcl::visualization::PCLVisualizer::removeAllShapes(int)'
cloud_processor.cpp:(.text+0x14d2): undefined reference to `pcl::visualization::PCLVisualizer::addLine(pcl::ModelCoefficients const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int)'
cloud_processor.cpp:(.text+0x175c): undefined reference to `pcl::visualization::PCLVisualizer::addLine(pcl::ModelCoefficients const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int)'
cloud_processor.cpp:(.text+0x19e6): undefined reference to `pcl::visualization::PCLVisualizer::addLine(pcl::ModelCoefficients const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int)'
cloud_processor.cpp:(.text+0x1ac9): undefined reference to `pcl::visualization::PCLVisualizer::wasStopped() const'
cloud_processor.cpp:(.text+0x1aee): undefined reference to `pcl::visualization::PCLVisualizer::spinOnce(int, bool)'
CMakeFiles/cloud_processor.dir/src/cloud_processor.cpp.o: In function `main':
cloud_processor.cpp:(.text+0x21ac): undefined reference to `pcl::visualization::PCLVisualizer::initCameraParameters()'
cloud_processor.cpp:(.text+0x2214): undefined reference to `pcl::visualization::PCLVisualizer::addCoordinateSystem(double, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int)'
CMakeFiles/cloud_processor.dir/src/cloud_processor.cpp.o: In function `__static_initialization_and_destruction_0(int, int)':
cloud_processor.cpp:(.text+0x275a): undefined reference to `pcl::visualization::PCLVisualizer::PCLVisualizer(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool)'
CMakeFiles/cloud_processor.dir/src/cloud_processor.cpp.o: In function `bool pcl::visualization::PCLVisualizer::addPointCloud<pcl::PointXYZRGB>(pcl::PointCloud<pcl::PointXYZRGB>::ConstPtr const&, pcl::visualization::PointCloudColorHandler<pcl::PointXYZRGB> const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int)':
cloud_processor.cpp:(.text._ZN3pcl13visualization13PCLVisualizer13addPointCloudINS_11PointXYZRGBEEEbRKNS_10PointCloudIT_E8ConstPtrERKNS0_22PointCloudColorHandlerIS5_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEi[_ZN3pcl13visualization13PCLVisualizer13addPointCloudINS_11PointXYZRGBEEEbRKNS_10PointCloudIT_E8ConstPtrERKNS0_22PointCloudColorHandlerIS5_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEi]+0x84): undefined reference to `pcl::visualization::PointCloudGeometryHandlerXYZ<pcl::PointXYZRGB>::PointCloudGeometryHandlerXYZ(boost::shared_ptr<pcl::PointCloud<pcl::PointXYZRGB> const> const&)'
CMakeFiles/cloud_processor.dir/src/cloud_processor.cpp.o: In function `bool pcl::visualization::PCLVisualizer::addSphere<pcl::PointXYZ>(pcl::PointXYZ const&, double, double, double, double, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int)':
cloud_processor.cpp:(.text._ZN3pcl13visualization13PCLVisualizer9addSphereINS_8PointXYZEEEbRKT_ddddRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEi[_ZN3pcl13visualization13PCLVisualizer9addSphereINS_8PointXYZEEEbRKT_ddddRKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEi]+0x36e): undefined reference to `pcl::visualization::PCLVisualizer::addActorToRenderer(vtkSmartPointer<vtkProp> const&, int)'
CMakeFiles/cloud_processor.dir/src/cloud_processor.cpp.o: In function `bool pcl::visualization::PCLVisualizer::fromHandlersToScreen<pcl::PointXYZRGB>(pcl::visualization::PointCloudGeometryHandler<pcl::PointXYZRGB> const&, pcl::visualization::PointCloudColorHandler<pcl::PointXYZRGB> const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, int, Eigen::Matrix<float, 4, 1, 0, 4, 1> const&, Eigen::Quaternion<float, 0> const&)':
cloud_processor.cpp:(.text._ZN3pcl13visualization13PCLVisualizer20fromHandlersToScreenINS_11PointXYZRGBEEEbRKNS0_25PointCloudGeometryHandlerIT_EERKNS0_22PointCloudColorHandlerIS5_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEiRKN5Eigen6MatrixIfLi4ELi1ELi0ELi4ELi1EEERKNSL_10QuaternionIfLi0EEE[_ZN3pcl13visualization13PCLVisualizer20fromHandlersToScreenINS_11PointXYZRGBEEEbRKNS0_25PointCloudGeometryHandlerIT_EERKNS0_22PointCloudColorHandlerIS5_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEiRKN5Eigen6MatrixIfLi4ELi1ELi0ELi4ELi1EEERKNSL_10QuaternionIfLi0EEE]+0x259): undefined reference to `pcl::visualization::PCLVisualizer::createActorFromVTKDataSet(vtkSmartPointer<vtkDataSet> const&, vtkSmartPointer<vtkLODActor>&, bool)'
cloud_processor.cpp:(.text._ZN3pcl13visualization13PCLVisualizer20fromHandlersToScreenINS_11PointXYZRGBEEEbRKNS0_25PointCloudGeometryHandlerIT_EERKNS0_22PointCloudColorHandlerIS5_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEiRKN5Eigen6MatrixIfLi4ELi1ELi0ELi4ELi1EEERKNSL_10QuaternionIfLi0EEE[_ZN3pcl13visualization13PCLVisualizer20fromHandlersToScreenINS_11PointXYZRGBEEEbRKNS0_25PointCloudGeometryHandlerIT_EERKNS0_22PointCloudColorHandlerIS5_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEiRKN5Eigen6MatrixIfLi4ELi1ELi0ELi4ELi1EEERKNSL_10QuaternionIfLi0EEE]+0x2ca): undefined reference to `pcl::visualization::PCLVisualizer::addActorToRenderer(vtkSmartPointer<vtkProp> const&, int)'
cloud_processor.cpp:(.text._ZN3pcl13visualization13PCLVisualizer20fromHandlersToScreenINS_11PointXYZRGBEEEbRKNS0_25PointCloudGeometryHandlerIT_EERKNS0_22PointCloudColorHandlerIS5_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEiRKN5Eigen6MatrixIfLi4ELi1ELi0ELi4ELi1EEERKNSL_10QuaternionIfLi0EEE[_ZN3pcl13visualization13PCLVisualizer20fromHandlersToScreenINS_11PointXYZRGBEEEbRKNS0_25PointCloudGeometryHandlerIT_EERKNS0_22PointCloudColorHandlerIS5_EERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEiRKN5Eigen6MatrixIfLi4ELi1ELi0ELi4ELi1EEERKNSL_10QuaternionIfLi0EEE]+0x359): undefined reference to `pcl::visualization::PCLVisualizer::convertToVtkMatrix(Eigen::Matrix<float, 4, 1, 0, 4, 1> const&, Eigen::Quaternion<float, 0> const&, vtkSmartPointer<vtkMatrix4x4>&)'
CMakeFiles/cloud_processor.dir/src/cloud_processor.cpp.o: In function `void pcl::visualization::PCLVisualizer::convertPointCloudToVTKPolyData<pcl::PointXYZRGB>(pcl::visualization::PointCloudGeometryHandler<pcl::PointXYZRGB> const&, vtkSmartPointer<vtkPolyData>&, vtkSmartPointer<vtkIdTypeArray>&)':
cloud_processor.cpp:(.text._ZN3pcl13visualization13PCLVisualizer30convertPointCloudToVTKPolyDataINS_11PointXYZRGBEEEvRKNS0_25PointCloudGeometryHandlerIT_EER15vtkSmartPointerI11vtkPolyDataERS9_I14vtkIdTypeArrayE[_ZN3pcl13visualization13PCLVisualizer30convertPointCloudToVTKPolyDataINS_11PointXYZRGBEEEvRKNS0_25PointCloudGeometryHandlerIT_EER15vtkSmartPointerI11vtkPolyDataERS9_I14vtkIdTypeArrayE]+0x5b): undefined reference to `pcl::visualization::PCLVisualizer::allocVtkPolyData(vtkSmartPointer<vtkPolyData>&)'
cloud_processor.cpp:(.text._ZN3pcl13visualization13PCLVisualizer30convertPointCloudToVTKPolyDataINS_11PointXYZRGBEEEvRKNS0_25PointCloudGeometryHandlerIT_EER15vtkSmartPointerI11vtkPolyDataERS9_I14vtkIdTypeArrayE[_ZN3pcl13visualization13PCLVisualizer30convertPointCloudToVTKPolyDataINS_11PointXYZRGBEEEvRKNS0_25PointCloudGeometryHandlerIT_EER15vtkSmartPointerI11vtkPolyDataERS9_I14vtkIdTypeArrayE]+0x1c3): undefined reference to `pcl::visualization::PCLVisualizer::updateCells(vtkSmartPointer<vtkIdTypeArray>&, vtkSmartPointer<vtkIdTypeArray>&, long long)'
CMakeFiles/cloud_processor.dir/src/cloud_processor.cpp.o:(.data.rel.ro._ZTVN3pcl13visualization28PointCloudGeometryHandlerXYZINS_11PointXYZRGBEEE[_ZTVN3pcl13visualization28PointCloudGeometryHandlerXYZINS_11PointXYZRGBEEE]+0x30): undefined reference to `pcl::visualization::PointCloudGeometryHandlerXYZ<pcl::PointXYZRGB>::getGeometry(vtkSmartPointer<vtkPoints>&) const'
collect2: error: ld returned 1 exit status
GeoGrasp/geograsp/CMakeFiles/cloud_processor.dir/build.make:311: recipe for target '/home/ignacio/catkin_ws/devel/lib/geograsp/cloud_processor' failed

```
We add `pcl_visualization` line.

# Citation
[1] Zapata-Impata, B. S., Mateo, C. M., Gil, P., & Pomares, J. (2017). Using Geometry to Detect Grasping Points on 3D Unknown Point Cloud. In Proceedings of the 14th International Conference on Informatics in Control, Automation and Robotics (ICINCO) 2017 (Vol. 2, pp. 154–161). Best Paper Award. SCITEPRESS - Science and Technology Publications. https://doi.org/10.5220/0006470701540161

[2] Zapata-Impata, B. S., Gil, P., Pomares, J., & Torres, F. (2019). Fast geometry-based computation of grasping points on three-dimensional point clouds. International Journal of Advanced Robotic Systems, 16(1), 172988141983184. https://doi.org/10.1177/1729881419831846
