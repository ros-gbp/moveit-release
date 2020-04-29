/*********************************************************************
 * Software License Agreement (BSD License)
 *
 *  Copyright (c) 2008, Willow Garage, Inc.
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
 *   * Neither the name of Willow Garage nor the names of its
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

/* Author: E. Gil Jones */

#include <moveit/robot_model/robot_model.h>
#include <moveit/robot_state/robot_state.h>
#include <moveit/collision_detection_fcl/collision_world_fcl.h>
#include <moveit/collision_detection_fcl/collision_robot_fcl.h>
#include <moveit/utils/robot_model_test_utils.h>

#include <urdf_parser/urdf_parser.h>
#include <geometric_shapes/shape_operations.h>

#include <gtest/gtest.h>
#include <sstream>
#include <algorithm>
#include <ctype.h>
#include <fstream>

typedef collision_detection::CollisionWorldFCL DefaultCWorldType;
typedef collision_detection::CollisionRobotFCL DefaultCRobotType;

class FclCollisionDetectionTester : public testing::Test
{
protected:
  void SetUp() override
  {
    robot_model_ = moveit::core::loadTestingRobotModel("pr2");
    robot_model_ok_ = static_cast<bool>(robot_model_);
    kinect_dae_resource_ = "package://moveit_resources/pr2_description/urdf/meshes/sensors/kinect_v0/kinect.dae";

    acm_.reset(new collision_detection::AllowedCollisionMatrix(robot_model_->getLinkModelNames(), true));

    crobot_.reset(new DefaultCRobotType(robot_model_));
    cworld_.reset(new DefaultCWorldType());
  }

  void TearDown() override
  {
  }

protected:
  bool robot_model_ok_;

  robot_model::RobotModelPtr robot_model_;

  collision_detection::CollisionRobotPtr crobot_;
  collision_detection::CollisionWorldPtr cworld_;

  collision_detection::AllowedCollisionMatrixPtr acm_;

  std::string kinect_dae_resource_;
};

TEST_F(FclCollisionDetectionTester, InitOK)
{
  ASSERT_TRUE(robot_model_ok_);
}

TEST_F(FclCollisionDetectionTester, DefaultNotInCollision)
{
  robot_state::RobotState robot_state(robot_model_);
  robot_state.setToDefaultValues();
  robot_state.update();

  collision_detection::CollisionRequest req;
  collision_detection::CollisionResult res;
  crobot_->checkSelfCollision(req, res, robot_state, *acm_);
  ASSERT_FALSE(res.collision);
}

TEST_F(FclCollisionDetectionTester, LinksInCollision)
{
  collision_detection::CollisionRequest req;
  collision_detection::CollisionResult res1;
  collision_detection::CollisionResult res2;
  collision_detection::CollisionResult res3;
  // req.contacts = true;
  // req.max_contacts = 100;

  robot_state::RobotState robot_state(robot_model_);
  robot_state.setToDefaultValues();
  robot_state.update();

  Eigen::Isometry3d offset = Eigen::Isometry3d::Identity();
  offset.translation().x() = .01;

  //  robot_state.getLinkState("base_link")->updateGivenGlobalLinkTransform(Eigen::Isometry3d::Identity());
  //  robot_state.getLinkState("base_bellow_link")->updateGivenGlobalLinkTransform(offset);
  robot_state.updateStateWithLinkAt("base_link", Eigen::Isometry3d::Identity());
  robot_state.updateStateWithLinkAt("base_bellow_link", offset);
  robot_state.update();

  acm_->setEntry("base_link", "base_bellow_link", false);
  crobot_->checkSelfCollision(req, res1, robot_state, *acm_);
  ASSERT_TRUE(res1.collision);

  acm_->setEntry("base_link", "base_bellow_link", true);
  crobot_->checkSelfCollision(req, res2, robot_state, *acm_);
  ASSERT_FALSE(res2.collision);

  //  req.verbose = true;
  //  robot_state.getLinkState("r_gripper_palm_link")->updateGivenGlobalLinkTransform(Eigen::Isometry3d::Identity());
  //  robot_state.getLinkState("l_gripper_palm_link")->updateGivenGlobalLinkTransform(offset);
  robot_state.updateStateWithLinkAt("r_gripper_palm_link", Eigen::Isometry3d::Identity());
  robot_state.updateStateWithLinkAt("l_gripper_palm_link", offset);
  robot_state.update();

  acm_->setEntry("r_gripper_palm_link", "l_gripper_palm_link", false);
  crobot_->checkSelfCollision(req, res3, robot_state, *acm_);
  ASSERT_TRUE(res3.collision);
}

