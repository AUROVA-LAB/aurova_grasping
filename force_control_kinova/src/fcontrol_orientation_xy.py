#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import time
import math
from papillarray_ros_v2.msg import SensorState
from kortex_driver.msg import TwistCommand

class ImpedanceController:
    def __init__(self):
        # ---- Force controller parameters ----
        self.force_desired = rospy.get_param('force_desired',  0.5)  # Desired force in N
        self.K_p = rospy.get_param('K_p', 0.00225)  # Proportional gain (0.2 for solid surface)
        self.K_d = rospy.get_param('K_d', 0.00015)  # Derivative gain (0.0001-0.00025 for solid surface)

        self.K_p_orient = rospy.get_param('K_p_orient', 0.05)  # Gain for orientation correction
        self.K_fx = rospy.get_param('K_fx', 0.00)  # Gain for velocity adjustment in X
        self.K_fy = rospy.get_param('K_fy', 0.00)  # Gain for velocity adjustment in Y

        self.loop_rate_hz = rospy.get_param('loop_rate_hz', 50.0)  # Control loop frequency (Hz)

        self.dt = 1.0 / self.loop_rate_hz

        # ---- State variables ----
        self.forces = {i: {"fX": 0.0, "fY": 0.0, "fZ": 0.0} for i in range(9)}  # Forces from the 9 pillars
        self.prev_error = 0.0    # Previous error for derivative control
        self.contact = False
        self.init = False
        self.end = False
        self.experiment = True
        self.time_exp = 30.0
        self.loops = 1.0 

        # ---- Parameters for circular trajectory (in XY) ----
        self.move_in_circle = rospy.get_param('move_in_circle', True)
        self.radius = rospy.get_param('circle_radius', 0.090)  # [m]
        self.period = rospy.get_param('circle_period', self.time_exp) # [s] time to complete one circle
        self.omega = 2.0 * math.pi / self.period  # Angular velocity [rad/s]

        self.start_time = time.time()

        # ---- PapillArray sensor subscriber ----
        rospy.Subscriber('/hub_0/sensor_0', SensorState, self.force_callback, queue_size=10)

        # ---- Publisher for velocity commands (Twist) ----
        self.cmd_pub = rospy.Publisher('/terminator/in/cartesian_velocity',
                                       TwistCommand, queue_size=1)

        rospy.loginfo("ImpedanceController started with K_p_orient=%.4f, loop=%.1f Hz",
                      self.K_p_orient, self.loop_rate_hz)

    def force_callback(self, msg: SensorState):
        """Callback to extract forces from the sensor pillars."""
        self.contact = bool(msg.is_contact)
        for pillar in msg.pillars:
            self.forces[pillar.id]["fX"] = pillar.fX
            self.forces[pillar.id]["fY"] = pillar.fY
            self.forces[pillar.id]["fZ"] = pillar.fZ
        self.contact = bool(msg.is_contact)

    def control_loop(self):

        twist_cmd = TwistCommand()
        reference_frame = 2 #  0 base, 1 mixed, 2 tool
        twist_cmd.reference_frame = reference_frame

        # ---- Approach until contact ----
        if(not(self.contact)and not (self.init)):

            if (reference_frame == 2):
                twist_cmd.twist.linear_x = 0 
                twist_cmd.twist.linear_y = 0 
                twist_cmd.twist.linear_z = 0.0020 
                twist_cmd.twist.angular_x = 0  
                twist_cmd.twist.angular_y = 0  
                twist_cmd.twist.angular_z = 0.0      

            else:
                twist_cmd.twist.linear_x = 0 
                twist_cmd.twist.linear_y = 0 
                twist_cmd.twist.linear_z = -0.0020
                twist_cmd.twist.angular_x = 0 
                twist_cmd.twist.angular_y = 0  
                twist_cmd.twist.angular_z = 0.0

            self.start_time = time.time()
              
        # ---- Main experiment loop ----
        elif(self.experiment):
            self.init = True
            # --- 1) Compute force error (Z) ---
            Fz = self.forces[4]["fZ"]  # Force in central pillar
            error = self.force_desired - Fz

            # --- 2) Compute error derivative ---
            dedt = (error - self.prev_error) / self.dt
            self.prev_error = error

            # --- 3) PD control to get normal velocity magnitude ---
            vf_mag = self.K_p * error + self.K_d * dedt

            # Saturate magnitude
            max_vf = 0.1  # m/s
            vf_mag = max(min(vf_mag, max_vf), -max_vf)

            # --- 5) Velocity adjustment based on Fx and Fy ---
            Fx = self.forces[3]["fZ"] - self.forces[5]["fZ"]  # Force difference in Y
            Fy = self.forces[7]["fZ"] - self.forces[1]["fZ"]  # Force difference in X

            # --- 6) Proportional orientation control ---
            omega_x = -self.K_p_orient * Fx  # Pitch correction (X axis)
            omega_y = -self.K_p_orient * Fy  # Roll correction (Y axis)

            # Saturate angular velocities
            max_omega = 0.5  # rad/s
            omega_x = max(min(omega_x, max_omega), -max_omega)
            omega_y = max(min(omega_y, max_omega), -max_omega)

            # --- 4) Estimate current orientation (normal vector) ---
            theta_x = omega_x  # pitch (inclination around Y)
            theta_y = omega_y  # roll  (inclination around X)

            tan_x = math.tan(theta_x)
            tan_y = math.tan(theta_y)

            # Non-normalized normal vector
            nx = -tan_y
            ny = -tan_x
            nz = 1.0

            norm = math.sqrt(nx**2 + ny**2 + nz**2)

            # Normalized normal vector
            nx /= norm
            ny /= norm
            nz /= norm

            # Velocity projected along normal direction
            vx_f = vf_mag * nx
            vy_f = vf_mag * ny
            vz_cmd = vf_mag * nz

            # Saturate Z velocity
            max_vz = 0.1  # m/s
            vz_cmd = max(min(vz_cmd, max_vz), -max_vz)

            # --- 4) Circular XY trajectory with force adjustments ---
            t_now = time.time() - self.start_time
            vx_nominal = self.radius * math.sin(self.omega * t_now) * self.omega
            vy_nominal = self.radius * math.cos(self.omega * t_now) * self.omega

            sin_ox = math.sin(omega_x)
            cos_ox = math.cos(omega_x)
            sin_oy = math.sin(omega_y)
            cos_oy = math.cos(omega_y)

            vx_cmd = vx_nominal 
            vy_cmd = vy_nominal

            # Saturate X and Y velocities
            max_vxy = 0.1  # m/s
            vx_cmd = max(min(vx_cmd, max_vxy), -max_vxy)
            vy_cmd = max(min(vy_cmd, max_vxy), -max_vxy)

            # --- 7) Build and publish TwistCommand message ---           
            if (reference_frame == 2):
                twist_cmd.twist.linear_x = 1*(vy_cmd + 0*vy_f )  # Y component
                twist_cmd.twist.linear_y = 1*(vx_cmd + 0*vx_f)   # X component
                twist_cmd.twist.linear_z = vz_cmd
                twist_cmd.twist.angular_x = omega_x  
                twist_cmd.twist.angular_y = omega_y  
                twist_cmd.twist.angular_z = 0.0      

            else:
                twist_cmd.twist.linear_x = vx_cmd + vx_f
                twist_cmd.twist.linear_y = vy_cmd + vy_f
                twist_cmd.twist.linear_z = -vz_cmd
                twist_cmd.twist.angular_x = omega_y 
                twist_cmd.twist.angular_y = omega_x  
                twist_cmd.twist.angular_z = 0.0    

            print(" Time:%.3f  Fz=%.3f | Fx=%.3f | Fy=%.3f |+| cm/s -> vz=%.3f | vx=%.3f | vy=%.3f |+| Rad omega_x=%.3f | omega_y=%.3f" 
                % (t_now, Fz, Fx, Fy, vz_cmd*100, vx_cmd*100, vy_cmd*100, omega_x, omega_y))
            
            if(t_now>=self.loops*self.time_exp):
                self.end = True
                self.experiment = False
                self.time_final = time.time()
               
        # ---- End phase: retreat ----
        elif(self.end):
            t_end = time.time() - self.time_final
            if (t_end < 2.0):
                if (reference_frame == 2):
                    twist_cmd.twist.linear_x = 0.0
                    twist_cmd.twist.linear_y = 0.0
                    twist_cmd.twist.linear_z = -0.01
                    twist_cmd.twist.angular_x = 0.0
                    twist_cmd.twist.angular_y = 0.0 
                    twist_cmd.twist.angular_z = 0.0      
                else:
                    twist_cmd.twist.linear_x = 0.0
                    twist_cmd.twist.linear_y = 0.0
                    twist_cmd.twist.linear_z = 0.01
                    twist_cmd.twist.angular_x = 0.0
                    twist_cmd.twist.angular_y = 0.0 
                    twist_cmd.twist.angular_z = 0.0  
            else:
                twist_cmd.twist.linear_z = 0.00

        self.cmd_pub.publish(twist_cmd)

def main():
    rospy.init_node('impedance_controller', anonymous=False)
    controller = ImpedanceController()
    rate = rospy.Rate(controller.loop_rate_hz)

    while not rospy.is_shutdown():
        controller.control_loop()
        rate.sleep()

if __name__ == '__main__':
    main()
