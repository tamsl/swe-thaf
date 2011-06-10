from movements import handle_movement,go_drive

def calc_speed():
    v = (current_speed*0.1650)/2
    return v
def calc_collision():
    c_t = front_ir /calc_speed()
    return c_t
ir_data = [2,3,4,5,6,7,]
front_ir = ir_data[int(len(ir_data)/2)]
print front_ir
sonar_data = []
odometry_data = []
## currentspeed moeten we ophalen.   
current_speed = 2
d = 16.50
print calc_speed()
print calc_collision()
handle_movement("forward", 5.0, 5.0)
handle_movement("right")
handle_movement("left")
handle_movement("brake")
handle_movement("reverse")


if calc_collision() <= 4 and front_ir <= 1.5 :
##  stuur bericht naar de movement dat de speed omlaag moet
    current_speed /2
    handle_movement("forward", 5.0, 5.0)
