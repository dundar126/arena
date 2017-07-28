# Downslope calculation
def downslope(x, left, right):
	return (right - x) / (right - left)


# Upslope calculation
def upslope(x, left, right):
	return (x - left) / (right - left)


# Close membership
def mem_close(x):
	left = 0
	right = 4

	if x <= left:
		return 1
	elif x >= right:
		return 0
	else:
		return downslope(x, left, right)


# Medium membership
def mem_medium(x):
	upleft = 3
	upright = 4
	downleft = 5
	downright = 6

	if x < upleft:
		return 0
	elif (x > upleft) and (x < upright):
		return upslope(x, upleft, upright)
	elif (x > downleft) and (x < downright):
		return downslope(x, downleft, downright)
	elif x > downright:
		return 0
	else:
		return 1


# Far membership
def mem_far(x):
	left = 7
	right = 8

	if x <= left:
		return 0
	elif x >= right:
		return 1
	else:
		return upslope(x, left, right)


# Low health membership
def mem_health_low(x):
	left = 0
	right = 30

	if x <= left:
		return 1
	elif x >= right:
		return 0
	else:
		return downslope(x, left, right)


# Low-medium health membership
def mem_health_low_med(x):
	upleft = 20
	upright = 40
	downleft = 50
	downright = 60

	if x < upleft:
		return 0
	elif (x > upleft) and (x < upright):
		return upslope(x, upleft, upright)
	elif (x > downleft) and (x < downright):
		return downslope(x, downleft, downright)
	elif x > downright:
		return 0
	else:
		return 1


# High-medium health membership
def mem_health_high_med(x):
	upleft = 50
	upright = 60
	downleft = 70
	downright = 80

	if x < upleft:
		return 0
	elif (x > upleft) and (x < upright):
		return upslope(x, upleft, upright)
	elif (x > downleft) and (x < downright):
		return downslope(x, downleft, downright)
	elif x > downright:
		return 0
	else:
		return 1


# High health membership
def mem_health_high(x):
	left = 70
	right = 90

	if x <= left:
		return 0
	elif x >= right:
		return 1
	else:
		return upslope(x, left, right)


# Range
def get_range(x):
	x_close = round(mem_close(x), 3)
	x_medium = round(mem_medium(x), 3)
	x_far = round(mem_far(x), 3)
	max_membership = max(x_close, x_medium, x_far)

	membership = ""
	if max_membership == x_close:
		membership = "close"
	elif max_membership == x_medium:
		membership = "medium"
	else:
		membership = "far"

	return membership


# Health
def get_health(x):
	x_low = round(mem_health_low(x), 3)
	x_low_med = round(mem_health_low_med(x), 3)
	x_high_med = round(mem_health_high_med(x), 3)
	x_high = round(mem_health_high(x), 3)
	max_membership = max(x_low, x_low_med, x_high_med, x_high)

	membership = ""
	if max_membership == x_low:
		membership = "low"
	elif max_membership == x_low_med:
		membership = "low-medium"
	elif max_membership == x_high_med:
		membership = "high-medium"
	else:
		membership = "high"
	return membership


# Logic system
def logic_system(r, s):
	threat = ""
	range = get_range(r)
	health = get_health(s)

	if health == "high" and range == "close":
		threat = "medium"
	elif health == "high" and range == "medium":
		threat = "low"
	elif health == "high" and range == "far":
		threat = "low"
	elif health == "high-medium" and range == "close":
		threat = "high"
	elif health == "high-medium" and range == "medium":
		threat = "medium"
	elif health == "high-medium" and range == "far":
		threat = "low"
	elif health == "low-medium" and range == "close":
		threat = "high"
	elif health == "low-medium" and range == "medium":
		threat = "high"
	elif health == "low-medium" and range == "far":
		threat = "medium"
	elif health == "low" and range == "close":
		threat = "high"
	elif health == "low" and range == "medium":
		threat = "high"
	else:
		threat = "medium"

	return threat


