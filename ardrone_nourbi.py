#!/usr/bin/env python

import liblo, sys, getpass, libardrone

# create server, listening on port 1234
class CommandData(liblo.Server):
    def __init__(self, port, debug = False):
        self.drone = libardrone.ARDrone()

        #ALT = self.drone.navdata['altitude']
        #print ALT
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


        if s == 'emergency':
            print "Emergency\n"
            self.drone.reset()
        elif s == 'takeoff':
            print "Takeoff\n"
            self.drone.takeoff()
        elif s == 'landing':
            print "Landing\n"
            self.drone.land()
        elif s == 'trim':
            print "Trim\n"
            self.drone.trim()

        # Move up
        if s == 'u':
            self.drone.set_speed_updown(0.5)
        elif s == 'nu':
            self.drone.set_speed_updown(0.0)

        # Move down
        elif s == 'd':
            self.drone.set_speed_updown(-0.4)
        elif s == 'nd':
            self.drone.set_speed_updown(0.0)

        # Move forward
        elif s == 'f':
            self.drone.set_speed_forwardback(-0.1)
        elif s == 'nf':
            self.drone.set_speed_forwardback(0.0)

        # Move back
        elif s == 'b':
            self.drone.set_speed_forwardback(0.1)
        elif s == 'nb':
            self.drone.set_speed_forwardback(0.0)

        # Rotate right
        elif s == 'rr':
            self.drone.set_speed_yaw(0.5)
        elif s == 'nrr':
            self.drone.set_speed_yaw(0.0)

        # Rotate left
        elif s == 'rl':
            self.drone.set_speed_yaw(-0.5)
        elif s == 'nrl':
            self.drone.set_speed_yaw(0.0)

        # Move left
        elif s == 'yl':
            self.drone.set_speed_leftright(-0.1)
        elif s == 'nyl':
            self.drone.set_speed_leftright(0.0)

        # Move right
        elif s == 'yr':
            self.drone.set_speed_leftright(0.1)
        elif s == 'nyr':
            self.drone.set_speed_leftright(0.0)

        # Change video feed mode (front, lower, 2x PiP)
        elif s == 'vid_front':
            self.drone.set_video_mode('front')
        elif s == 'vid_lower':
            self.drone.set_video_mode('lower')
        elif s == 'vid_pip_front':
            self.drone.set_video_mode('pip_front')
        elif s == 'vid_pip_lower':
            self.drone.set_video_mode('pip_lower')
    
    # Safely shuts down the drone
    def shutdown(self):
        self.drone.halt()

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
                server.shutdown()
                sys.exit(0)
