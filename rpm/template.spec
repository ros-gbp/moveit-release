Name:           ros-indigo-moveit-ros-planning-interface
Version:        0.7.4
Release:        0%{?dist}
Summary:        ROS moveit_ros_planning_interface package

Group:          Development/Libraries
License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       python-devel
Requires:       ros-indigo-actionlib
Requires:       ros-indigo-eigen-conversions
Requires:       ros-indigo-moveit-ros-manipulation
Requires:       ros-indigo-moveit-ros-move-group
Requires:       ros-indigo-moveit-ros-planning
Requires:       ros-indigo-moveit-ros-warehouse
Requires:       ros-indigo-rosconsole
Requires:       ros-indigo-roscpp
Requires:       ros-indigo-rospy
Requires:       ros-indigo-tf
Requires:       ros-indigo-tf-conversions
BuildRequires:  python-catkin_pkg
BuildRequires:  python-devel
BuildRequires:  ros-indigo-actionlib
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-cmake-modules
BuildRequires:  ros-indigo-eigen-conversions
BuildRequires:  ros-indigo-moveit-ros-manipulation
BuildRequires:  ros-indigo-moveit-ros-move-group
BuildRequires:  ros-indigo-moveit-ros-planning
BuildRequires:  ros-indigo-moveit-ros-warehouse
BuildRequires:  ros-indigo-rosconsole
BuildRequires:  ros-indigo-roscpp
BuildRequires:  ros-indigo-rospy
BuildRequires:  ros-indigo-tf
BuildRequires:  ros-indigo-tf-conversions

%description
Components of MoveIt that offer simpler interfaces to planning and execution

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
* Thu Dec 22 2016 Ioan Sucan <isucan@google.com> - 0.7.4-0
- Autogenerated by Bloom

* Tue Dec 20 2016 Ioan Sucan <isucan@google.com> - 0.7.3-0
- Autogenerated by Bloom

