# UR5Ing: Helping you figure out how to control this thing!
Basic scripts for remote/TCP control of UR robots.
This is mostly example code to help people who might want to control the UR5 robot from their computer using a very simple TCP server. 

It's important to know a couple of things:
- This repo manually sends urscript commands over TCP. UniversalRobots already has a fantastic package for remote Python work known as RDTE, for more complicated real-time robot control, you might want to check that out. 
- If you want to integrate websockets, you can create a JS/Node client and send messages using Python servers similar to this. 
- Note: Will add examples eventually. 
- You can also use RoboDK, which supports various UR robots. 

This repo was programmed and managed by:
Angelica Bonilla Fominaya 
Carnegie Mellon University. 2022