from graphics import Canvas
import random
import math
import time
    
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
GRAVITY = 0.15
MIN_SPEED_TO_SPLIT = 1.0
MIN_RADIUS_TO_SPLIT = 8

class Ball:
    # setting up the basic ball structure
    def __init__(self, canvas, x, y, r, vx, vy, color, mass = 1.0, generation = 0):
        # self = ball object
        # canvas = canvas. duh.
        # x, y = center coordinates of ball
        # r = radius of ball
        # vx, vy = velocity of ball in x and y directions, since it IS moving when alive
        # color = color of ball
        # mass = mass of ball
        # generation = I/ II/ III (no further descendants)
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.OGcolor= color # fixed color
        self.color = color  # changing color
        self.mass = mass
        self.generation = generation
        self.alive = True
        ######
        self.flash_timer = 0
        self.is_flashing = False
        ######
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, color)
    
    # ball animation/movement
    def update_position(self):
        # ded ball, no update
        if not self.alive:
            return

        # update coords using velocity
        self.x += self.vx
        self.y += self.vy

        # add gravity to the ball
        self.vy += GRAVITY

        # verrry slight air resistance? tbd whether to keep or not ######
        self.vx *= 0.999
        self.vy *= 0.999

        # bounce ball off canvas edges
        if self.x - self.r <= 0 or self.x + self.r >= CANVAS_WIDTH:
            # direction reverses and vx decreases (play around w this to see what feels suitable) ######
            self.vx *= -0.9
            ######
            if self.x - self.r <= 0:
                self.x = self.r
            if self.x + self.r >= CANVAS_WIDTH:
                self.x = CANVAS_WIDTH - self.r
            ######    
        
        if self.y - self.r <= 0:
            # vy at top does not decrease(reverses), vx, if any reduces by 0.2 (changeable)######
            self.y = self.r
            self.vy *= -1
            self.vx *= 0.8

        if self.y + self.r >= CANVAS_HEIGHT:
            # decrease speed in y-direction decently, bc gravity ######
            self.y = CANVAS_HEIGHT - self.r
            self.vy *= -0.6
            self.vx *= 0.8   

        # Start flashing when ball gets very slow
        if not self.is_flashing:
            speed = math.sqrt(self.vx**2 + self.vy**2)
            if speed < 0.5 and (self.y + self.r == CANVAS_HEIGHT):  # Very slow
                self.start_flash()
        
        # Handle flashing effect
        if self.is_flashing:
            self.canvas.set_color(self.id, '#f8f8f2')  # Turn white
            self.die()
            return
        
        # move that ball!!!
        canvas_x = self.x - self.r
        canvas_y = self.y - self.r
        self.canvas.moveto(self.id, canvas_x, canvas_y)    

    def start_flash(self):
        """Start the flashing death sequence"""
        if not self.is_flashing:
            self.is_flashing = True
            self.flash_timer = 0

    def die(self):
        """Remove ball from canvas"""
        self.canvas.delete(self.id)
        self.alive = False

    # split checker
    def should_split(self):
        #case where we do not want a split: generation OVER 3 
        if self.generation >= 3:
            return False
        if self.r < MIN_RADIUS_TO_SPLIT:
            return False
        
        speed = math.sqrt(self.vx**2 + self.vy**2)
        return speed > MIN_SPEED_TO_SPLIT and random.random() < 0.025

    # splitting tha ball
    def split(self):
        # call split checker
        if not self.should_split():
            return []

        # fragment the ball #### can also use random.randint (2,3) but lets see
        num_fragments = random.randint(2,3)
        fragments = []

        # new fragments radius definition
        frag_radius = max(self.r // 2, 5)

        for i in range(num_fragments):
            # defining the speed and angle of the fragmented balls
            angle = random.uniform(0, 2 * math.pi)
            speed = ((self.vx**2 + self.vy**2)**0.5)/num_fragments

            # defining the velocity of the balls
            frag_vx = speed * math.cos(angle)
            frag_vy = speed * math.sin(angle)

            # Slight position offset to prevent overlap
            offset_x = random.uniform(-self.r//3, self.r//3)
            offset_y = random.uniform(-self.r//3, self.r//3)

            # get the color for the fragments
            frag_color = self.get_fragment_color()
            
            # creating the fragments
            fragment = Ball(
                self.canvas, 
                self.x + offset_x, 
                self.y + offset_y, 
                frag_radius,
                frag_vx, 
                frag_vy, 
                frag_color,
                frag_radius / 10.0,
                self.generation + 1
            )

            # adding the fragments to the list for tracking!!
            fragments.append(fragment)

        # Remove OG ball 
        self.canvas.delete(self.id)
        self.alive = False

        return fragments 
        return []

    # setting the colors for the balls
    def get_fragment_color(self):
        if self.generation == 0:
            color = '#9fd3c7' 
        elif self.generation == 1:
            color = '#bbe4e9'
        elif self.generation == 2:
            color ='#e3f3f7'   
        return color           
    

# decide on the starting explosion point of the balls
def explosion_point():
    explode_x = random.uniform(CANVAS_WIDTH / 3, 2 * CANVAS_WIDTH / 3 )
    explode_y = random.uniform(CANVAS_HEIGHT / 4, CANVAS_HEIGHT / 2)

    return explode_x, explode_y

# starting explosion of the balls
def explosion(canvas, explode_x, explode_y, init_number=5):

    # tracking balls
    balls = []

    for j in range(init_number):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(4, 7)

        # Initial velocity of balls
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle) 

        # varying sizes of the balls
        r = random.randint(10, 15)

        #color list can be made hmm
        color = '#385170'

        ball = Ball(canvas, explode_x, explode_y, r, vx, vy, color, r/10.0, 0)
        balls.append(ball)
    
    return balls

# final game loop
def game_loop(canvas, balls):
    """Main game loop with splitting mechanics"""    
    while True:
        new_balls = []
        
        # Update all balls and check for splitting
        for ball in balls[:]:
            if ball.alive:
                ball.update_position()
                
                # Check if ball should split (only if still alive after update)
                if ball.alive:
                    fragments = ball.split()
                    if fragments:
                        new_balls.extend(fragments)
                        balls.remove(ball)
        
        # Add new fragments to ball list
        balls.extend(new_balls)
        
        # Remove dead balls
        balls[:] = [ball for ball in balls if ball.alive]
        
        # End program when all balls are dead
        if len(balls) == 0:
            print("All balls have died. Program ending.")
            break
        
        # Control frame rate
        time.sleep(0.016)  # ~60 FPS
    
def main():
    # setting up the canvas
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    #background of the game!
    background = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, '#ececec', 'white')

    #functions to set up the explosion ! & ST!
    explode_x, explode_y = explosion_point()
    balls = explosion(canvas, explode_x, explode_y)

    # here come the balls!
    game_loop(canvas, balls)

if __name__ == '__main__':
    main()