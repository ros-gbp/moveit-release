Name:           ros-kinetic-moveit-core
Version:        0.9.12
Release:        1%{?dist}
Summary:        ROS moveit_core package

Group:          Development/Libraries
License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       assimp
Requires:       boost-devel
Requires:       console-bridge-devel
Requires:       eigen3-devel
Requires:       fcl-devel
Requires:       ros-kinetic-eigen-conversions
Requires:       ros-kinetic-eigen-stl-containers
Requires:       ros-kinetic-geometric-shapes >= 0.5.2
Requires:       ros-kinetic-geometry-msgs
Requires:       ros-kinetic-kdl-parser
Requires:       ros-kinetic-moveit-msgs
Requires:       ros-kinetic-octomap
Requires:       ros-kinetic-octomap-msgs
Requires:       ros-kinetic-random-numbers
Requires:       ros-kinetic-rosconsole
Requires:       ros-kinetic-rostime
Requires:       ros-kinetic-sensor-msgs
Requires:       ros-kinetic-srdfdom
Requires:       ros-kinetic-std-msgs
Requires:       ros-kinetic-trajectory-msgs
Requires:       ros-kinetic-urdf
Requires:       ros-kinetic-visualization-msgs
Requires:       urdfdom-devel
Requires:       urdfdom-headers-devel
BuildRequires:  assimp
BuildRequires:  boost-devel
BuildRequires:  console-bridge-devel
BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  pkgconfig
BuildRequires:  ros-kinetic-angles
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-eigen-conversions
BuildRequires:  ros-kinetic-eigen-stl-containers
BuildRequires:  ros-kinetic-geometric-shapes >= 0.5.2
BuildRequires:  ros-kinetic-geometry-msgs
BuildRequires:  ros-kinetic-kdl-parser
BuildRequires:  ros-kinetic-moveit-msgs
BuildRequires:  ros-kinetic-moveit-resources
BuildRequires:  ros-kinetic-octomap
BuildRequires:  ros-kinetic-octomap-msgs
BuildRequires:  ros-kinetic-orocos-kdl
BuildRequires:  ros-kinetic-random-numbers
BuildRequires:  ros-kinetic-rosconsole
BuildRequires:  ros-kinetic-roslib
BuildRequires:  ros-kinetic-rostime
BuildRequires:  ros-kinetic-rosunit
BuildRequires:  ros-kinetic-sensor-msgs
BuildRequires:  ros-kinetic-shape-msgs
BuildRequires:  ros-kinetic-srdfdom
BuildRequires:  ros-kinetic-std-msgs
BuildRequires:  ros-kinetic-tf-conversions
BuildRequires:  ros-kinetic-trajectory-msgs
BuildRequires:  ros-kinetic-urdf
BuildRequires:  ros-kinetic-visualization-msgs
BuildRequires:  urdfdom-devel
BuildRequires:  urdfdom-headers-devel

%description
Core libraries used by MoveIt!

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/kinetic" \
        -DCMAKE_PREFIX_PATH="/opt/ros/kinetic" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/kinetic

%changelog
* Wed May 30 2018 Dave Coleman <dave@dav.ee> - 0.9.12-1
- Autogenerated by Bloom

* Tue May 29 2018 Dave Coleman <dave@dav.ee> - 0.9.12-0
- Autogenerated by Bloom

* Mon Dec 25 2017 Dave Coleman <dave@dav.ee> - 0.9.11-0
- Autogenerated by Bloom

* Sat Dec 09 2017 Dave Coleman <dave@dav.ee> - 0.9.10-0
- Autogenerated by Bloom

* Sun Aug 06 2017 Dave Coleman <dave@dav.ee> - 0.9.9-0
- Autogenerated by Bloom

* Wed Jun 21 2017 Dave Coleman <dave@dav.ee> - 0.9.8-0
- Autogenerated by Bloom

* Mon Jun 05 2017 Dave Coleman <dave@dav.ee> - 0.9.7-0
- Autogenerated by Bloom

* Wed Apr 12 2017 Dave Coleman <dave@dav.ee> - 0.9.6-0
- Autogenerated by Bloom

* Sat Apr 08 2017 Dave Coleman <dave@dav.ee> - 0.9.5-1
- Autogenerated by Bloom

* Wed Mar 08 2017 Dave Coleman <dave@dav.ee> - 0.9.5-0
- Autogenerated by Bloom

* Mon Feb 06 2017 Dave Coleman <dave@dav.ee> - 0.9.4-0
- Autogenerated by Bloom

* Wed Nov 16 2016 Dave Coleman <dave@dav.ee> - 0.9.3-0
- Autogenerated by Bloom

* Sun Nov 13 2016 Sachin Chitta <robot.moveit@gmail.com> - 0.9.2-1
- Autogenerated by Bloom

