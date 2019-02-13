# OBDIIPy
## Warning
This project is highly experimental. Do not use on your daily expensive cars.

Trouble codes and descriptions supplied with this source code have
been obtained from various sources and reformatted for use in this
application. The original data may be erroneous and the reformatting
process may have introduced errors into the codes or descriptions. The ties
between the codes and the descriptions may also have been effected and
made erroneous. As such any part of this software or data may provide
invalid or misguiding data or cause harm. Use this software and data at
your own risk, no guarantees or warranties are provided with the software
and data and absolutely no responsibility will be taken for and issues or
damage caused during the installation or use of the software or data.

Never use a vehicle on a public road with a device connected to the OBDII
port or any other part of the CAN BUS. The CAN BUS is used to run the engine,
any issues on the CAN BUS while the engine is running may effect the running
of the engine or even damage the engine. 

I am not responsible for bricked ECUs, dead SD cards, thermonuclear war, 
or you getting fired because the car failed. Please do some research if you 
have any concerns about features included in this project before using it! 
YOU are choosing to make these modifications, and if you point the finger at us 
for messing up your car, we will laugh at you.

Do not use fake devices, there are reports that they can cause damage.
https://obd-car-doctor.com/en-us/thread/Attention-Bad-Bluetooth-adapters-/

## Requirements
This application has been tested with a Original USB ELM327 OBDII cable and a Original
Bluetooth ELM327 OBDII dongle.

```
sudo apt-get install python3
sudo apt-get install python3-serial
sudo apt-get install python3-pygame
sudo apt-get install python3-pypdf2
sudo apt-get install python3-reportlab
```

## Optional for printer support, currently untested:
```
sudo apt-get install lpr
```

## Optional for opening and reading PDF files from Raspbian:
```
sudo apt-get install evince
```
## Packages for Bluetooth Serial dongle
```
sudo apt-get install bluez
sudo apt-get install bluetoothd
```

## Start application from the command line:
```
chmod +x OBDIIPy.py
sudo ./OBDIIPy.py
```
OR:
```
sudo python3 OBDIIPy.py
```

## Adding Missing PID Support
Additional PID code support may have been added over time. But
for other vehicles there may be missing supported PID codes. To add support
for a PID code, add the PID code to the ELM327 class using existing PID source
code as a guide. And check the formatting of the data in the PID text file
definitions.

## What does this mean for other vehicles

The trouble code reporting is standard to the OBDII protocol. So trouble code
reporting should work. There are standard ISO trouble code descriptions which
apply to all vehicles, these descriptions are present, and will be displayed
with the trouble codes reported. Vehicle specific trouble codes will be
reported, but with the description "[NO DESCRIPTION]", so you will still see
the trouble code numbers which you can look up, or provide a lookup table for
your own vehicle. You can send pull requests for codes.

The most common PIDs are supported, such as vehicle speed, engine speed, engine
temperature, ... Any unsupported PIDs should appear with an unsupported message.
You should be able to add them in the ELM327.py file. I am unlikely to have
time to add them, but you can report them as missing and if I have time I will
attempt to add them if you reply as to if they are working correctly after.

## Bluetooth service
Get the status of the Bluetooth service.
```
sudo service bluetooth status
```

If the Bluetooth service is not running, start it.
```
sudo service bluetooth start
```

Stop the Bluetooth service only if required.
```
sudo service bluetooth stop
```

## Pairing a Bluetooth device
Once a device is paired it should automatically pair in future.


Start the Bluetooth utility.
```
bluetoothctl
```

Make sure the Bluetooth device is powered on.
```
power on
```

Make sure an agent is running for the Bluetooth device.
```
agent on
```

Start a scan for other Bluetooth devices in the area.
```
scan on
```

Wait for the required Bluetooth device to be reported...

Stop scanning when the required Bluetooth device is found.
```
scan off
```

Attempt to pair the required Bluetooth device.
```
pair <dev>
```
e.g. \<dev> = 00:1D:A5:F7:FF:0D

Pairing normally prompts for a password. Standard Bluetooth pairing passwords
are: 0000 or 1234, try these if you are unsure of the password.

If parinig fails or propt for password does not appear, try the following, and
then try paring again.
```
agent off
power off
power on
agent on
```

Once paired it should appear in the list of paired devices.
```
paired-devices
```

You can now leave the Bluetooth utility and the device should be paired and
ready for use.
```
quit
```

## Creating a serial device for use in the OBDII application

rfcomm associates the paired device ID with a serial device name.
```
rfcomm bind 0 <dev>
```

The device it should create is:
```
/dev/rfcomm0
```

To remove the serial device do the following if required.
```
rfcomm release <dev>
```

You shouldn't need this command, force rfdevices to stop.
```
rfkill list
```

## Unpairing a Bluetooth device

Start the Bluetooth utility.
```
bluetoothctl
```

Unpair the Bluetooth device if required.
```
remove <dev>
```

Make sure the agent is stopped for the Bluetooth device.
```
agent off
```

Make sure the Bluetooth device is powered down.
```
power off
```
Exit the Bluetooth utility.
```
quit
```

## About clone ELM devices

If the MAC address of your adapter starts with the numbers 66:35:56: ...  or 88:35:56:...(for example, 66:35:56:78:90:AB)
 
* 00:00:00:00:00:01
* AA:BB:CC:11:22:33
* 00:00:00:11:11:11 (fresh example from 2018 garbage collection, marked as version 1.5)
* some other "strange looking" addresses

be prepared that this adapter could fail to connect, support not all protocols, fail to 
read some data and what's more, they can cause problems with your car.

There are also some adapters that might be almost good while working with single ECU and 
short commands, but could fail to get reliable results for cars with 2 and more ECUs and 
"long" commands like VIN or DTC readings