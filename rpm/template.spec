%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/noetic/.*$
%global __requires_exclude_from ^/opt/ros/noetic/.*$

Name:           ros-noetic-moveit-ros-perception
Version:        1.1.1
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS moveit_ros_perception package

License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       freeglut-devel
Requires:       glew-devel
Requires:       libomp-devel
Requires:       mesa-libGL-devel
Requires:       mesa-libGLU-devel
Requires:       ros-noetic-cv-bridge
Requires:       ros-noetic-image-transport
Requires:       ros-noetic-message-filters
Requires:       ros-noetic-moveit-core
Requires:       ros-noetic-moveit-msgs
Requires:       ros-noetic-moveit-ros-occupancy-map-monitor
Requires:       ros-noetic-object-recognition-msgs
Requires:       ros-noetic-pluginlib >= 1.11.2
Requires:       ros-noetic-rosconsole
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-sensor-msgs
Requires:       ros-noetic-tf2
Requires:       ros-noetic-tf2-eigen
Requires:       ros-noetic-tf2-geometry-msgs
Requires:       ros-noetic-tf2-ros
Requires:       ros-noetic-urdf
BuildRequires:  eigen3-devel
BuildRequires:  freeglut-devel
BuildRequires:  glew-devel
BuildRequires:  libomp-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  ros-noetic-catkin
BuildRequires:  ros-noetic-cv-bridge
BuildRequires:  ros-noetic-image-transport
BuildRequires:  ros-noetic-message-filters
BuildRequires:  ros-noetic-moveit-core
BuildRequires:  ros-noetic-moveit-msgs
BuildRequires:  ros-noetic-moveit-ros-occupancy-map-monitor
BuildRequires:  ros-noetic-object-recognition-msgs
BuildRequires:  ros-noetic-pluginlib >= 1.11.2
BuildRequires:  ros-noetic-rosconsole
BuildRequires:  ros-noetic-roscpp
BuildRequires:  ros-noetic-rosunit
BuildRequires:  ros-noetic-sensor-msgs
BuildRequires:  ros-noetic-tf2
BuildRequires:  ros-noetic-tf2-eigen
BuildRequires:  ros-noetic-tf2-geometry-msgs
BuildRequires:  ros-noetic-tf2-ros
BuildRequires:  ros-noetic-urdf
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
Components of MoveIt connecting to perception

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
* Tue Oct 13 2020 Michael Ferguson <mferguson@fetchrobotics.com> - 1.1.1-1
- Autogenerated by Bloom

* Mon Sep 07 2020 Michael Ferguson <mferguson@fetchrobotics.com> - 1.1.0-1
- Autogenerated by Bloom

