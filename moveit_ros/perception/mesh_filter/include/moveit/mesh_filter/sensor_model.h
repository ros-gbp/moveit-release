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

/* Author: Suat Gedikli */

#pragma once

#include <moveit/macros/class_forward.h>
#include <Eigen/Core>  // for Vector3f

namespace mesh_filter
{
// forward declarations
class GLRenderer;

/**
 * \brief Abstract Interface defining a sensor model for mesh filtering
 * \author Suat Gedikli <gedikli@willowgarage.com>
 */
class SensorModel
{
public:
  MOVEIT_CLASS_FORWARD(Parameters);  // Defines ParametersPtr, ConstPtr, WeakPtr... etc

  /**
   * \brief Abstract Interface defining Sensor Parameters.
   * \author Suat Gedikli <gedikli@willowgarage.com>
   */
  class Parameters
  {
  public:
    /**
     * \brief Constructor taking core parameters that are required for all sensors
     * \param width width of the image generated by this kind of sensor
     * \param height height of the image generated by this kind of sensors
     * \param near_clipping_plane_distance distance of the near clipping plane in meters
     * \param far_clipping_plane_distance distance of the far clipping plane in meters
     */
    Parameters(unsigned width, unsigned height, float near_clipping_plane_distance, float far_clipping_plane_distance);

    /** \brief virtual destructor*/
    virtual ~Parameters();

    /**
     * \brief method that sets required parameters for the renderer.
     * Each sensor usually has its own shaders with specific parameters depending on sensor parameters.
     * This method is called within MeshFilter before any rendering/filtering is done to set any changed
     * sensor parameters in the shader code.
     * \param renderer the renderer that needs to be updated
     */
    virtual void setRenderParameters(GLRenderer& renderer) const = 0;

    /**
     * \brief sets the specific Filter Renderer parameters
     * \param renderer renderer the renderer that needs to be updated
     */
    virtual void setFilterParameters(GLRenderer& renderer) const = 0;

    /**
     * \brief polymorphic clone method
     * \return clones object as base class
     */
    virtual Parameters* clone() const = 0;

    /**
     * \brief returns sensor dependent padding coefficients
     * \return returns sensor dependent padding coefficients
     */
    virtual const Eigen::Vector3f& getPaddingCoefficients() const = 0;

    /**
     * \brief transforms depth values from rendered model to metric depth values
     * \param[in,out] depth pointer to floating point depth buffer
     */
    virtual void transformModelDepthToMetricDepth(float* depth) const;

    /**
     * \brief transforms depth values from filtered depth to metric depth values
     * \param[in,out] depth pointer to floating point depth buffer
     */
    virtual void transformFilteredDepthToMetricDepth(float* depth) const;

    /**
     * \brief sets  the image size
     * \param[in] width with of depth map
     * \param[in] height height of depth map
     */
    void setImageSize(unsigned width, unsigned height);

    /**
     * \brief sets the clipping range
     * \param[in] near distance of near clipping plane
     * \param[in] far distance of far clipping plane
     */
    void setDepthRange(float near, float far);

    /**
     * \brief returns the width of depth maps
     * \return width of the depth map
     */
    unsigned getWidth() const;

    /**
     * \brief returns the height of depth maps
     * \return height of the depth map
     */
    unsigned getHeight() const;

    /**
     * \brief returns distance to the near clipping plane
     * \return distance to near clipping plane
     */
    float getNearClippingPlaneDistance() const;

    /**
     * \brief returns the distance to the far clipping plane
     * \return distance to far clipping plane
     */
    float getFarClippingPlaneDistance() const;

  protected:
    /** \brief width of depth maps generated by the sensor*/
    unsigned width_;

    /** \brief height of depth maps generated by the sensor*/
    unsigned height_;

    /** \brief distance of far clipping plane*/
    float far_clipping_plane_distance_;

    /** \brief distance of near clipping plane*/
    float near_clipping_plane_distance_;
  };

  /**
   * \brief virtual destructor
   */
  virtual ~SensorModel();
};
}  // namespace mesh_filter
