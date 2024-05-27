#!/bin/bash

set -e # fail script on error

# Note: this script assumes that it is located at SCRIPT_FOLDER="[moveit_source_root]/moveit_kinematics/test/test_4dof",
# and all the model/testing packages generated by it will be placed at ${SCRIPT_FOLDER}/../../../test_4dof/src

TMP_DIR=$(mktemp -d --tmpdir test_4dof.XXXXXX)
SCRIPT_FOLDER="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
LOG_FILE="${TMP_DIR}/test_4dof.log"

OUTPUT_SRC_FOLDER="${SCRIPT_FOLDER}/../../../test_4dof/src"

if [ -d "${OUTPUT_SRC_FOLDER}" ]
then
  OLD_PACKAGES=$(ls -1 "${OUTPUT_SRC_FOLDER}")
  if [ -n "${OLD_PACKAGES}" ]
  then
    echo "${OLD_PACKAGES}" | xargs -d '\n' catkin clean
  fi
fi

rm -rf ""$(dirname "${OUTPUT_SRC_FOLDER}")""
mkdir -p "${OUTPUT_SRC_FOLDER}"
tar -zxf "${SCRIPT_FOLDER}/packages.tgz" -C "${OUTPUT_SRC_FOLDER}"


# Robot/IK configuration
PLANNING_GROUP="arm"
BASE_LINK="base"
EEF_LINK="link_3"
JOINT_NAMES="joint_base, joint_0, joint_1, joint_2"
IK_TYPES=("translationxaxisangle4d"
          "translationyaxisangle4d"
          "translationzaxisangle4d"
          "translationxaxisangleznorm4d"
          "translationyaxisanglexnorm4d"
          "translationzaxisangleynorm4d")
ROBOT_NAMES=("test_4dof_xaxis" "test_4dof_yaxis" "test_4dof_zaxis" "test_4dof_xaxis" "test_4dof_yaxis" "test_4dof_zaxis")
EEF_DIRECTIONS=("1.0 0.0 0.0" "0.0 1.0 0.0" "0.0 0.0 1.0" "1.0 0.0 0.0" "0.0 1.0 0.0" "0.0 0.0 1.0")

echo -e "\n\nNote: detailed messages to stdout are redirected to ${LOG_FILE}\n\n"