TEST_F(FclCollisionDetectionTester, ContactReporting)
{
  collision_detection::CollisionRequest req;
  req.contacts = true;
  req.max_contacts = 1;

  robot_state::RobotState robot_state(robot_model_);
  robot_state.setToDefaultValues();
  robot_state.update();

  Eigen::Isometry3d offset = Eigen::Isometry3d::Identity();
  offset.translation().x() = .01;

  //  robot_state.getLinkState("base_link")->updateGivenGlobalLinkTransform(Eigen::Isometry3d::Identity());
  //  robot_state.getLinkState("base_bellow_link")->updateGivenGlobalLinkTransform(offset);
  //  robot_state.getLinkState("r_gripper_palm_link")->updateGivenGlobalLinkTransform(Eigen::Isometry3d::Identity());
  //  robot_state.getLinkState("l_gripper_palm_link")->updateGivenGlobalLinkTransform(offset);

  robot_state.updateStateWithLinkAt("base_link", Eigen::Isometry3d::Identity());
  robot_state.updateStateWithLinkAt("base_bellow_link", offset);
  robot_state.updateStateWithLinkAt("r_gripper_palm_link", Eigen::Isometry3d::Identity());
  robot_state.updateStateWithLinkAt("l_gripper_palm_link", offset);
  robot_state.update();

  acm_->setEntry("base_link", "base_bellow_link", false);
  acm_->setEntry("r_gripper_palm_link", "l_gripper_palm_link", false);

  collision_detection::CollisionResult res;
  crobot_->checkSelfCollision(req, res, robot_state, *acm_);
  ASSERT_TRUE(res.collision);
  EXPECT_EQ(res.contacts.size(), 1u);
  EXPECT_EQ(res.contacts.begin()->second.size(), 1u);

  res.clear();
  req.max_contacts = 2;
  req.max_contacts_per_pair = 1;
  //  req.verbose = true;
  crobot_->checkSelfCollision(req, res, robot_state, *acm_);
  ASSERT_TRUE(res.collision);
  EXPECT_EQ(res.contacts.size(), 2u);
  EXPECT_EQ(res.contacts.begin()->second.size(), 1u);

  res.contacts.clear();
  res.contact_count = 0;

  req.max_contacts = 10;
  req.max_contacts_per_pair = 2;
  acm_.reset(new collision_detection::AllowedCollisionMatrix(robot_model_->getLinkModelNames(), false));
  crobot_->checkSelfCollision(req, res, robot_state, *acm_);
  ASSERT_TRUE(res.collision);
  EXPECT_LE(res.contacts.size(), 10u);
  EXPECT_LE(res.contact_count, 10u);
}

