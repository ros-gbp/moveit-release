Name:           ros-jade-moveit-ros-benchmarks-gui
Version:        0.8.6
Release:        0%{?dist}
Summary:        ROS moveit_ros_benchmarks_gui package

Group:          Development/Libraries
License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-jade-eigen-conversions
Requires:       ros-jade-interactive-markers
Requires:       ros-jade-moveit-ros-benchmarks
Requires:       ros-jade-moveit-ros-planning
Requires:       ros-jade-moveit-ros-visualization
Requires:       ros-jade-moveit-ros-warehouse
Requires:       ros-jade-roscpp
Requires:       ros-jade-rviz
Requires:       ros-jade-tf
BuildRequires:  eigen3-devel
BuildRequires:  pkgconfig
BuildRequires:  ros-jade-catkin
BuildRequires:  ros-jade-eigen-conversions
BuildRequires:  ros-jade-interactive-markers
BuildRequires:  ros-jade-moveit-ros-benchmarks
BuildRequires:  ros-jade-moveit-ros-planning
BuildRequires:  ros-jade-moveit-ros-visualization
BuildRequires:  ros-jade-moveit-ros-warehouse
BuildRequires:  ros-jade-roscpp
BuildRequires:  ros-jade-rviz
BuildRequires:  ros-jade-tf

%description
MoveIt GUI tools for benchmarking

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jade/setup.sh" ]; then . "/opt/ros/jade/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/jade" \
        -DCMAKE_PREFIX_PATH="/opt/ros/jade" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jade/setup.sh" ]; then . "/opt/ros/jade/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/jade

%changelog
* Wed Mar 08 2017 Ioan Sucan <isucan@gmail.com> - 0.8.6-0
- Autogenerated by Bloom

* Mon Feb 06 2017 Ioan Sucan <isucan@gmail.com> - 0.8.5-0
- Autogenerated by Bloom

* Mon Feb 06 2017 Ioan Sucan <isucan@gmail.com> - 0.8.4-0
- Autogenerated by Bloom

* Sun Aug 21 2016 Ioan Sucan <isucan@gmail.com> - 0.8.3-0
- Autogenerated by Bloom

