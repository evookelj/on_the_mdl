import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """

    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1

    clear_screen(screen)
    t = new_matrix()
    ident(t)
    systems = [ t ]

    step = 0.1
    c = 0

    for command in commands:
        cmd = command[0]
        args = command[1:]
        if cmd == 'sphere':
            #print 'SPHERE\t' + str(args)
            edges = []
            add_sphere(edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult( systems[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []

        elif cmd == 'torus':
            #print 'TORUS\t' + str(args)
            edges = []
            add_torus(edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step)
            matrix_mult( systems[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
            
        elif cmd == 'box':
            #print 'BOX\t' + str(args)
            edges = []
            add_box(edges,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( systems[-1], edges )
            draw_polygons(edges, screen, color)
            edges = []
            
        elif cmd == 'circle':
            #print 'CIRCLE\t' + str(args)
            edges = []
            add_circle(edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            edges = []

        elif cmd == 'hermite' or cmd == 'bezier':
            #print 'curve\t' + line + ": " + str(args)
            add_curve(edges,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step, line)                      
            
        elif cmd == 'line':            
            #print 'LINE\t' + str(args)

            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )

        elif cmd == 'scale':
            #print 'SCALE\t' + str(args)
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]

        elif cmd == 'move':
            #print 'MOVE\t' + str(args)
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]


        elif cmd == 'rotate':
            #print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)
            
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( systems[-1], t )
            systems[-1] = [ x[:] for x in t]
                
        elif cmd == 'clear':
            edges = []
            
        elif cmd == 'ident':
            ident(transform)

        elif cmd == 'apply':
            matrix_mult( transform, edges )

        elif cmd == 'push':
            systems.append( [x[:] for x in systems[-1]] )
            
        elif cmd == 'pop':
            systems.pop()
            
        elif cmd == 'display' or cmd == 'save':
            if cmd == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])