TEST_F(FclCollisionDetectionTester, ContactPositions)
{
  collision_detection::CollisionRequest req;
  req.contacts = true;
  req.max_contacts = 1;

  robot_state::RobotState robot_state(robot_model_);
  robot_state.setToDefaultValues();
  robot_state.update();

  Eigen::Isometry3d pos1 = Eigen::Isometry3d::Identity();
  Eigen::Isometry3d pos2 = Eigen::Isometry3d::Identity();

  pos1.translation().x() = 5.0;
  pos2.translation().x() = 5.01;

  //  robot_state.getLinkState("r_gripper_palm_link")->updateGivenGlobalLinkTransform(pos1);
  //  robot_state.getLinkState("l_gripper_palm_link")->updateGivenGlobalLinkTransform(pos2);
  robot_state.updateStateWithLinkAt("r_gripper_palm_link", pos1);
  robot_state.updateStateWithLinkAt("l_gripper_palm_link", pos2);
  robot_state.update();

  acm_->setEntry("r_gripper_palm_link", "l_gripper_palm_link", false);

  collision_detection::CollisionResult res;
  crobot_->checkSelfCollision(req, res, robot_state, *acm_);
  ASSERT_TRUE(res.collision);
  ASSERT_EQ(res.contacts.size(), 1u);
  ASSERT_EQ(res.contacts.begin()->second.size(), 1u);

  for (collision_detection::CollisionResult::ContactMap::const_iterator it = res.contacts.begin();
       it != res.contacts.end(); it++)
  {
    EXPECT_NEAR(it->second[0].pos.x(), 5.0, .33);
  }

  pos1 = Eigen::Isometry3d(Eigen::Translation3d(3.0, 0.0, 0.0) * Eigen::Quaterniond::Identity());
  pos2 = Eigen::Isometry3d(Eigen::Translation3d(3.0, 0.0, 0.0) * Eigen::Quaterniond(0.965, 0.0, 0.258, 0.0));
  //  robot_state.getLinkState("r_gripper_palm_link")->updateGivenGlobalLinkTransform(pos1);
  //  robot_state.getLinkState("l_gripper_palm_link")->updateGivenGlobalLinkTransform(pos2);
  robot_state.updateStateWithLinkAt("r_gripper_palm_link", pos1);
  robot_state.updateStateWithLinkAt("l_gripper_palm_link", pos2);
  robot_state.update();

  collision_detection::CollisionResult res2;
  crobot_->checkSelfCollision(req, res2, robot_state, *acm_);
  ASSERT_TRUE(res2.collision);
  ASSERT_EQ(res2.contacts.size(), 1u);
  ASSERT_EQ(res2.contacts.begin()->second.size(), 1u);

  for (collision_detection::CollisionResult::ContactMap::const_iterator it = res2.contacts.begin();
       it != res2.contacts.end(); it++)
  {
    EXPECT_NEAR(it->second[0].pos.x(), 3.0, 0.33);
  }

  pos1 = Eigen::Isometry3d(Eigen::Translation3d(3.0, 0.0, 0.0) * Eigen::Quaterniond::Identity());
  pos2 = Eigen::Isometry3d(Eigen::Translation3d(3.0, 0.0, 0.0) * Eigen::Quaterniond(M_PI / 4.0, 0.0, M_PI / 4.0, 0.0));
  //  robot_state.getLinkState("r_gripper_palm_link")->updateGivenGlobalLinkTransform(pos1);
  //  robot_state.getLinkState("l_gripper_palm_link")->updateGivenGlobalLinkTransform(pos2);
  robot_state.updateStateWithLinkAt("r_gripper_palm_link", pos1);
  robot_state.updateStateWithLinkAt("l_gripper_palm_link", pos2);
  robot_state.update();

  collision_detection::CollisionResult res3;
  crobot_->checkSelfCollision(req, res2, robot_state, *acm_);
  ASSERT_FALSE(res3.collision);
}

