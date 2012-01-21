#!/usr/bin/env python

import liblo, sys, getpass, libardrone

# create server, listening on port 1234
class CommandData(liblo.Server):
    def __init__(self, port, debug = False):
        self.drone = libardrone.ARDrone()

        #ALT = self.drone.navdata['altitude']
        #print ALT
        print "Startup - trimming drone"
        self.drone.trim()

        try:
            super(CommandData, self).__init__(port)
            self.add_method("/command", 's', self.command_callback)
            
            # register a fallback for unhandled messages
            self.add_method(None, None, self.fallback)
            self.debug = debug
            
        except liblo.ServerError, err:
            print str(err)
            sys.exit()

    def command_callback(self, path, args):
        # self.drone.altitude()
        #ALT = self.tn.read_very_eager()
        #print ALT
        [s] = args
        print s
        if self.debug:
            print "Received command: '%s'" % s
        if s == 'takeoff':
            print "Takeoff\n"
            self.drone.takeoff()
            pass
        if s == 'landing':
            print "Landing\n"
            self.drone.land()
            pass
        if s == 'u':
            #self.drone.speedZ = 0.4
            self.drone.move_up()
        elif s == 'd':
            #self.drone.speedZ = -0.4
            #mode ar drone down...
            self.drone.move_down()
        if s == 'nu':
            #self.drone.speedZ = 0
            self.drone.move_down()
        elif s == 'nd':
            #self.drone.speedZ = 0
            #mode ar drone down...
            self.drone.move_up()
        elif s == 'f':
            #self.drone.speedY = -0.1
            # forward
            self.drone.move_forward()
            pass
        elif s == 'nf':
            #self.drone.speedY = 0.0
            self.drone.move_backward()
            # forward
            pass
        elif s == 'b':
            #self.drone.speedY = 0.1
            self.drone.move_backward()
            # back
            pass
        elif s == 'nb':
            self.drone.speedY = 0.1
            self.drone.move_forward()
            # back
            pass
        elif s == 'rr':
            #self.drone.speedYaw = -0.5
            # forward
            self.drone.turn_right()
            pass
        elif s == 'nrr':
            #self.drone.speedYaw = 0.0
            # forward
            self.drone.turn_left()
            pass
        elif s == 'rl':
            #self.drone.speedYaw = 0.5
            # back
            self.drone.turn_left()
            pass
        elif s == 'nrl':
            #self.drone.speedYaw = 0.0
            # back
            self.drone.turn_right()
            pass
        elif s == 'yl':
            #self.drone.speedX = -0.5
            # forward
            self.drone.move_left()
            pass
        elif s == 'nyl':
            #self.drone.speedX = 0.0
            # forward
            self.drone.move_right()
            pass
        elif s == 'yr':
            #self.drone.speedX = 0.5
            # back
            self.drone.move_right()
            pass
        elif s == 'nyr':
            #self.drone.speedX = 0.0
            # back
            self.drone.move_left()
            pass
    
    
    def fallback(self, path, args, types, src):
        if self.debug:
            print "got unknown message '%s' from '%s'" % (path, src.get_url())
            for a, t in zip(args, types):
                print "argument of type '%s': %s" % (t, a)


if __name__ == "__main__":
    # loop and dispatch messages every 100ms
    if len(sys.argv) == 2 and sys.argv[1] == "-h":
        print "Usage: ardrone.py [debug]"
        sys.exit(2)
    else:
        debug = False
        if len(sys.argv) > 1:
            debug = True
        server = CommandData(7111, debug)
        while True:
            try:
                server.recv(100)
            except KeyboardInterrupt:
                sys.exit(0)
