Name:           ros-melodic-moveit-experimental
Version:        0.10.2
Release:        0%{?dist}
Summary:        ROS moveit_experimental package

Group:          Development/Libraries
License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       assimp
Requires:       boost-devel
Requires:       console-bridge-devel
Requires:       eigen3-devel
Requires:       ros-melodic-actionlib-msgs
Requires:       ros-melodic-eigen-stl-containers
Requires:       ros-melodic-geometric-shapes >= 0.3.4
Requires:       ros-melodic-geometry-msgs
Requires:       ros-melodic-kdl-parser
Requires:       ros-melodic-moveit-core
Requires:       ros-melodic-moveit-msgs
Requires:       ros-melodic-octomap
Requires:       ros-melodic-octomap-msgs
Requires:       ros-melodic-pluginlib >= 1.11.2
Requires:       ros-melodic-rosconsole
Requires:       ros-melodic-rostime
Requires:       ros-melodic-sensor-msgs
Requires:       ros-melodic-shape-msgs
Requires:       ros-melodic-std-msgs
Requires:       ros-melodic-tf2-eigen
Requires:       ros-melodic-trajectory-msgs
Requires:       ros-melodic-visualization-msgs
Requires:       urdfdom-devel
Requires:       urdfdom-headers-devel
BuildRequires:  assimp
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  eigen3-devel
BuildRequires:  ros-melodic-actionlib-msgs
BuildRequires:  ros-melodic-angles
BuildRequires:  ros-melodic-catkin
BuildRequires:  ros-melodic-cmake-modules
BuildRequires:  ros-melodic-eigen-stl-containers
BuildRequires:  ros-melodic-geometric-shapes >= 0.3.4
BuildRequires:  ros-melodic-geometry-msgs
BuildRequires:  ros-melodic-kdl-parser
BuildRequires:  ros-melodic-moveit-core
BuildRequires:  ros-melodic-moveit-msgs
BuildRequires:  ros-melodic-moveit-resources
BuildRequires:  ros-melodic-octomap
BuildRequires:  ros-melodic-octomap-msgs
BuildRequires:  ros-melodic-orocos-kdl
BuildRequires:  ros-melodic-pluginlib >= 1.11.2
BuildRequires:  ros-melodic-rosconsole
BuildRequires:  ros-melodic-roslib
BuildRequires:  ros-melodic-rostime
BuildRequires:  ros-melodic-sensor-msgs
BuildRequires:  ros-melodic-shape-msgs
BuildRequires:  ros-melodic-std-msgs
BuildRequires:  ros-melodic-tf2-eigen
BuildRequires:  ros-melodic-trajectory-msgs
BuildRequires:  ros-melodic-visualization-msgs
BuildRequires:  urdfdom-devel
BuildRequires:  urdfdom-headers-devel

%description
Experimental packages for moveit.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/melodic/setup.sh" ]; then . "/opt/ros/melodic/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/melodic" \
        -DCMAKE_PREFIX_PATH="/opt/ros/melodic" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/melodic/setup.sh" ]; then . "/opt/ros/melodic/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/melodic

%changelog
* Wed Oct 24 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.2-0
- Autogenerated by Bloom

* Fri May 25 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.1-0
- Autogenerated by Bloom

* Tue May 22 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.0-0
- Autogenerated by Bloom