TEST_F(FclCollisionDetectionTester, AttachedBodyTester)
{
  collision_detection::CollisionRequest req;
  collision_detection::CollisionResult res;

  acm_.reset(new collision_detection::AllowedCollisionMatrix(robot_model_->getLinkModelNames(), true));

  robot_state::RobotState robot_state(robot_model_);
  robot_state.setToDefaultValues();
  robot_state.update();

  Eigen::Isometry3d pos1 = Eigen::Isometry3d::Identity();
  pos1.translation().x() = 5.0;

  //  robot_state.getLinkState("r_gripper_palm_link")->updateGivenGlobalLinkTransform(pos1);
  robot_state.updateStateWithLinkAt("r_gripper_palm_link", pos1);
  robot_state.update();
  crobot_->checkSelfCollision(req, res, robot_state, *acm_);
  ASSERT_FALSE(res.collision);

  shapes::Shape* shape = new shapes::Box(.1, .1, .1);
  cworld_->getWorld()->addToObject("box", shapes::ShapeConstPtr(shape), pos1);

  res = collision_detection::CollisionResult();
  cworld_->checkRobotCollision(req, res, *crobot_, robot_state, *acm_);
  ASSERT_TRUE(res.collision);

  // deletes shape
  cworld_->getWorld()->removeObject("box");

  shape = new shapes::Box(.1, .1, .1);
  std::vector<shapes::ShapeConstPtr> shapes;
  EigenSTL::vector_Isometry3d poses;
  shapes.push_back(shapes::ShapeConstPtr(shape));
  poses.push_back(Eigen::Isometry3d::Identity());
  std::vector<std::string> touch_links;
  robot_state.attachBody("box", shapes, poses, touch_links, "r_gripper_palm_link");

  res = collision_detection::CollisionResult();
  crobot_->checkSelfCollision(req, res, robot_state, *acm_);
  ASSERT_TRUE(res.collision);

  // deletes shape
  robot_state.clearAttachedBody("box");

  touch_links.push_back("r_gripper_palm_link");
  touch_links.push_back("r_gripper_motor_accelerometer_link");
  shapes[0].reset(new shapes::Box(.1, .1, .1));
  robot_state.attachBody("box", shapes, poses, touch_links, "r_gripper_palm_link");
  robot_state.update();

  res = collision_detection::CollisionResult();
  crobot_->checkSelfCollision(req, res, robot_state, *acm_);
  ASSERT_FALSE(res.collision);

  pos1.translation().x() = 5.01;
  shapes::Shape* coll = new shapes::Box(.1, .1, .1);
  cworld_->getWorld()->addToObject("coll", shapes::ShapeConstPtr(coll), pos1);
  res = collision_detection::CollisionResult();
  cworld_->checkRobotCollision(req, res, *crobot_, robot_state, *acm_);
  ASSERT_TRUE(res.collision);

  acm_->setEntry("coll", "r_gripper_palm_link", true);
  res = collision_detection::CollisionResult();
  cworld_->checkRobotCollision(req, res, *crobot_, robot_state, *acm_);
  ASSERT_TRUE(res.collision);
}

TEST_F(FclCollisionDetectionTester, DiffSceneTester)
{
  robot_state::RobotState robot_state(robot_model_);
  robot_state.setToDefaultValues();
  robot_state.update();

  collision_detection::CollisionRequest req;
  collision_detection::CollisionResult res;

  collision_detection::CollisionRobotFCL new_crobot(
      *(dynamic_cast<collision_detection::CollisionRobotFCL*>(crobot_.get())));

  ros::WallTime before = ros::WallTime::now();
  new_crobot.checkSelfCollision(req, res, robot_state);
  double first_check = (ros::WallTime::now() - before).toSec();
  before = ros::WallTime::now();
  new_crobot.checkSelfCollision(req, res, robot_state);
  double second_check = (ros::WallTime::now() - before).toSec();

  EXPECT_LT(fabs(first_check - second_check), .05);

  std::vector<shapes::ShapeConstPtr> shapes;
  shapes.resize(1);

  shapes[0].reset(shapes::createMeshFromResource(kinect_dae_resource_));

  EigenSTL::vector_Isometry3d poses;
  poses.push_back(Eigen::Isometry3d::Identity());

  std::vector<std::string> touch_links;
  robot_state.attachBody("kinect", shapes, poses, touch_links, "r_gripper_palm_link");

  before = ros::WallTime::now();
  new_crobot.checkSelfCollision(req, res, robot_state);
  first_check = (ros::WallTime::now() - before).toSec();
  before = ros::WallTime::now();
  new_crobot.checkSelfCollision(req, res, robot_state);
  second_check = (ros::WallTime::now() - before).toSec();

  // the first check is going to take a while, as data must be constructed
  EXPECT_LT(second_check, .1);

  collision_detection::CollisionRobotFCL other_new_crobot(
      *(dynamic_cast<collision_detection::CollisionRobotFCL*>(crobot_.get())));
  before = ros::WallTime::now();
  new_crobot.checkSelfCollision(req, res, robot_state);
  first_check = (ros::WallTime::now() - before).toSec();
  before = ros::WallTime::now();
  new_crobot.checkSelfCollision(req, res, robot_state);
  second_check = (ros::WallTime::now() - before).toSec();

  EXPECT_LT(fabs(first_check - second_check), .05);
}

