Name:           ros-kinetic-moveit-runtime
Version:        0.9.4
Release:        0%{?dist}
Summary:        ROS moveit_runtime package

Group:          Development/Libraries
License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       ros-kinetic-moveit-core
Requires:       ros-kinetic-moveit-planners
Requires:       ros-kinetic-moveit-plugins
Requires:       ros-kinetic-moveit-ros-manipulation
Requires:       ros-kinetic-moveit-ros-move-group
Requires:       ros-kinetic-moveit-ros-perception
Requires:       ros-kinetic-moveit-ros-planning
Requires:       ros-kinetic-moveit-ros-planning-interface
Requires:       ros-kinetic-moveit-ros-warehouse
BuildRequires:  ros-kinetic-catkin

%description
moveit_runtime meta package contains MoveIt! packages that are essential for its
runtime (e.g. running MoveIt! on robots).

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
* Mon Feb 06 2017 Isaac I. Y. Saito <gm130s@gmail.com> - 0.9.4-0
- Autogenerated by Bloom

