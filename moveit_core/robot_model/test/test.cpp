/*********************************************************************
* Software License Agreement (BSD License)
*
*  Copyright (c) 2013, Willow Garage, Inc.
*  All rights reserved.
*
*  Redistribution and use in source and binary forms, with or without
*  modification, are permitted provided that the following conditions
*  are met:
*
*   * Redistributions of source code must retain the above copyright
*     notice, this list of conditions and the following disclaimer.
*   * Redistributions in binary form must reproduce the above
*     copyright notice, this list of conditions and the following
*     disclaimer in the documentation and/or other materials provided
*     with the distribution.
*   * Neither the name of the Willow Garage nor the names of its
*     contributors may be used to endorse or promote products derived
*     from this software without specific prior written permission.
*
*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
*  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
*  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
*  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
*  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
*  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
*  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
*  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
*  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
*  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
*  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
*  POSSIBILITY OF SUCH DAMAGE.
*********************************************************************/

/* Author: Ioan Sucan */

#include <moveit/robot_model/robot_model.h>
#include <urdf_parser/urdf_parser.h>
#include <fstream>
#include <gtest/gtest.h>
#include <boost/filesystem/path.hpp>
#include <moveit/profiler/profiler.h>
#include <ros/package.h>

class LoadPlanningModelsPr2 : public testing::Test
{
protected:

  virtual void SetUp()
  {
    srdf_model.reset(new srdf::Model());
    std::string xml_string;
    std::string resource_dir = ros::package::getPath("moveit_resources");
    if(resource_dir == "")
    {
      FAIL() << "Failed to find package moveit_resources.";
      return;
    }
    std::fstream xml_file((boost::filesystem::path(resource_dir) / "test/urdf/robot.xml").string().c_str(), std::fstream::in);
    if (xml_file.is_open())
    {
      while (xml_file.good())
      {
        std::string line;
        std::getline(xml_file, line);
        xml_string += (line + "\n");
      }
      xml_file.close();
      urdf_model = urdf::parseURDF(xml_string);
    }
    srdf_model->initFile(*urdf_model, (boost::filesystem::path(resource_dir) / "test/srdf/robot.xml").string());
    robot_model.reset(new moveit::core::RobotModel(urdf_model, srdf_model));
  };

  virtual void TearDown()
  {
  }

protected:

  boost::shared_ptr<urdf::ModelInterface> urdf_model;
  boost::shared_ptr<srdf::Model> srdf_model;
  moveit::core::RobotModelConstPtr robot_model;
};

TEST_F(LoadPlanningModelsPr2, InitOK)
{
  ASSERT_EQ(urdf_model->getName(), "pr2");
  ASSERT_EQ(srdf_model->getName(), "pr2");
}

TEST_F(LoadPlanningModelsPr2, Model)
{
  //robot_model->printModelInfo(std::cout);

  const std::vector<const moveit::core::JointModel*> &joints = robot_model->getJointModels();
  for (std::size_t i = 0 ; i < joints.size() ; ++i)
  {
    ASSERT_EQ(joints[i]->getJointIndex(), i);
    ASSERT_EQ(robot_model->getJointModel(joints[i]->getName()), joints[i]);
  }
  const std::vector<const moveit::core::LinkModel*> &links = robot_model->getLinkModels();
  for (std::size_t i = 0 ; i < links.size() ; ++i)
  {
    ASSERT_EQ(links[i]->getLinkIndex(), i);
    //    std::cout << joints[i]->getName() << std::endl;

  }
  moveit::tools::Profiler::Status();

}


int main(int argc, char **argv)
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
