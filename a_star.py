import pygame, time, math

#fix confusing output
print("\n\n\n\n\n")

#grid
size = 550
count = 15

sep = 1
nss = size - (sep*(count+1))
sqr_size = nss / count

#clicks
left = False
right = False
e = False
e_num = 0
s = False
s_num = 0
shift = False
c = False

#a_star	
end = None
start = None
searched = []
found = False
current = []
ran = False

pygame.init()
display = pygame.display.set_mode((size,size))


def drawGrid(rect, node):
	if node == "closed":
		clr = (0, 0, 0)
	elif node == "open":
		clr = (255, 255, 255)
	elif node == "current":
		clr = (58, 194, 48)
	elif node == "searched":
		clr = (209, 33, 33)
	elif node == "start":
		clr = (52, 113, 235)
	elif node == "end":
		clr = (235, 207, 52)
	elif node == "path":
		clr = (39, 58, 184)
	else:
		clr = (207, 68, 212) #error color

	pygame.draw.rect(display, clr, rect)
	pygame.display.update()

def genGrid():
	global s_num, e_num
	grid = []

	for row in range(count):
		for col in range(count):
			pos = [sep + (sep + sqr_size)*row, sep + (sep + sqr_size)*col]
			grid.append([pygame.Rect(pos[0], pos[1], sqr_size, sqr_size), "open", [], [row+1, col+1], []])
			# FORMAT: [rect, class, costs, pos, prev]
			
			drawGrid(pygame.Rect(pos[0], pos[1], sqr_size, sqr_size), "open")
	return grid
grid = genGrid()



def clickedGrid(m_pos, button):
	global s_num, e_num, grid
	for sqr in grid:
		if sqr[0].collidepoint(m_pos):
			if button == "left":
				if sqr[1] == "start":
					s_num = 0
				if sqr[1] == "end":
					e_num = 0

				if s and s_num < 1:
					sqr[1] = "start"
					s_num += 1
				if e and e_num < 1:
					sqr[1] = "end"
					e_num += 1
					
				if not s and not e:
					sqr[1] = "closed"

			if button == "right":
				if sqr[1] == "start":
					s_num = 0
				if sqr[1] == "end":
					e_num = 0
				sqr[1] = "open"
		drawGrid(sqr[0], sqr[1])

def get_costs(cur):
	global end, start

	# dist formula = sqrt((x2-x1)^2 + (y2-y1)^2)
	e_cost = math.sqrt((cur[3][0] - start[3][0]) ** 2 + (cur[3][1] - start[3][1]) ** 2)
	e_cost = round(e_cost*10)
	f_cost = math.sqrt((cur[3][0] - end[3][0]) ** 2 + (cur[3][1] - end[3][1]) ** 2)
	f_cost = round(f_cost*10)
	g_cost = e_cost + f_cost			

	return [g_cost, e_cost, f_cost]


def a_star():
	global end, start, searched, found, ran

	#prevent running again
	ran = True
	
	#startup
	start, end = None, None
	found = False
	searched, current = [], []
	
	for sqr in grid:
		if sqr[1] == "start" and start == None:
			print("start")
			start = sqr
			current.append(sqr)
		elif sqr[1] == "end" and end == None:
			end = sqr

	while not found:
		#check for no solution
		if len(current) == 0:
			print("The end or beginning is completely blocked off!")
			return

		#get best
		best = None
		for cur in current:
			if len(cur[2]) == 0:
				cur[2] = get_costs(cur)

			if best == None:
				best = cur
			elif cur[2][0] < best[2][0]:
				best = cur
			elif cur[2][0] == best[2][0] and cur[2][2] < best[2][2]:
				best = cur

		best[1] = "searched"
		grid[grid.index(best)][1] = "searched"#synchronize
		current.remove(best)
		drawGrid(best[0], best[1])

		# get surrounding of best
		for sqr in grid:
			adjacent = False

			if sqr[3] == [best[3][0]+1, best[3][1]]:
				adjacent = True
			elif sqr[3] == [best[3][0]+1, best[3][1]+1]:
				adjacent = True
			elif sqr[3] == [best[3][0]+1, best[3][1]-1]:
				adjacent = True
			elif sqr[3] == [best[3][0]-1, best[3][1]+1]:
				adjacent = True
			elif sqr[3] == [best[3][0]-1, best[3][1]-1]:
				adjacent = True
			elif sqr[3] == [best[3][0]-1, best[3][1]]:
				adjacent = True
			elif sqr[3] == [best[3][0], best[3][1]-1]:
				adjacent = True
			elif sqr[3] == [best[3][0], best[3][1]+1]:
				adjacent = True

			if adjacent:
				if sqr[1] == "closed" or sqr[1] == "searched":
					continue
					
				#prev
				if sqr[1] == "open" or sqr[1] == "end":
					sqr[4] = grid.index(best)
				elif sqr[1] == "current":
					if len(sqr[2]) == 0:
						sqr[2] = get_costs(sqr)

					if sqr[2][1] > best[2][1]:
						sqr[4] = grid.index(best)

				if sqr[1] == "open":
					sqr[1] = "current"
					current.append(sqr)
					drawGrid(sqr[0], sqr[1])

				elif sqr[1] == "end":
					drawGrid(sqr[0], sqr[1])
					print("The fastest route has been found.")
					
					prev = end[4]
					back = False
					
					#go back through the bests
					while not back:
						
						nxt = grid[prev]
						nxt[1] = "path"
						prev = nxt[4]
						drawGrid(nxt[0], nxt[1])

						if nxt == start:
							back = True
						time.sleep(.128)

					print("Best route created")
					found = True
		time.sleep(.128)

while True:
	pygame.event.pump()
	events = pygame.event.get()
	
	for event in events:
		if event.type == pygame.QUIT:
			pygame.quit()

		if not ran:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					left = True
					clickedGrid(pygame.mouse.get_pos(), "left")
				elif event.button == 3:
					right = True
					clickedGrid(pygame.mouse.get_pos(), "right")
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					left = False
				elif event.button == 3:
					right = False
	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					s = True
				if event.key == pygame.K_e:
					e = True
				if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
					shift = True
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_s:
					s = False
				if event.key == pygame.K_e:
					e = False
				if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
					shift = False
				if event.key == pygame.K_r:
					if s_num == 1 and e_num == 1:
						a_star()

	if left and shift:
		clickedGrid(pygame.mouse.get_pos(), "left")
	if right and shift:
		clickedGrid(pygame.mouse.get_pos(), "right")

	try:
		pygame.display.update()
	except:
		break