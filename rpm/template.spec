Name:           ros-melodic-chomp-motion-planner
Version:        0.10.7
Release:        0%{?dist}
Summary:        ROS chomp_motion_planner package

Group:          Development/Libraries
License:        BSD
URL:            http://ros.org/wiki/chomp_motion_planner
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  ros-melodic-catkin
BuildRequires:  ros-melodic-moveit-core
BuildRequires:  ros-melodic-roscpp

%description
chomp_motion_planner

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
* Thu Dec 13 2018 Chittaranjan Srinivas Swaminathan <chitt@live.in> - 0.10.7-0
- Autogenerated by Bloom

* Tue Dec 11 2018 Chittaranjan Srinivas Swaminathan <chitt@live.in> - 0.10.6-2
- Autogenerated by Bloom

* Mon Dec 10 2018 Chittaranjan Srinivas Swaminathan <chitt@live.in> - 0.10.6-1
- Autogenerated by Bloom

* Mon Dec 10 2018 Chittaranjan Srinivas Swaminathan <chitt@live.in> - 0.10.6-0
- Autogenerated by Bloom

* Thu Nov 01 2018 Chittaranjan Srinivas Swaminathan <chitt@live.in> - 0.10.5-0
- Autogenerated by Bloom

* Mon Oct 29 2018 Chittaranjan Srinivas Swaminathan <chitt@live.in> - 0.10.4-0
- Autogenerated by Bloom

* Mon Oct 29 2018 Chittaranjan Srinivas Swaminathan <chitt@live.in> - 0.10.3-0
- Autogenerated by Bloom

* Wed Oct 24 2018 Chittaranjan Srinivas Swaminathan <chitt@live.in> - 0.10.2-0
- Autogenerated by Bloom

* Fri May 25 2018 Chittaranjan Srinivas Swaminathan <chitt@live.in> - 0.10.1-0
- Autogenerated by Bloom

* Tue May 22 2018 Chittaranjan Srinivas Swaminathan <chitt@live.in> - 0.10.0-0
- Autogenerated by Bloom