TEST_F(FclCollisionDetectionTester, ConvertObjectToAttached)
{
  collision_detection::CollisionRequest req;
  collision_detection::CollisionResult res;

  shapes::ShapeConstPtr shape(shapes::createMeshFromResource(kinect_dae_resource_));
  Eigen::Isometry3d pos1 = Eigen::Isometry3d::Identity();
  Eigen::Isometry3d pos2 = Eigen::Isometry3d::Identity();
  pos2.translation().x() = 10.0;

  cworld_->getWorld()->addToObject("kinect", shape, pos1);

  robot_state::RobotState robot_state(robot_model_);
  robot_state.setToDefaultValues();
  robot_state.update();

  ros::WallTime before = ros::WallTime::now();
  cworld_->checkRobotCollision(req, res, *crobot_, robot_state);
  double first_check = (ros::WallTime::now() - before).toSec();
  before = ros::WallTime::now();
  cworld_->checkRobotCollision(req, res, *crobot_, robot_state);
  double second_check = (ros::WallTime::now() - before).toSec();

  EXPECT_LT(second_check, .05);

  collision_detection::CollisionWorld::ObjectConstPtr object = cworld_->getWorld()->getObject("kinect");
  cworld_->getWorld()->removeObject("kinect");

  robot_state::RobotState robot_state1(robot_model_);
  robot_state::RobotState robot_state2(robot_model_);
  robot_state1.setToDefaultValues();
  robot_state2.setToDefaultValues();
  robot_state1.update();
  robot_state2.update();

  std::vector<std::string> touch_links;
  robot_state1.attachBody("kinect", object->shapes_, object->shape_poses_, touch_links, "r_gripper_palm_link");

  EigenSTL::vector_Isometry3d other_poses;
  other_poses.push_back(pos2);

  // This creates a new set of constant properties for the attached body, which happens to be the same as the one above;
  robot_state2.attachBody("kinect", object->shapes_, object->shape_poses_, touch_links, "r_gripper_palm_link");

  // going to take a while, but that's fine
  res = collision_detection::CollisionResult();
  crobot_->checkSelfCollision(req, res, robot_state1);

  EXPECT_TRUE(res.collision);

  before = ros::WallTime::now();
  crobot_->checkSelfCollision(req, res, robot_state1, *acm_);
  first_check = (ros::WallTime::now() - before).toSec();
  before = ros::WallTime::now();
  req.verbose = true;
  res = collision_detection::CollisionResult();
  crobot_->checkSelfCollision(req, res, robot_state2, *acm_);
  second_check = (ros::WallTime::now() - before).toSec();

  EXPECT_LT(first_check, .05);
  EXPECT_LT(fabs(first_check - second_check), .1);
}

