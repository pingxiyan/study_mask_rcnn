# README
Image segment calibration tool, which use python3 and OpenCV to implement.

# Dependency

	Python3
	OpenCV
	
# Get Started

	calibration.py [image_path]

	Categories loop:
	Arrow key ** Left **  : draw curve thickness decrease 2 pixels.
	Arrow key ** Right **  : draw curve thickness increase 2 pixels.
	Arrow key ** Up **  : Previous category.
	Arrow key ** Down **  : Next category.
	Key: ** 'q' or 'Esc' ** : Exit categories loop, and enter into image loop.
	
	Image loop:
	Arrow key ** Up **  : Previous image, and then enter into Categories loop.
	Arrow key ** Down **  : Next image, and then enter into Categories loop.
	Key: ** 'q' or 'Esc' ** : Exit calibartion tool.