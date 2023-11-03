import sys, pygame

from classes.obj import OBJ
from utils.debug import debug

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

obj = OBJ("xyzcube.obj")

class Program:
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.LMB = False
        self.RMB = False
        self.wireframe = True
        self.normals = False
        self.translation = False
        self.rotation = False
        self.x = False
        self.y = False
        self.z = False
        self.angle = 1.0
        self.scale = 100

    def run(self):
        while True:
            #region EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                #region KEYS
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()

                    # select mode: translation/rotation
                    if keys[pygame.K_n]:
                        if self.normals: 
                            self.normals = False
                        else:
                            self.normals = True
                    if keys[pygame.K_q]:
                        if self.rotation: 
                            self.rotation = False
                        if self.translation:
                            self.translation = False
                        else:
                            self.translation = True
                    if keys[pygame.K_r]:
                        if self.translation:
                            self.translation = False
                        if self.rotation:
                            self.rotation = False
                        else:
                            self.rotation = True

                    # change rotation axis
                    if keys[pygame.K_x]:
                        if self.x: self.x = False
                        else:      self.x = True
                    if keys[pygame.K_y]:
                        if self.y: self.y = False
                        else:      self.y = True
                    if keys[pygame.K_z]:
                        if self.z: self.z = False
                        else:      self.z = True
                    
                    # change rotation angle (still spinning crazy af)
                    if keys[pygame.K_UP]:
                        self.angle += 0.1
                    if keys[pygame.K_DOWN]:
                        self.angle -= 0.1
                    
                    # toggle wireframe mode
                    if keys[pygame.K_1]:
                        if self.wireframe:
                            self.wireframe = False
                        else:
                            self.wireframe = True

                # toggle current action
                # hold LMB to perform currently selected operations
                if event.type == pygame.MOUSEBUTTONDOWN:
                        keys = pygame.mouse.get_pressed()
                        if keys[0] and not self.LMB:
                            self.LMB = True
                        if keys[2] and not self.RMB:
                            self.RMB = True

                if event.type == pygame.MOUSEBUTTONUP:
                    keys = pygame.mouse.get_pressed()
                    if not keys[0] and self.LMB:
                        self.LMB = False
                    if not keys[0] and self.RMB:
                        self.RMB = False
                
                # change model scale
                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        self.scale += 3
                    if event.y > 0:
                        self.scale -= 3
                #endregion KEYS
            #endregion EVENTS

            #region UPDATE

            obj.update([self.LMB, self.RMB], self.angle, 
                       [self.translation, self.rotation], 
                       [self.x, self.y, self.z])
            
            #endregion UPDATE

            #region RENDER

            screen.fill("black")
            obj.render(self.display, self.wireframe, self.normals, self.scale)

            # render debug info
            debug(f"Move: {'On' if self.translation else 'Off'}, Rotate: {'On' if self.rotation else 'Off'}")
            debug(f"Wireframe: {'On' if self.wireframe else 'Off'}, Normals: {'On' if self.normals else 'Off'}", 30, 10)
            debug(f"X: {'On' if self.x else 'Off'}, Y: {'On' if self.y else 'Off'}, Z: {'On' if self.z else 'Off'}, Scale: {self.scale}, Angle: {self.angle}", 50, 10)
            debug(f"FPS:{clock.get_fps()}", 70, 10)
            pygame.display.update()

            #endregion RENDER
            
            clock.tick(60)


if __name__ == "__main__":
    Program().run()