# coding:utf-8

import pygame
import random
from random import randint
import sys

# 画布宽和长
WIDTH = 800
HEIGHT = 600
#　速度范围
SPEED = [10, 30]
# 字符串大小范围
SIZE = [5, 30]
# code长度范围
LEN = [1, 10]

# 随机生成一个颜色
def randomColor():
	return (randint(0, 255), randint(0, 255), randint(0, 255))

# 随机生成一个位置
def randomPos():
	return (randint(0, WIDTH), -10)

# 随机生成一个字符串
def randomCode():
	return random.choice('ASDASARsdgsrhad56768513asar35a4sr684a3s51ra4r344sgs8484')

# 定义代码精灵类
class Code(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.Font('./font.ttf', randint(SIZE[0], SIZE[1]))
		self.speed = randint(SPEED[0], SPEED[1])
		self.code = self.getCode()
		self.image = self.font.render(self.code, True, randomColor())
		self.image = pygame.transform.rotate(self.image, randint(87, 93))
		self.rect = self.image.get_rect()
		self.rect.topleft = randomPos()

	def getCode(self):
		length = randint(LEN[0], LEN[1])
		code = ''
		for i in range(length):
			code += randomCode()
		return code

	def update(self):
		self.rect = self.rect.move(0, self.speed)
		if self.rect.top > HEIGHT:
			self.kill()

pygame.init()
# 背景颜色
bg_color = (1, 1, 1)
# 设置画布大小
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# 获取窗口标题
pygame.display.set_caption('有意思的代码雨')
clock = pygame.time.Clock()
codesGroup = pygame.sprite.Group()
while True:
	clock.tick(24)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
	screen.fill(bg_color)
	codeobject = Code()
	codesGroup.add(codeobject)
	codesGroup.update()
	codesGroup.draw(screen)
	pygame.display.update()