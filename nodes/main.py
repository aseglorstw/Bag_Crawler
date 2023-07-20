import numpy as np

import rosbag
import topics_reader
import graphs_creator
import writer_to_files
import calculator


def main():
    path = '/home/robert/catkin_ws/src/bag_crawler/bagfiles/husky_2022-09-27-15-01-44.bag'
    #path = '/home/robert/catkin_ws/src/bag_crawler/bagfiles/husky_2022-09-23-12-38-31.bag'
    bag = rosbag.Bag(path)

    reader = topics_reader.Reader(bag)
    reader.load_buffer()
    point_cloud = reader.read_point_cloud()
    icp, odom, saved_times = reader.read_icp_odom()
    rotation_matrix_icp, rotation_matrix_odom, rotation_matrix_lidar = reader.get_first_rotation_matrices()
    # reader.read_images_and_save_video()
    #joy_control_times = reader.read_joy_topic()

    calc = calculator.Calculater(icp, odom, saved_times)
    # distances_icp = calc.get_distances(icp)
    # distances_odom = calc.get_distances(odom)
    # speeds = calc.get_speeds_one_period()
    # start_of_moving, end_of_moving = calc.get_start_and_end_of_moving()
    #joy_control_coordinates = calc.get_joy_control_coordinates(joy_control_times)
    #joy_control_binary = calc.get_joy_control_binary(joy_control_times)
    transformed_icp = calc.transform_trajectory(icp, rotation_matrix_icp)
    transformed_odom = calc.transform_trajectory(odom, rotation_matrix_odom)

    creator = graphs_creator.GraphsCreator(transformed_icp, transformed_odom, saved_times)
    # creator.create_graph_x_over_time()
    # creator.create_graph_y_over_time()
    # creator.create_graph_z_over_time()
    creator.create_graph_xy_and_point_cloud(point_cloud)
    # creator.create_graph_distance_over_time(distances_icp, distances_odom, start_of_moving, end_of_moving)
    #creator.create_graph_joy_control_times_and_icp(joy_control_coordinates)
    #creator.create_binary_graph_joy_control_and_time(joy_control_binary)

    #
    # writer = writer_to_files.Writer(bag, distances_icp[-1], start_of_moving, end_of_moving, speeds)
    # writer.write_topics_info()
    # writer.write_bag_info()

    bag.close()


if __name__ == '__main__':
    main()
