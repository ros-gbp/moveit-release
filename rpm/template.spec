Name:           ros-indigo-moveit-ros-visualization
Version:        0.7.13
Release:        0%{?dist}
Summary:        ROS moveit_ros_visualization package

Group:          Development/Libraries
License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-indigo-geometric-shapes
Requires:       ros-indigo-interactive-markers
Requires:       ros-indigo-moveit-ros-perception
Requires:       ros-indigo-moveit-ros-planning-interface
Requires:       ros-indigo-moveit-ros-robot-interaction
Requires:       ros-indigo-moveit-ros-warehouse
Requires:       ros-indigo-object-recognition-msgs
Requires:       ros-indigo-pluginlib
Requires:       ros-indigo-roscpp
Requires:       ros-indigo-rospy
Requires:       ros-indigo-rviz
BuildRequires:  pkgconfig
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-cmake-modules
BuildRequires:  ros-indigo-geometric-shapes
BuildRequires:  ros-indigo-interactive-markers
BuildRequires:  ros-indigo-moveit-ros-perception
BuildRequires:  ros-indigo-moveit-ros-planning-interface
BuildRequires:  ros-indigo-moveit-ros-robot-interaction
BuildRequires:  ros-indigo-moveit-ros-warehouse
BuildRequires:  ros-indigo-object-recognition-msgs
BuildRequires:  ros-indigo-pluginlib
BuildRequires:  ros-indigo-roscpp
BuildRequires:  ros-indigo-rospy
BuildRequires:  ros-indigo-rostest
BuildRequires:  ros-indigo-rviz

%description
Components of MoveIt that offer visualization

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/indigo" \
        -DCMAKE_PREFIX_PATH="/opt/ros/indigo" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/indigo

%changelog
* Mon Dec 25 2017 Jon Binney <jon.binney@gmail.com> - 0.7.13-0
- Autogenerated by Bloom

* Sun Aug 06 2017 Ioan Sucan <isucan@google.com> - 0.7.12-0
- Autogenerated by Bloom

* Wed Jun 21 2017 Ioan Sucan <isucan@google.com> - 0.7.11-0
- Autogenerated by Bloom

* Wed Jun 07 2017 Ioan Sucan <isucan@google.com> - 0.7.10-0
- Autogenerated by Bloom

* Mon Apr 03 2017 Ioan Sucan <isucan@google.com> - 0.7.9-0
- Autogenerated by Bloom

* Wed Mar 08 2017 Ioan Sucan <isucan@google.com> - 0.7.8-0
- Autogenerated by Bloom

* Mon Feb 06 2017 Ioan Sucan <isucan@google.com> - 0.7.7-0
- Autogenerated by Bloom

* Fri Dec 30 2016 Ioan Sucan <isucan@google.com> - 0.7.6-0
- Autogenerated by Bloom

* Sun Dec 25 2016 Ioan Sucan <isucan@google.com> - 0.7.5-0
- Autogenerated by Bloom

* Thu Dec 22 2016 Ioan Sucan <isucan@google.com> - 0.7.4-0
- Autogenerated by Bloom

* Tue Dec 20 2016 Ioan Sucan <isucan@google.com> - 0.7.3-0
- Autogenerated by Bloom

