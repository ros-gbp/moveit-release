%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/noetic/.*$
%global __requires_exclude_from ^/opt/ros/noetic/.*$

Name:           ros-noetic-moveit-fake-controller-manager
Version:        1.1.4
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS moveit_fake_controller_manager package

License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-noetic-moveit-core
Requires:       ros-noetic-moveit-ros-planning
Requires:       ros-noetic-pluginlib >= 1.11.2
Requires:       ros-noetic-roscpp
BuildRequires:  ros-noetic-catkin
BuildRequires:  ros-noetic-moveit-core
BuildRequires:  ros-noetic-moveit-ros-planning
BuildRequires:  ros-noetic-pluginlib >= 1.11.2
BuildRequires:  ros-noetic-roscpp
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
A fake controller manager plugin for MoveIt.

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
* Wed May 12 2021 Michael Görner <me@v4hn.de> - 1.1.4-1
- Autogenerated by Bloom

* Tue May 04 2021 Michael Görner <me@v4hn.de> - 1.1.3-1
- Autogenerated by Bloom

* Fri Apr 09 2021 Michael Görner <me@v4hn.de> - 1.1.2-1
- Autogenerated by Bloom

* Tue Oct 13 2020 Michael Görner <me@v4hn.de> - 1.1.1-1
- Autogenerated by Bloom

* Mon Sep 07 2020 Michael Görner <me@v4hn.de> - 1.1.0-1
- Autogenerated by Bloom

