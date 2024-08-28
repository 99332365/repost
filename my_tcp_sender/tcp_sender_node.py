

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose  # Importez le message Pose de Turtlesim
import socket
import time
import random

class TcpSenderNode(Node):
    def __init__(self):
        super().__init__('tcp_sender_node')

        # Configuration de la connexion TCP avec le FiPy
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fipy_ip = '10.89.2.196'  # Adresse IP du FiPy
        self.fipy_port = 1234

        self.get_logger().info('Connexion au FiPy...')
        self.client_socket.connect((self.fipy_ip, self.fipy_port))
        self.get_logger().info('Connecté au FiPy')

        # Souscription au topic /turtle1/pose pour obtenir la position réelle de la tortue
        self.pose_subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Stockage de la dernière position connue
        self.current_position = None

        # Timer pour envoyer les données de température et de position
        self.create_timer(2.0, self.send_temperature_data)
        self.create_timer(5.0, self.send_position_data)

    def pose_callback(self, msg):
        # Mettre à jour la position actuelle avec les données de pose de la tortue
        self.current_position = msg

    def send_temperature_data(self):
        # Simulation d'une donnée de température aléatoire
        temperature = random.uniform(20.0, 30.0)
        message = f'Temperature: {temperature:.2f}'
        self.client_socket.send(message.encode())
        self.get_logger().info(f'Donnée de température envoyée: {message}')

    def send_position_data(self):
        # Envoyer la position réel 
        if self.current_position is not None:
            position = (self.current_position.x, self.current_position.y)
            message = f'Position: {position[0]:.2f}, {position[1]:.2f}'
            self.client_socket.send(message.encode())
            self.get_logger().info(f'Donnée de position envoyée: {message}')
        else:
            self.get_logger().warn('Position non disponible')

def main(args=None):
    rclpy.init(args=args)
    node = TcpSenderNode()
    
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()