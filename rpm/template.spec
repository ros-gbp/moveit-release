Name:           ros-melodic-moveit-ros-perception
Version:        1.0.0
Release:        1%{?dist}
Summary:        ROS moveit_ros_perception package

Group:          Development/Libraries
License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       freeglut-devel
Requires:       glew-devel
Requires:       mesa-libGL-devel
Requires:       mesa-libGLU-devel
Requires:       ros-melodic-cv-bridge
Requires:       ros-melodic-image-transport
Requires:       ros-melodic-message-filters
Requires:       ros-melodic-moveit-core
Requires:       ros-melodic-moveit-msgs
Requires:       ros-melodic-object-recognition-msgs
Requires:       ros-melodic-octomap
Requires:       ros-melodic-pluginlib >= 1.11.2
Requires:       ros-melodic-rosconsole
Requires:       ros-melodic-roscpp
Requires:       ros-melodic-sensor-msgs
Requires:       ros-melodic-tf2
Requires:       ros-melodic-tf2-eigen
Requires:       ros-melodic-tf2-geometry-msgs
Requires:       ros-melodic-tf2-ros
Requires:       ros-melodic-urdf
BuildRequires:  eigen3-devel
BuildRequires:  freeglut-devel
BuildRequires:  glew-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  ros-melodic-catkin
BuildRequires:  ros-melodic-cv-bridge
BuildRequires:  ros-melodic-image-transport
BuildRequires:  ros-melodic-message-filters
BuildRequires:  ros-melodic-moveit-core
BuildRequires:  ros-melodic-moveit-msgs
BuildRequires:  ros-melodic-object-recognition-msgs
BuildRequires:  ros-melodic-octomap
BuildRequires:  ros-melodic-pluginlib >= 1.11.2
BuildRequires:  ros-melodic-rosconsole
BuildRequires:  ros-melodic-roscpp
BuildRequires:  ros-melodic-rosunit
BuildRequires:  ros-melodic-sensor-msgs
BuildRequires:  ros-melodic-tf2
BuildRequires:  ros-melodic-tf2-eigen
BuildRequires:  ros-melodic-tf2-geometry-msgs
BuildRequires:  ros-melodic-tf2-ros
BuildRequires:  ros-melodic-urdf

%description
Components of MoveIt! connecting to perception

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
* Fri Mar 08 2019 Michael Ferguson <mferguson@fetchrobotics.com> - 1.0.0-1
- Autogenerated by Bloom

* Sun Feb 24 2019 Michael Ferguson <mferguson@fetchrobotics.com> - 1.0.0-0
- Autogenerated by Bloom

* Mon Dec 24 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.8-0
- Autogenerated by Bloom

* Thu Dec 13 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.7-0
- Autogenerated by Bloom

* Tue Dec 11 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.6-2
- Autogenerated by Bloom

* Mon Dec 10 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.6-1
- Autogenerated by Bloom

* Mon Dec 10 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.6-0
- Autogenerated by Bloom

* Thu Nov 01 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.5-0
- Autogenerated by Bloom

* Mon Oct 29 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.4-0
- Autogenerated by Bloom

* Mon Oct 29 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.3-0
- Autogenerated by Bloom

* Wed Oct 24 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.2-0
- Autogenerated by Bloom

* Fri May 25 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.1-0
- Autogenerated by Bloom

* Tue May 22 2018 Michael Ferguson <mferguson@fetchrobotics.com> - 0.10.0-0
- Autogenerated by Bloom

