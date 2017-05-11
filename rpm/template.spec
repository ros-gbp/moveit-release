Name:           ros-lunar-moveit-ros-control-interface
Version:        0.9.6
Release:        0%{?dist}
Summary:        ROS moveit_ros_control_interface package

Group:          Development/Libraries
License:        BSD
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-lunar-actionlib
Requires:       ros-lunar-controller-manager-msgs
Requires:       ros-lunar-moveit-core
Requires:       ros-lunar-moveit-simple-controller-manager
Requires:       ros-lunar-pluginlib >= 1.10.4
Requires:       ros-lunar-trajectory-msgs
BuildRequires:  ros-lunar-actionlib
BuildRequires:  ros-lunar-catkin
BuildRequires:  ros-lunar-controller-manager-msgs
BuildRequires:  ros-lunar-moveit-core
BuildRequires:  ros-lunar-moveit-simple-controller-manager
BuildRequires:  ros-lunar-pluginlib >= 1.10.4
BuildRequires:  ros-lunar-trajectory-msgs

%description
ros_control controller manager interface for MoveIt!

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/lunar/setup.sh" ]; then . "/opt/ros/lunar/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/lunar" \
        -DCMAKE_PREFIX_PATH="/opt/ros/lunar" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/lunar/setup.sh" ]; then . "/opt/ros/lunar/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/lunar

%changelog
* Wed May 10 2017 Mathias Lüdtke <mathias.luedtke@ipa.fraunhofer.de> - 0.9.6-0
- Autogenerated by Bloom

