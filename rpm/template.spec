%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/noetic/.*$
%global __requires_exclude_from ^/opt/ros/noetic/.*$

Name:           ros-noetic-pilz-industrial-motion-planner
Version:        1.1.3
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS pilz_industrial_motion_planner package

License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       orocos-kdl-devel
Requires:       ros-noetic-joint-limits-interface
Requires:       ros-noetic-moveit-core
Requires:       ros-noetic-moveit-msgs
Requires:       ros-noetic-moveit-ros-move-group
Requires:       ros-noetic-moveit-ros-planning
Requires:       ros-noetic-moveit-ros-planning-interface
Requires:       ros-noetic-pluginlib
Requires:       ros-noetic-roscpp
Requires:       ros-noetic-tf2
Requires:       ros-noetic-tf2-eigen
Requires:       ros-noetic-tf2-geometry-msgs
Requires:       ros-noetic-tf2-kdl
Requires:       ros-noetic-tf2-ros
BuildRequires:  orocos-kdl-devel
BuildRequires:  ros-noetic-catkin
BuildRequires:  ros-noetic-cmake-modules
BuildRequires:  ros-noetic-code-coverage
BuildRequires:  ros-noetic-joint-limits-interface
BuildRequires:  ros-noetic-moveit-core
BuildRequires:  ros-noetic-moveit-msgs
BuildRequires:  ros-noetic-moveit-resources-panda-moveit-config
BuildRequires:  ros-noetic-moveit-resources-prbt-moveit-config
BuildRequires:  ros-noetic-moveit-resources-prbt-pg70-support
BuildRequires:  ros-noetic-moveit-resources-prbt-support
BuildRequires:  ros-noetic-moveit-ros-move-group
BuildRequires:  ros-noetic-moveit-ros-planning
BuildRequires:  ros-noetic-moveit-ros-planning-interface
BuildRequires:  ros-noetic-pilz-industrial-motion-planner-testutils
BuildRequires:  ros-noetic-pluginlib
BuildRequires:  ros-noetic-roscpp
BuildRequires:  ros-noetic-rostest
BuildRequires:  ros-noetic-rosunit
BuildRequires:  ros-noetic-tf2
BuildRequires:  ros-noetic-tf2-eigen
BuildRequires:  ros-noetic-tf2-geometry-msgs
BuildRequires:  ros-noetic-tf2-kdl
BuildRequires:  ros-noetic-tf2-ros
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
MoveIt plugin to generate industrial trajectories PTP, LIN, CIRC and sequences
thereof.

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
* Tue May 04 2021 Alexander Gutenkunst <a.gutenkunst@pilz.de> - 1.1.3-1
- Autogenerated by Bloom

* Fri Apr 09 2021 Alexander Gutenkunst <a.gutenkunst@pilz.de> - 1.1.2-1
- Autogenerated by Bloom