TEST_F(FclCollisionDetectionTester, TestCollisionMapAdditionSpeed)
{
  EigenSTL::vector_Isometry3d poses;
  std::vector<shapes::ShapeConstPtr> shapes;
  for (unsigned int i = 0; i < 10000; i++)
  {
    poses.push_back(Eigen::Isometry3d::Identity());
    shapes.push_back(shapes::ShapeConstPtr(new shapes::Box(.01, .01, .01)));
  }
  ros::WallTime start = ros::WallTime::now();
  cworld_->getWorld()->addToObject("map", shapes, poses);
  double t = (ros::WallTime::now() - start).toSec();
  EXPECT_GE(1.0, t);
  // this is not really a failure; it is just that slow;
  // looking into doing collision checking with a voxel grid.
  ROS_INFO_NAMED("collision_detection.fcl", "Adding boxes took %g", t);
}

TEST_F(FclCollisionDetectionTester, MoveMesh)
{
  robot_state::RobotState robot_state1(robot_model_);
  robot_state1.setToDefaultValues();
  robot_state1.update();

  Eigen::Isometry3d kinect_pose;
  kinect_pose.setIdentity();
  shapes::ShapePtr kinect_shape;
  kinect_shape.reset(shapes::createMeshFromResource(kinect_dae_resource_));

  cworld_->getWorld()->addToObject("kinect", kinect_shape, kinect_pose);

  Eigen::Isometry3d np;
  for (unsigned int i = 0; i < 5; i++)
  {
    np = Eigen::Translation3d(i * .001, i * .001, i * .001) * Eigen::Quaterniond::Identity();
    cworld_->getWorld()->moveShapeInObject("kinect", kinect_shape, np);
    collision_detection::CollisionRequest req;
    collision_detection::CollisionResult res;
    cworld_->checkCollision(req, res, *crobot_, robot_state1, *acm_);
  }
}

TEST_F(FclCollisionDetectionTester, TestChangingShapeSize)
{
  robot_state::RobotState robot_state1(robot_model_);
  robot_state1.setToDefaultValues();
  robot_state1.update();

  collision_detection::CollisionRequest req1;
  collision_detection::CollisionResult res1;

  ASSERT_FALSE(res1.collision);

  EigenSTL::vector_Isometry3d poses;
  std::vector<shapes::ShapeConstPtr> shapes;
  for (unsigned int i = 0; i < 5; i++)
  {
    cworld_->getWorld()->removeObject("shape");
    shapes.clear();
    poses.clear();
    shapes.push_back(shapes::ShapeConstPtr(new shapes::Box(1 + i * .0001, 1 + i * .0001, 1 + i * .0001)));
    poses.push_back(Eigen::Isometry3d::Identity());
    cworld_->getWorld()->addToObject("shape", shapes, poses);
    collision_detection::CollisionRequest req;
    collision_detection::CollisionResult res;
    cworld_->checkCollision(req, res, *crobot_, robot_state1, *acm_);
    ASSERT_TRUE(res.collision);
  }

  Eigen::Isometry3d kinect_pose = Eigen::Isometry3d::Identity();
  shapes::ShapePtr kinect_shape;
  kinect_shape.reset(shapes::createMeshFromResource(kinect_dae_resource_));
  cworld_->getWorld()->addToObject("kinect", kinect_shape, kinect_pose);
  collision_detection::CollisionRequest req2;
  collision_detection::CollisionResult res2;
  cworld_->checkCollision(req2, res2, *crobot_, robot_state1, *acm_);
  ASSERT_TRUE(res2.collision);
  for (unsigned int i = 0; i < 5; i++)
  {
    cworld_->getWorld()->removeObject("shape");
    shapes.clear();
    poses.clear();
    shapes.push_back(shapes::ShapeConstPtr(new shapes::Box(1 + i * .0001, 1 + i * .0001, 1 + i * .0001)));
    poses.push_back(Eigen::Isometry3d::Identity());
    cworld_->getWorld()->addToObject("shape", shapes, poses);
    collision_detection::CollisionRequest req;
    collision_detection::CollisionResult res;
    cworld_->checkCollision(req, res, *crobot_, robot_state1, *acm_);
    ASSERT_TRUE(res.collision);
  }
}

int main(int argc, char** argv)
{
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
