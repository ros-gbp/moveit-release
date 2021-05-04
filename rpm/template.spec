%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/noetic/.*$
%global __requires_exclude_from ^/opt/ros/noetic/.*$

Name:           ros-noetic-moveit-ros-planning-interface
Version:        1.1.3
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS moveit_ros_planning_interface package

License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       python3-devel
Requires:       ros-noetic-actionlib
Requires:       ros-noetic-eigenpy
Requires:       ros-noetic-geometry-msgs
Requires:       ros-noetic-moveit-msgs
Requires:       ros-noetic-moveit-ros-manipulation
Requires:       ros-noetic-moveit-ros-move-group
Requires:       ros-noetic-moveit-ros-planning
Requires:       ros-noetic-moveit-ros-warehouse
Requires:       ros-noetic-rosconsole
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-rospy
Requires:       ros-noetic-tf2
Requires:       ros-noetic-tf2-eigen
Requires:       ros-noetic-tf2-geometry-msgs
Requires:       ros-noetic-tf2-ros
BuildRequires:  eigen3-devel
BuildRequires:  python3-catkin_pkg
BuildRequires:  python3-devel
BuildRequires:  ros-noetic-actionlib
BuildRequires:  ros-noetic-catkin
BuildRequires:  ros-noetic-eigenpy
BuildRequires:  ros-noetic-geometry-msgs
BuildRequires:  ros-noetic-moveit-msgs
BuildRequires:  ros-noetic-moveit-resources-fanuc-moveit-config
BuildRequires:  ros-noetic-moveit-resources-panda-moveit-config
BuildRequires:  ros-noetic-moveit-ros-manipulation
BuildRequires:  ros-noetic-moveit-ros-move-group
BuildRequires:  ros-noetic-moveit-ros-planning
BuildRequires:  ros-noetic-moveit-ros-warehouse
BuildRequires:  ros-noetic-rosconsole
BuildRequires:  ros-noetic-roscpp
BuildRequires:  ros-noetic-rospy
BuildRequires:  ros-noetic-rostest
BuildRequires:  ros-noetic-tf2
BuildRequires:  ros-noetic-tf2-eigen
BuildRequires:  ros-noetic-tf2-geometry-msgs
BuildRequires:  ros-noetic-tf2-ros
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
Components of MoveIt that offer simpler interfaces to planning and execution

%prep
%autosetup -p1

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
* Tue May 04 2021 Michael Ferguson <mferguson@fetchrobotics.com> - 1.1.3-1
- Autogenerated by Bloom

* Fri Apr 09 2021 Michael Ferguson <mferguson@fetchrobotics.com> - 1.1.2-1
- Autogenerated by Bloom

* Tue Oct 13 2020 Michael Ferguson <mferguson@fetchrobotics.com> - 1.1.1-1
- Autogenerated by Bloom

* Mon Sep 07 2020 Michael Ferguson <mferguson@fetchrobotics.com> - 1.1.0-1
- Autogenerated by Bloom