echo "Building docker image"
cat <<EOF | docker build -t fixed-openrave - >> "${LOG_FILE}"
FROM personalrobotics/ros-openrave
# Update ROS keys (https://discourse.ros.org/t/new-gpg-keys-deployed-for-packages-ros-org/9454)
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 && \
apt-key del 421C365BD9FF1F717815A3895523BAEEB01FA116 && \
apt-get update && \
apt-get install -y --no-install-recommends python-pip build-essential liblapack-dev ros-indigo-collada-urdf && \
apt-get clean && rm -rf /var/lib/apt/lists/*
# enforce a specific version of sympy, which is known to work with OpenRave
#RUN python -v -m pip install git+https://github.com/sympy/sympy.git@sympy-0.7.1
RUN pip install https://github.com/sympy/sympy/archive/refs/tags/sympy-0.7.1.tar.gz
EOF

CUR_DIR="${PWD}"
cd "${OUTPUT_SRC_FOLDER}"

for INDEX in ${!IK_TYPES[@]}
do
  IK_TYPE=${IK_TYPES[${INDEX}]}
  ROBOT_NAME=${ROBOT_NAMES[${INDEX}]}
  EEF_DIRECTION=${EEF_DIRECTIONS[${INDEX}]}


  DOCKER_INPUT_BINDING="${OUTPUT_SRC_FOLDER}/${ROBOT_NAME}_description"

  if [ ! -f "${DOCKER_INPUT_BINDING}/${ROBOT_NAME}.dae" ]
  then
    # Running a container to convert the given urdf file to one in the dae format
    CMD=(rosrun collada_urdf urdf_to_collada "/input/${ROBOT_NAME}.urdf" "/input/${ROBOT_NAME}.dae")

    docker run --rm --user $(id -u):$(id -g) -v ${TMP_DIR}:/workspace -v "${DOCKER_INPUT_BINDING}":/input \
    --workdir /workspace -e HOME=/workspace fixed-openrave:latest "${CMD[@]}" >> "${LOG_FILE}"

  fi

  # Producing a wrapper.xml describing the robot configuration
  cat <<EOF > "${DOCKER_INPUT_BINDING}/${IK_TYPE}_wrapper.xml"
<robot file="${ROBOT_NAME}.dae">
  <Manipulator name="${ROBOT_NAME}">
    <base>${BASE_LINK}</base>
    <effector>${EEF_LINK}</effector>
    <direction>${EEF_DIRECTION}</direction>
  </Manipulator>
</robot>
EOF

  # Running a container to generate a IKFast solver cpp with the given ik type
  CMD=(openrave0.9.py --database inversekinematics --robot "/input/${IK_TYPE}_wrapper.xml" --iktype "${IK_TYPE}" --iktests=1000)
  echo "Running ${CMD[@]}"

  docker run --rm --user $(id -u):$(id -g) -v "${TMP_DIR}":/workspace -v "${DOCKER_INPUT_BINDING}":/input \
  --workdir /workspace -e HOME=/workspace fixed-openrave:latest "${CMD[@]}" >> "${LOG_FILE}"

  # the solver cpp, if having been generated successfully, will be located in $TMP_DIR/.openrave/*/
  CPP_FILE=$(ls -1 ${TMP_DIR}/.openrave/*/*.cpp 2> /dev/null)
  if [ -z "${CPP_FILE}" ] ; then
    echo "Failed to create an ikfast solver for iktype = ${IK_TYPE}"
    continue
  fi


  # Note that the robot name given to create_ikfast_moveit_plugin.py is deliberately changed to $test_4dof_${IK_TYPE}
  # for the purpose of creating a unique namespace for each plugin referencing the same robot definition but with a different ik solver;
  # the real robot name is still available through the input argument --robot_name_in_srdf

  PACKAGE_NAME="test_4dof_${IK_TYPE}_ikfast_plugin"
  CMD=$(cat <<EOF
"${SCRIPT_FOLDER}/../../ikfast_kinematics_plugin/scripts/create_ikfast_moveit_plugin.py" \
--search_mode=OPTIMIZE_MAX_JOINT \
--moveit_config_pkg=${ROBOT_NAME}_config \
--srdf_filename="${ROBOT_NAME}.srdf" \
--robot_name_in_srdf="${ROBOT_NAME}" \
--eef_direction ${EEF_DIRECTION} \
"test_4dof_${IK_TYPE}" "${PLANNING_GROUP}" \
"${PACKAGE_NAME}" \
"${BASE_LINK}" "${EEF_LINK}" "${CPP_FILE}"
EOF
  )

  echo "Running ${CMD}"
  eval "${CMD}" >> "${LOG_FILE}"

  # Removing the current openrave data, so that it will not interfere with the next run of solver generation
  rm -rf "${TMP_DIR}/.openrave"

  # Generating a test case file "test_4dof-ikfast.test" for this iktype
  CMD=$(cat <<EOF
awk '{ \
gsub(/_ROBOT_CONFIG_/, "${ROBOT_NAME}_config"); \
gsub(/_BASE_LINK_/, "${BASE_LINK}"); \
gsub(/_EEF_LINK_/, "${EEF_LINK}"); \
gsub(/_PLANNING_GROUP_/, "${PLANNING_GROUP}"); \
gsub(/_JOINT_NAMES_/, "${JOINT_NAMES}"); \
gsub(/_IK_PLUGIN_NAME_/, "test_4dof_${IK_TYPE}_${PLANNING_GROUP}/IKFastKinematicsPlugin"); \
gsub(/_TEST_NAME_/, "test_4dof_${IK_TYPE}_ikfast"); \
print}' "${SCRIPT_FOLDER}/test_4dof-ikfast.test" > "./${PACKAGE_NAME}/test_4dof-ikfast.test"
EOF
  )
  eval "${CMD}"

done

cd "${CUR_DIR}"
# Building all generated packages, including model/config ones that are extracted from the prepared tar file "packages.tgz"
ls -1 "${OUTPUT_SRC_FOLDER}" | xargs -d '\n' catkin build --no-status --no-summary --no-deps
