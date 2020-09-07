%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/noetic/.*$
%global __requires_exclude_from ^/opt/ros/noetic/.*$

Name:           ros-noetic-moveit-core
Version:        1.1.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS moveit_core package

License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       assimp
Requires:       boost-devel
Requires:       boost-python3-devel
Requires:       bullet-devel
Requires:       console-bridge-devel
Requires:       eigen3-devel
Requires:       fcl-devel
Requires:       ros-noetic-eigen-conversions
Requires:       ros-noetic-eigen-stl-containers
Requires:       ros-noetic-geometric-shapes >= 0.5.2
Requires:       ros-noetic-geometry-msgs
Requires:       ros-noetic-kdl-parser
Requires:       ros-noetic-moveit-msgs
Requires:       ros-noetic-octomap
Requires:       ros-noetic-octomap-msgs
Requires:       ros-noetic-random-numbers
Requires:       ros-noetic-rosconsole
Requires:       ros-noetic-roslib
Requires:       ros-noetic-rostime
Requires:       ros-noetic-sensor-msgs
Requires:       ros-noetic-shape-msgs
Requires:       ros-noetic-srdfdom
Requires:       ros-noetic-std-msgs
Requires:       ros-noetic-tf2-eigen
Requires:       ros-noetic-tf2-geometry-msgs
Requires:       ros-noetic-trajectory-msgs
Requires:       ros-noetic-urdf
Requires:       ros-noetic-visualization-msgs
Requires:       ros-noetic-xmlrpcpp
Requires:       urdfdom-devel
Requires:       urdfdom-headers-devel
BuildRequires:  assimp
BuildRequires:  boost-devel
BuildRequires:  boost-python3-devel
BuildRequires:  bullet-devel
BuildRequires:  console-bridge-devel
BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  orocos-kdl-devel
BuildRequires:  pkgconfig
BuildRequires:  ros-noetic-angles
BuildRequires:  ros-noetic-catkin
BuildRequires:  ros-noetic-eigen-conversions
BuildRequires:  ros-noetic-eigen-stl-containers
BuildRequires:  ros-noetic-geometric-shapes >= 0.5.2
BuildRequires:  ros-noetic-geometry-msgs
BuildRequires:  ros-noetic-kdl-parser
BuildRequires:  ros-noetic-moveit-msgs
BuildRequires:  ros-noetic-moveit-resources-panda-moveit-config
BuildRequires:  ros-noetic-moveit-resources-pr2-description
BuildRequires:  ros-noetic-octomap
BuildRequires:  ros-noetic-octomap-msgs
BuildRequires:  ros-noetic-random-numbers
BuildRequires:  ros-noetic-rosconsole
BuildRequires:  ros-noetic-roslib
BuildRequires:  ros-noetic-rostime
BuildRequires:  ros-noetic-rosunit
BuildRequires:  ros-noetic-sensor-msgs
BuildRequires:  ros-noetic-shape-msgs
BuildRequires:  ros-noetic-srdfdom
BuildRequires:  ros-noetic-std-msgs
BuildRequires:  ros-noetic-tf2-eigen
BuildRequires:  ros-noetic-tf2-geometry-msgs
BuildRequires:  ros-noetic-tf2-kdl
BuildRequires:  ros-noetic-trajectory-msgs
BuildRequires:  ros-noetic-urdf
BuildRequires:  ros-noetic-visualization-msgs
BuildRequires:  ros-noetic-xmlrpcpp
BuildRequires:  urdfdom-devel
BuildRequires:  urdfdom-headers-devel
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
Core libraries used by MoveIt

%prep
%autosetup

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/noetic/setup.sh" ]; then . "/opt/ros/noetic/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_LIBDIR="lib" \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/noetic" \
    -DCMAKE_PREFIX_PATH="/opt/ros/noetic" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
    -DCATKIN_BUILD_BINARY_PACKAGE="1" \
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/noetic/setup.sh" ]; then . "/opt/ros/noetic/setup.sh"; fi
%make_install -C obj-%{_target_platform}

%files
/opt/ros/noetic

%changelog
* Mon Sep 07 2020 Dave Coleman <dave@picknik.ai> - 1.1.0-1
- Autogenerated by Bloom

