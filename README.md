# MashPi
This repo is for my brew controller software for a brutus-10 style, single tier, three vessel HERMS brewery.    As of Jan '15, it only supports monitoring and charting of HLT and Mash temps using DS temp probes, a raspberry pi B+ and streaming plots from plot.ly   Control etc is currently done by a PID device on my setup, but I plan to move PID control to the PI soon.

Setup:  (Lazily written... go look it up yourself.) 

Hardware: 
Look on youtube for any of the tutorials on wiring DS one wire temperature probes to the GPIO on a raspberry pi.  They work in series with unique ids. This code supports two at the moment. 

https://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi

I connect my Pi to my home network using a wifi dongle and then access the streaming plots via a web browser on an ipad.  


Software:
Install python, pip etc.   Follow instructions for plot.ly setup online. 

Set up a Plot.ly account and replace the api keys and stream ids at the beginning of the code. 

You may want to play with the timedelta in the code to adjust it to your timezone.  It is set to PST by default.

You may want to read in the target temp from the command line.  I hardcoded to 152F.

This setup might be useful for home brewers because you can record and visualize the effects of different hardware setups on the thermal efficiency of your setup.  For example, changing the length of a tube, insulating a mash tun, getting a different lid, etc etc.


*** Feedback is welcomne, but please remember I only spent a few minutes on this.  It seems to work ok, but is likel to have issues that I have missed ***

cheers