import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import numpy as np

class Alvos(Node):

    def __init__(self):
        super().__init__('alvos')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.alvo1 = self.create_subscription(Odometry,'/alvo1/odometry',self.alvo1_callback,10)
        self.alvo1
        self.alvo2 = self.create_subscription(Odometry,'/alvo2/odometry',self.alvo2_callback,10)
        self.alvo2
        self.alvo3 = self.create_subscription(Odometry,'/alvo3/odometry',self.alvo3_callback,10)
        self.alvo3
        self.alvo4 = self.create_subscription(Odometry,'/alvo4/odometry',self.alvo4_callback,10)
        self.alvo4
        self.alvo5 = self.create_subscription(Odometry,'/alvo5/odometry',self.alvo5_callback,10)
        self.alvo5
        self.carro = self.create_subscription(Odometry,'/carrinho/odometry',self.carro_callback,10)
        self.carro
        self.modo1=False
        self.modo2=False
        self.modo3=False
        self.modo4=False
        self.modo5=False
        vel=Twist()
        vel.linear.x=2
        vel.linear.y=0
        vel.linear.z=0
        vel.angular.x=0
        vel.angular.y=0
    def alvo1_callback(self,msg):
        self.alvo1x=msg.pose.pose.position.x
        self.alvo1y=msg.pose.pose.position.y
    def alvo2_callback(self,msg):
        self.alvo2x=msg.pose.pose.position.x
        self.alvo2y=msg.pose.pose.position.y
    def alvo3_callback(self,msg):
        self.alvo3x=msg.pose.pose.position.x
        self.alvo3y=msg.pose.pose.position.y
    def alvo4_callback(self,msg):
        self.alvo4x=msg.pose.pose.position.x
        self.alvo4y=msg.pose.pose.position.y
    def alvo5_callback(self,msg):
        self.alvo5x=msg.pose.pose.position.x
        self.alvo5y=msg.pose.pose.position.y
    def carro_callback(self,msg):
        self.x=msg.pose.pose.position.x
        self.y=msg.pose.pose.position.y
        self.angx=msg.pose.pose.orientation.x
        self.angy=msg.pose.pose.orientation.y
        self.angz=msg.pose.pose.orientation.z
        self.angw=msg.pose.pose.orientation.w
        self.arco = math.asin(self.angz)
        self.ang = self.arco*2
        self.angc = np.degrees(self.ang)
        if (self.angw<0):
            self.angc=(-1)*(self.angc)

        self.vx1=self.alvo1x-self.x
        self.vy1=self.alvo1y-self.y
        self.tang1 = self.vy1/self.vx1
        self.ang1=math.atan(self.tang1)
        self.angg1 = np.degrees(self.ang1)
        if(self.vx1<0):
            self.angg1+=180
        self.d1=self.angg1-self.angc

        self.vx2=self.alvo2x-self.x
        self.vy2=self.alvo2y-self.y
        self.tang2 = self.vy2/self.vx2
        self.ang2=math.atan(self.tang2)
        self.angg2 = np.degrees(self.ang2)
        if(self.vx2>0):
            self.angg2+=180
        self.d2=self.angg2-self.angc

        self.vx3=self.alvo3x-self.x
        self.vy3=self.alvo3y-self.y
        self.tang3 = self.vy3/self.vx3
        self.ang3=math.atan(self.tang3)
        self.angg3 = np.degrees(self.ang3)
        if(self.vx3>0):
            self.angg3+=180
        self.d3=self.angg3-self.angc

        self.vx4=self.alvo4x-self.x
        self.vy4=self.alvo4y-self.y
        self.tang4 = self.vy4/self.vx4
        self.ang4=math.atan(self.tang4)
        self.angg4 = np.degrees(self.ang4)
        if(self.vx4>0):
            self.angg4+=180
        self.d4=self.angg4-self.angc

        self.vx5=self.alvo5x-self.x
        self.vy5=self.alvo5y-self.y
        self.tang5 = self.vy5/self.vx5
        self.ang5=math.atan(self.tang5)
        self.angg5 = np.degrees(self.ang5)
        if(self.vx5>0):
            self.angg5+=180
        self.d5=self.angg5-self.angc

        if(self.modo1==False):
            vel.angular.z=self.d1/12
        elif(self.modo2==False):
            vel.angular.z=self.d2/12
        elif(self.modo3==False):
            vel.angular.z=self.d3/12
        elif(self.modo4==False):
            vel.angular.z=self.d4/12
        elif(self.modo5==False):
            vel.angular.z=self.d5/12
        else:
            vel.angular.z=0
            vel.linear.x=0

        if(self.vx1<0.5 and self.vx1>-0.5 and self.vy1<0.5 and self.vy1>-0.5):
            self.modo1=True
        if(self.vx2<0.5 and self.vx2>-0.5 and self.vy2<0.5 and self.vy2>-0.5):
            self.modo2=True
        if(self.vx3<0.5 and self.vx3>-0.5 and self.vy3<0.5 and self.vy3>-0.5):
            self.modo3=True
        if(self.vx4<0.5 and self.vx4>-0.5 and self.vy4<0.5 and self.vy4>-0.5):
            self.modo4=True
        if(self.vx5<0.5 and self.vx5>-0.5 and self.vy5<0.5 and self.vy5>-0.5):
            self.modo5=True    

        self.publisher_.publish(vel)

def main(args=None):
    rclpy.init(args=args)
    alvos = Alvos()
    rclpy.spin(alvos)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    alvos.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()

