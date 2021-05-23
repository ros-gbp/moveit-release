%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/noetic/.*$
%global __requires_exclude_from ^/opt/ros/noetic/.*$

Name:           ros-noetic-moveit-servo
Version:        1.1.4
Release:        2%{?dist}%{?release_suffix}
Summary:        ROS moveit_servo package

License:        BSD 3-Clause
URL:            https://ros-planning.github.io/moveit_tutorials
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-noetic-control-msgs
Requires:       ros-noetic-control-toolbox
Requires:       ros-noetic-geometry-msgs
Requires:       ros-noetic-joy-teleop
Requires:       ros-noetic-moveit-msgs
Requires:       ros-noetic-moveit-ros-planning-interface
Requires:       ros-noetic-rosparam-shortcuts
Requires:       ros-noetic-sensor-msgs
Requires:       ros-noetic-spacenav-node
Requires:       ros-noetic-std-msgs
Requires:       ros-noetic-std-srvs
Requires:       ros-noetic-tf2-eigen
Requires:       ros-noetic-trajectory-msgs
BuildRequires:  ros-noetic-catkin
BuildRequires:  ros-noetic-control-msgs
BuildRequires:  ros-noetic-control-toolbox
BuildRequires:  ros-noetic-geometry-msgs
BuildRequires:  ros-noetic-moveit-msgs
BuildRequires:  ros-noetic-moveit-resources-panda-moveit-config
BuildRequires:  ros-noetic-moveit-ros-planning-interface
BuildRequires:  ros-noetic-rosparam-shortcuts
BuildRequires:  ros-noetic-rostest
BuildRequires:  ros-noetic-sensor-msgs
BuildRequires:  ros-noetic-std-msgs
BuildRequires:  ros-noetic-std-srvs
BuildRequires:  ros-noetic-tf2-eigen
BuildRequires:  ros-noetic-trajectory-msgs
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
Provides real-time manipulator Cartesian and joint servoing.

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
* Sun May 23 2021 Blake Anderson <blakeanderson@utexas.edu> - 1.1.4-2
- Autogenerated by Bloom

* Wed May 12 2021 Blake Anderson <blakeanderson@utexas.edu> - 1.1.4-1
- Autogenerated by Bloom

* Tue May 04 2021 Blake Anderson <blakeanderson@utexas.edu> - 1.1.3-1
- Autogenerated by Bloom

* Fri Apr 09 2021 Blake Anderson <blakeanderson@utexas.edu> - 1.1.2-1
- Autogenerated by Bloom

* Tue Oct 13 2020 Blake Anderson <blakeanderson@utexas.edu> - 1.1.1-1
- Autogenerated by Bloom

* Mon Sep 07 2020 Blake Anderson <blakeanderson@utexas.edu> - 1.1.0-1
- Autogenerated by Bloom

