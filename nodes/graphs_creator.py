import numpy as np
import matplotlib.pyplot as plt


class GraphsCreator:
    def __init__(self,  icp, odom, saved_times):
        self.icp = np.array(icp)
        self.odom = np.array(odom)
        self.saved_times = saved_times

    def create_graph_xy_and_point_cloud(self, point_cloud):
        output_path = "/home/robert/catkin_ws/src/bag_crawler/web_server/shared_point_cloud.png"
        fig, ax = plt.subplots()
        marker_size = 0.5
        plt.xlabel('X-coordinate')
        plt.ylabel('Y-coordinate')
        plt.title("XY plot of UGV's movement")
        combined_points = np.concatenate(point_cloud, axis=1)
        colors = self.transform_z_coordinates_to_color(combined_points[2, :])
        ax.scatter(combined_points[0, :], combined_points[1, :], s=marker_size, c=colors, cmap='Greens')
        self.icp = self.move_coordinates_to_the_origin(self.icp)
        self.odom = self.move_coordinates_to_the_origin(self.odom)
        ax.plot(self.odom[:, 0], self.odom[:, 1], color='blue', label='imu_odom')
        ax.plot(self.icp[:, 0], self.icp[:, 1], color='red', linestyle='--', label='icp_odom')
        plt.legend()
        plt.savefig(output_path)
        plt.close()

    def create_graph_x_over_time(self):
        output_path = "/home/robert/catkin_ws/src/bag_crawler/web_server/coord_x_and_time.png"
        fig, ax = plt.subplots()
        plt.xlabel('time [s]')
        plt.ylabel('distance[m]')
        plt.title("UGV's movement in X direction")
        ax.plot(self.saved_times, self.move_coordinates_to_the_origin(self.odom[:, 0]), color='blue')
        ax.plot(self.saved_times, self.move_coordinates_to_the_origin(self.icp[:, 0]), color='red', linestyle='--')
        plt.savefig(output_path)
        plt.close()

    def create_graph_y_over_time(self):
        output_path = "/home/robert/catkin_ws/src/bag_crawler/web_server/coord_y_and_time.png"
        fig, ax = plt.subplots()
        plt.xlabel('time [s]')
        plt.ylabel('distance[m]')
        plt.title("UGV's movement in Y direction")
        ax.plot(self.saved_times, self.move_coordinates_to_the_origin(self.odom[:, 1]), color='blue')
        ax.plot(self.saved_times, self.move_coordinates_to_the_origin(self.icp[:, 1]), color='red', linestyle='--')
        plt.savefig(output_path)
        plt.close()

    def create_graph_z_over_time(self):
        output_path = "/home/robert/catkin_ws/src/bag_crawler/web_server/coord_z_and_time.png"
        fig, ax = plt.subplots()
        plt.xlabel('time [s]')
        plt.ylabel('distance[m]')
        plt.title("UGV's movement in Z direction")
        ax.plot(self.saved_times, self.move_coordinates_to_the_origin(self.odom[:, 2]), color='blue')
        ax.plot(self.saved_times, self.move_coordinates_to_the_origin(self.icp[:, 2]), color='red', linestyle='--')
        plt.savefig(output_path)
        plt.close()

    def create_graph_distance_over_time(self, distances_icp, distances_odom, start_of_moving, end_of_moving):
        output_path = "/home/robert/catkin_ws/src/bag_crawler/web_server/distance_and_time.png"
        fig, ax = plt.subplots()
        plt.xlabel('time [s]')
        plt.ylabel('distance[m]')
        plt.title("UGV's travelled distance over time")
        ax.plot(self.saved_times, distances_odom, color='blue')
        ax.plot(self.saved_times, distances_icp, color='red', linestyle='--')
        ax.axvline(start_of_moving, color='green', linestyle=':', label='start_of_moving')
        ax.axvline(end_of_moving, color='green', linestyle='--', label='end_of_moving')
        plt.legend()
        plt.savefig(output_path)
        plt.close()

    def create_graph_joy_control_times_and_icp(self, joy_control_coordinates):
        output_path = "/home/robert/catkin_ws/src/bag_crawler/web_server/joy_control_and_icp.png"
        fig, ax = plt.subplots()
        plt.xlabel('X-coordinate')
        plt.ylabel('Y-coordinate')
        plt.title("XY plot of UGV's movement along with joystick control trajectory sections")
        self.icp = self.move_coordinates_to_the_origin(self.icp)
        ax.plot(self.icp[:, 0], self.icp[:, 1], color='red', linestyle='--', label='icp_odom')
        for coordinates in joy_control_coordinates:
            ax.plot(coordinates[:, 0], coordinates[:, 1], color='orange')
            break
        ax.plot([], [], color='orange', label='joy_control')
        plt.legend()
        plt.savefig(output_path)
        plt.close()

    def create_binary_graph_joy_control_and_time(self, joy_control_binary):
        output_path = '/home/robert/catkin_ws/src/bag_crawler/web_server/control_joy_and_time.png'
        fig, ax = plt.subplots()
        ax.step(self.saved_times, joy_control_binary, color='orange', where='post')
        ax.set_xlabel('time')
        ax.set_ylabel('control joy')
        ax.set_title('Joystick robot control chart')
        ax.set_yticks([0, 1])
        plt.savefig(output_path)
        plt.close()

    def transform_z_coordinates_to_color(self, coord_z):
        coord_z += abs(np.min(coord_z))
        colors = np.log1p(coord_z)
        return colors

    def move_coordinates_to_the_origin(self, coordinates):
        return np.array(coordinates) - coordinates[0]


