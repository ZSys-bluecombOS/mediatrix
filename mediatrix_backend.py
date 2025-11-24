from PIL import Image, ImageDraw, ImageFont
from math import floor

"""class MediaTrixScript():
	def __init__(self, script, environment = None):
		if environment == None:
			self.environment = {}
		elif type(environment) == dict:
			self.environment = environment

		self.code = script
		self.check_parentheses()
		self.commands()

	def commands(self, dictionary = None):
		if dictionary == None:
			dictionary = self.environment

		pass

	def check_parentheses(self):
		parentheses = []

		if self.code.split("\n")[0] == "":
			line_num = 0
		else:
			line_num = 1

		for char in self.code:
			if char in ["(", "[", "{"]:
				parentheses.append([char, line_num])
			elif char == ")" and parentheses[-1][0] == "(" or char == "]" and parentheses[-1][0] == "[" or char == "}" and parentheses[-1][0] == "{":
				del parentheses[-1]
			elif char == ")" and parentheses[-1][0] != "(" or char == "]" and parentheses[-1][0] != "[" or char == "}" and parentheses[-1][0] != "{":
				raise Exception(f"Parentheses mismatch at line {parentheses[-1][1]} (opened as {parentheses[-1][0]}, closed as {char})")
			elif char == "\n":
				line_num += 1

		if len(parentheses) != 0:
			raise Exception(parentheses)"""



class Mtx_Color():
	def __init__(self, mode, color, alpha_level = 255):
		if mode in ["sRGB", "sRGB hex"]:
			self.color = color
			self.mode = mode
		else:
			raise ValueError("Mtx_Color only supports sRGB as it currently stands")

		self.alpha_level = alpha_level

	def get_rgb_0_255(self):
		if self.mode == "sRGB":
			return tuple(self.color)
		elif self.mode == "sRGB hex":
			#print(self.color, int("aa", 16))
			#print(self.color[0:2], self.color[2:4], self.color[4:6])
			#print([int(self.color[(x*2):(x*2)+2], 16) for x in range(3)])
			return tuple([int(self.color[(x*2):(x*2)+2], 16) for x in range(3)])

	def get_rgb_0_1(self):
		if self.mode == "sRGB":
			return tuple([x/255 for x in self.color])
	
	def get_alpha_level(self, maximum = 255):
		return (self.alpha_level/255)*maximum



class Mtx_Image():
	class Mtx_Image_Layer():
		def __init__(self, size, pos, parent, base=Mtx_Color("sRGB", (0, 0, 0), 0)):
			self.xpos = pos[0]
			self.ypos = pos[1]
			self.visible = True

			if type(base) == Mtx_Color:
				self.base = Image.new("RGBA", (size[0], size[1]), (*base.get_rgb_0_255(), int(base.get_alpha_level())))
				self.width = size[0]
				self.height = size[1]
			elif type(base) == str:
				self.base = Image.open(base)

				if self.base.mode == "RGB":
					self.base.putalpha()

				self.width, self.height = self.base.size

			self.effects = []
			self.parent_image = parent
			self.parent_group = None
			self.__cache_regen()

		def __cache_regen(self):
			self.cache = self.base
			self.__effects_regen()

			if self.parent_group != None:
				self.parent_group._Mtx_Image_Group__cache_regen()

			self.parent_image._Mtx_Image__preview_regen()

		def __effects_regen(self):
			for item in self.effects:
				if item["type"] == "color_swap":
					image_load = self.cache.load()
					color1 = Mtx_Color(item["settings"]["color1"].split(" | ")[0], tuple([int(x) for x in item["settings"]["color1"].split(" | ")[1].split(", ")]), int(item["settings"]["color1"].split(" | ")[2]))
					color2 = Mtx_Color(item["settings"]["color2"].split(" | ")[0], tuple([int(x) for x in item["settings"]["color2"].split(" | ")[1].split(", ")]), int(item["settings"]["color2"].split(" | ")[2]))
					for i in range(self.width):
						for j in range(self.height):
							if image_load[i, j] == (*color1.get_rgb_0_255(), int(color1.get_alpha_level())):
								image_load[i, j] = (*color2.get_rgb_0_255(), int(color2.get_alpha_level()))

				elif item["type"] == "checkerboard":
					editable_new_layer = ImageDraw.Draw(self.cache)
					square_size = [int(x) for x in item["settings"]["square_size"].split(", ")]
					color1 = Mtx_Color(item["settings"]["color1"].split(" | ")[0], tuple([int(x) for x in item["settings"]["color1"].split(" | ")[1].split(", ")]), int(item["settings"]["color1"].split(" | ")[2]))
					color2 = Mtx_Color(item["settings"]["color2"].split(" | ")[0], tuple([int(x) for x in item["settings"]["color2"].split(" | ")[1].split(", ")]), int(item["settings"]["color2"].split(" | ")[2]))
					for i in range(self.width):
						for j in range(self.height):
							if i % int(square_size[0]*2) == 0 and j % int(square_size[1]*2) == int(square_size[1]) or i % int(square_size[0]*2) == int(square_size[0]) and j % int(square_size[1]*2) == 0:
								#print(i, j, square_size, square_size[1]*2, i % (square_size[1]+1), j % (square_size[0]+1))
								editable_new_layer.rectangle([i, j, i + square_size[0]-1, j + square_size[1]-1], fill=(*color2.get_rgb_0_255(), int(color2.get_alpha_level())))
							elif i % int(square_size[0]*2) == 0 and j % int(square_size[1]*2) == 0 or i % int(square_size[0]*2) == int(square_size[0]) and j % int(square_size[1]*2) == int(square_size[1]):
								editable_new_layer.rectangle([i, j, i + square_size[0]-1, j + square_size[1]-1], fill=(*color1.get_rgb_0_255(), int(color1.get_alpha_level())))

				elif item["type"] == "rotate":
					self.cache = self.cache.rotate(int(item["settings"]["angle"]), resample=Image.BICUBIC, expand=True)

				elif item["type"] == "rectangle":
					editable_new_layer = ImageDraw.Draw(self.cache)
					color1 = Mtx_Color(item["settings"]["color"].split(" | ")[0], tuple([int(x) for x in item["settings"]["color"].split(" | ")[1].split(", ")]), int(item["settings"]["color"].split(" | ")[2]))
					editable_new_layer.rectangle([int(item["settings"]["x"]), int(item["settings"]["y"]), int(item["settings"]["x"]) + int(item["settings"]["width"]), int(item["settings"]["y"]) + int(item["settings"]["height"])], fill=(*color1.get_rgb_0_255(), int(color1.get_alpha_level())))

				elif item["type"] == "auto_center_h":
					self.center_layer_horizontal(item["settings"]["placement"], item["settings"]["content_based"], item["settings"]["extra_shift"], from_effects_regen=True)

				elif item["type"] == "auto_center_v":
					self.center_layer_vertical(item["settings"]["placement"], item["settings"]["content_based"], item["settings"]["extra_shift"], from_effects_regen=True)

				elif item["type"] == "custom_code":
					exec(item["settings"]["code"])

		def color_swap(self, color1, color2):
			self.effects.append({"type": "color_swap", "settings": {"color1": f"{color1.mode} | {', '.join([str(x) for x in color1.color])} | {int(color1.get_alpha_level())}", "color2": f"{color2.mode} | {', '.join([str(x) for x in color2.color])} | {int(color2.get_alpha_level())}"}})
			self.__cache_regen()

		def checkerboard(self, square_size, color1, color2):
			self.effects.append({"type": "checkerboard", "settings": {"color1": f"{color1.mode} | {', '.join([str(x) for x in color1.color])} | {int(color1.get_alpha_level())}", "color2": f"{color2.mode} | {', '.join([str(x) for x in color2.color])} | {int(color2.get_alpha_level())}", "square_size": f"{square_size[0]}, {square_size[1]}"}})
			self.__cache_regen()

		def rotate(self, angle):
			self.effects.append({"type": "rotate", "settings": {"angle": f"{angle}"}})
			self.__cache_regen()

		def rectangle(self, x, y, width, height, color):
			self.effects.append({"type": "rectangle", "settings": {"x": f"{x}", "y": f"{y}", "width": f"{width}", "height": f"{height}", "color": f"{color.mode} | {', '.join([str(x) for x in color.color])} | {int(color.get_alpha_level())}"}})
			self.__cache_regen()

		def auto_center_horizontal(self, placement, content_based = False, extra_shift = 0):
			self.effects.append({"type": "auto_center_h", "settings": {"placement": placement, "content_based": content_based, "extra_shift": extra_shift}})
			self.__cache_regen()

		def auto_center_vertical(self, placement, content_based = False, extra_shift = 0):
			self.effects.append({"type": "auto_center_v", "settings": {"placement": placement, "content_based": content_based, "extra_shift": extra_shift}})
			self.__cache_regen()

		def custom_code(self, code):
			self.effects.append({"type": "custom_code", "settings": {"code": code}})
			self.__cache_regen()

		def center_layer_horizontal(self, placement, content_based = False, extra_shift = 0, from_effects_regen = False):
			if content_based == True:
				content_width = [10**10, 0, 10**10, 0]
				image_load = self.cache.load()

				for i in range(self.base.width):
					for j in range(self.base.height):
						if image_load[i, j][3] != 0 and i < content_width[0]:
							content_width[0] = i
						elif image_load[i, j][3] != 0 and i > content_width[1]:
							content_width[1] = i
						elif image_load[i, j][3] != 0 and j < content_width[2]:
							content_width[2] = j
						elif image_load[i, j][3] != 0 and j > content_width[3]:
							content_width[3] = j

				if placement == "left":
					self.xpos = 0 - content_width[0] + extra_shift
				elif placement == "center":
					self.xpos = floor((self.parent_image.width - (content_width[1] - content_width[0]))/2) - content_width[0] + extra_shift
				elif placement == "right":
					self.xpos = self.parent_image.width - (content_width[1] - content_width[0]) - content_width[0] + extra_shift
			else:
				if placement == "left":
					self.xpos = 0 + extra_shift
				elif placement == "center":
					self.xpos = floor((self.parent_image.width - self.base.width)/2) + extra_shift
				elif placement == "right":
					self.xpos = self.parent_image.width - self.base.width + extra_shift

			if from_effects_regen == False:
				self.__cache_regen()

		def center_layer_vertical(self, placement, content_based = False, extra_shift = 0, from_effects_regen = False):
			if content_based == True:
				content_width = [10**10, 0, 10**10, 0]
				image_load = self.cache.load()

				for i in range(self.base.width):
					for j in range(self.base.height):
						if image_load[i, j][3] != 0 and i < content_width[0]:
							content_width[0] = i
						elif image_load[i, j][3] != 0 and i > content_width[1]:
							content_width[1] = i
						elif image_load[i, j][3] != 0 and j < content_width[2]:
							content_width[2] = j
						elif image_load[i, j][3] != 0 and j > content_width[3]:
							content_width[3] = j

				if placement == "top":
					self.ypos = 0 - content_width[2] + extra_shift
				elif placement == "center":
					self.ypos = floor((self.parent_image.height - (content_width[3] - content_width[2]))/2) - content_width[2] + extra_shift
				elif placement == "bottom":
					self.ypos = self.parent_image.height - (content_width[3] - content_width[2]) - content_width[2] + extra_shift
			else:
				if placement == "top":
					self.ypos = 0 + extra_shift
				elif placement == "center":
					self.ypos = floor((self.parent_image.height - self.base.height)/2) + extra_shift
				elif placement == "bottom":
					self.ypos = self.parent_image.height - self.base.height + extra_shift

			if from_effects_regen == False:
				self.__cache_regen()



	class Mtx_Image_Text_Layer(Mtx_Image_Layer):
		def __init__(self, pos, text, font, color, size, parent, kerning = 0, line_gap = None, centering = "left", aliasing = False, extra_right_space = 0, extra_move_right = 0, rendering = "normal"):
			self.text = text
			self.xpos = pos[0]
			self.ypos = pos[1]
			self.visible = True
			self.font = font
			self.color = color
			self.size = size
			self.kerning = kerning
			self.line_gap = line_gap
			self.centering = centering
			self.aliasing = aliasing
			self.extra_right_space = extra_right_space
			self.extra_move_right = extra_move_right
			self.render_mode = rendering
			self.effects = []
			self.parent_image = parent
			self.parent_group = None
			self.__cache_regen()

		def __settings_handler(self, char, setting_name):
			if setting_name in self.kerning[char] or setting_name == "kerning":
				return self.kerning[char][setting_name]
			elif setting_name in ["xpos", "ypos", "font", "color", "size", "aliasing"]:
				return {"xpos": 0, "ypos": 0, "font": self.font, "color": self.color, "size": self.size, "aliasing": self.aliasing}[setting_name]

		def __base_regen(self):
			font = ImageFont.truetype(self.font, size=self.size)
			big_text = "".join([chr(x) for x in range(32, 256)])

			temp = Image.new("RGBA", (500, 500), (0, 0, 0, 0))
			temp_draw = ImageDraw.Draw(temp)

			if self.render_mode == "custom":
				simulated_width = [0] # This is per line, not in total
				simulated_height = 0
				x_pos = 0
				y_pos = 0

				# Copy of renderer but just all calculations

				if self.line_gap == None:
					line_gap = 0
				else:
					line_gap = self.line_gap

				for i, char in enumerate(self.text):
					if type(self.kerning) == dict and char in self.kerning and type(self.kerning[char]) == dict and self.__settings_handler(char, "font") != self.font:
						char_width = temp_draw.textbbox((0, 0), text=char, font=ImageFont.truetype(self.__settings_handler(char, "font"), size=self.__settings_handler(char, "size")))[2]
					else:
						char_width = temp_draw.textbbox((0, 0), text=char, font=font)[2]

					if char == "\n":
						y_pos += temp_draw.multiline_textbbox((0, 0), big_text, font=font)[3] + line_gap
						x_pos = 0
						simulated_width.append(0)
					else:
						if type(self.kerning) == dict and char in self.kerning and type(self.kerning[char]) == int:
							x_pos += self.kerning[char][-1]

						if type(self.kerning) == list:
							x_pos += char_width + self.kerning[i % len(self.kerning)]
						elif type(self.kerning) == int:
							x_pos += char_width + self.kerning
						else:
							x_pos += char_width

					# End of copy of renderer but just all calculations

					if x_pos + char_width > simulated_width[-1] and i+1 < len(self.text) and self.text[i+1] != "\n":
						simulated_width[-1] = x_pos + char_width
					if y_pos + temp_draw.multiline_textbbox((0, 0), big_text, font=font)[3] + line_gap > simulated_height:
						simulated_height = y_pos + temp_draw.multiline_textbbox((0, 0), big_text, font=font)[3] + line_gap

				self.base = Image.new("RGBA", (sorted(simulated_width, reverse=True)[0] + self.extra_right_space, simulated_height), (0, 0, 0, 0))
			else:
				if self.line_gap == None:
					self.base = Image.new("RGBA", (temp_draw.multiline_textbbox((0, 0), self.text, font=font)[2] + self.extra_right_space, temp_draw.multiline_textbbox((0, 0), "\n".join([big_text for x in range(len(self.text.split("\n")))]), font=font)[3]), (0, 0, 0, 0))
				else:
					self.base = Image.new("RGBA", (temp_draw.multiline_textbbox((0, 0), self.text, font=font, spacing=self.line_gap)[2] + self.extra_right_space, temp_draw.multiline_textbbox((0, 0), "\n".join([big_text for x in range(len(self.text.split("\n")))]), font=font, spacing=self.line_gap)[3]), (0, 0, 0, 0))

			draw = ImageDraw.Draw(self.base)
			if self.aliasing == True:
				draw.fontmode = "1"
			elif self.aliasing == False:
				draw.fontmode = "L"

			y_pos = 0
			line_num = 0

			if self.line_gap == None:
				line_gap = 0
			else:
				line_gap = self.line_gap

			if self.render_mode == "custom":
				if self.centering == "left":
					x_pos = self.extra_move_right
				elif self.centering == "center":
					x_pos = floor((self.base.width - simulated_width[line_num])/2) + self.extra_move_right
				elif self.centering == "right":
					x_pos = self.base.width - simulated_width[line_num] + self.extra_move_right

				for i, char in enumerate(self.text):
					if type(self.kerning) == dict and char in self.kerning and type(self.kerning[char]) == dict and self.__settings_handler(char, "font") != self.font:
						char_width = draw.textbbox((0, 0), text=char, font=ImageFont.truetype(self.__settings_handler(char, "font"), size=self.__settings_handler(char, "size")))[2]
					else:
						char_width = draw.textbbox((0, 0), text=char, font=font)[2]

					#print(char_width)

					if char == "\n":
						y_pos += draw.multiline_textbbox((0, 0), big_text, font=font)[3] + line_gap
						line_num += 1
						#print(simulated_width)

						if self.centering == "left":
							x_pos = self.extra_move_right
						elif self.centering == "center":
							x_pos = floor((self.base.width - simulated_width[line_num])/2) + self.extra_move_right
						elif self.centering == "right":
							x_pos = self.base.width - simulated_width[line_num] + self.extra_move_right

					else:
						#print(self.kerning)
						if type(self.kerning) == dict and char in self.kerning and type(self.kerning[char]) == int:
							x_pos += self.kerning[char]
							draw.text((x_pos, y_pos), char, fill=(*self.color.get_rgb_0_255(), int(self.color.get_alpha_level())), font=font)
						elif type(self.kerning) == dict and char in self.kerning and type(self.kerning[char]) == dict:
							x_pos += self.__settings_handler(char, "xpos")
							#print(char, self.kerning[char], self.__settings_handler(char, "font"))

							if self.aliasing != self.__settings_handler(char, "aliasing"):
								previous = draw.fontmode
								draw.fontmode = self.__settings_handler(char, "aliasing")
								char_width = draw.textbbox((0, 0), text=char, font=ImageFont.truetype(self.__settings_handler(char, "font")))[2]
								draw.text((x_pos, y_pos + self.__settings_handler(char, "ypos")), char, fill=(*self.__settings_handler(char, "color").get_rgb_0_255(), int(self.__settings_handler(char, "color").get_alpha_level())), font=ImageFont.truetype(self.__settings_handler(char, "font"), size=self.__settings_handler(char, "size")))
								draw.fontmode = previous
							else:
								draw.text((x_pos, y_pos + self.__settings_handler(char, "ypos")), char, fill=(*self.__settings_handler(char, "color").get_rgb_0_255(), int(self.__settings_handler(char, "color").get_alpha_level())), font=ImageFont.truetype(self.__settings_handler(char, "font"), size=self.__settings_handler(char, "size")))

						else:
							draw.text((x_pos, y_pos), char, fill=(*self.color.get_rgb_0_255(), int(self.color.get_alpha_level())), font=font)

					if type(self.kerning) == list:
						x_pos += char_width + self.kerning[i % len(self.kerning)]
					elif type(self.kerning) == int:
						x_pos += char_width + self.kerning
					else:
						x_pos += char_width
			else:
				if self.line_gap == None:
					draw.multiline_text((0, 0), self.text, font=font, fill=(*self.color.get_rgb_0_255(), int(self.color.get_alpha_level())), align=self.centering)
				else:
					draw.multiline_text((0, 0), self.text, font=font, fill=(*self.color.get_rgb_0_255(), int(self.color.get_alpha_level())), align=self.centering, spacing=self.line_gap)

		def __cache_regen(self):
			self.__base_regen()
			self.cache = self.base
			super()._Mtx_Image_Layer__effects_regen()

			if self.parent_group != None:
				self.parent_group._Mtx_Image_Group__cache_regen()

			self.parent_image._Mtx_Image__preview_regen()

		def replace_text(self, text):
			self.text = text
			self.__cache_regen()

		def change_color(self, color):
			self.color = color
			self.__cache_regen()



	class Mtx_Image_Group(Mtx_Image_Layer):
		def __init__(self, parent, layers=None):
			self.visible = True

			if type(layers) == Mtx_Image.Mtx_Image_Layer or type(layers) == Mtx_Image.Mtx_Image_Text_Layer:
				self.layers = [layers]
			elif type(layers) == list:
				for item in layers:
					if type(item) != Mtx_Image.Mtx_Image_Layer and type(item) != Mtx_Image.Mtx_Image_Text_Layer:
						raise TypeError(f"An entry in the Image_Group layers argument is of wrong format")
					else:
						item.parent_group = self

				self.layers = layers
			elif layers == None:
				self.layers = []
			else:
				raise ValueError("Image_Group layers argument is of wrong format")

			self.effects = []
			self.parent_image = parent
			self.parent_group = None
			self.__cache_regen()

		def __getitem__(self, number):
			return self.layers[number]

		def __cache_regen(self):
			highest_lowest = [[10**10, 0], [10**10, 0], [0, 0], [0, 0]] #left, top, right, bottom | x, y, x, y
			for item in self.layers:
				if item.xpos < highest_lowest[0][0]:
					highest_lowest[0][0] = item.xpos
					highest_lowest[0][1] = item
				if item.ypos < highest_lowest[1][0]:
					highest_lowest[1][0] = item.ypos
					highest_lowest[1][1] = item
				if item.xpos + item.cache.width > highest_lowest[2][0]:
					highest_lowest[2][0] = item.xpos + item.cache.width
					highest_lowest[2][1] = item
				if item.ypos + item.cache.height > highest_lowest[3][0]:
					highest_lowest[3][0] = item.ypos + item.cache.height
					highest_lowest[3][1] = item

			self.xpos = highest_lowest[0][0]
			self.ypos = highest_lowest[1][0]

			preview = Image.new("RGBA", (highest_lowest[2][0] - highest_lowest[0][0], highest_lowest[3][0] - highest_lowest[1][0]))
			for item in self.layers:
				current_layer = Image.new("RGBA", (highest_lowest[2][0] - highest_lowest[0][0], highest_lowest[3][0] - highest_lowest[1][0]))
				current_layer.paste(item.cache, (item.xpos - highest_lowest[0][0], item.ypos - highest_lowest[1][0]))
				preview = Image.alpha_composite(preview, current_layer)

			self.cache = preview
			self.base = preview
			super()._Mtx_Image_Layer__effects_regen()

			if self.parent_group != None:
				self.parent_group._Mtx_Image_Group__cache_regen()

			self.parent_image._Mtx_Image__preview_regen()



	def __init__(self, size, color):
		self.width = size[0]
		self.height = size[1]
		self.layers = []
		self.layers.append(self.Mtx_Image_Layer(size, (0, 0), self, color))
		self.preview = Image.new("RGBA", size, (*color.get_rgb_0_255(), int(color.get_alpha_level())))

	def __preview_regen(self):
		preview = Image.new("RGBA", (self.width, self.height))
		for item in self.layers:
			if item.visible == True:
				current_layer = Image.new("RGBA", (self.width, self.height))
				current_layer.paste(item.cache, (item.xpos, item.ypos))
				preview = Image.alpha_composite(preview, current_layer)

		self.preview = preview

	def export(self, file_name):
		self.preview.save(file_name)

	def add_checkerboard_layer(self, size, pos, square_size, color1, color2):
		new_layer = self.Mtx_Image_Layer(size, pos, self)
		new_layer.checkerboard(square_size, color1, color2)
		self.layers.append(new_layer)
		self.__preview_regen()
		return new_layer

	def add_text_layer(self, pos, text, font, color, size, kerning = 0, line_gap = 0, centering = "left", aliasing = False, extra_right_space = 0, extra_move_right = 0, rendering = "normal"):
		new_layer = self.Mtx_Image_Text_Layer(pos, text, font, color, size, self, kerning, line_gap, centering, aliasing, extra_right_space, extra_move_right, rendering)
		self.layers.append(new_layer)
		self.__preview_regen()
		return new_layer

	def add_new_layer_from_image(self, pos, image):
		new_layer = self.Mtx_Image_Layer((0, 0), pos, self, image)
		self.layers.append(new_layer)
		self.__preview_regen()
		return new_layer

	def add_new_layer_group(self, layers_to_move = None):
		new_layer = self.Mtx_Image_Group(self, layers_to_move)

		pointer = 0
		layers_temp = self.layers[:]
		for i, item in enumerate(layers_temp):
			if item in layers_to_move:
				del self.layers[i + pointer]
				pointer -= 1

		self.layers.append(new_layer)
		self.__preview_regen()
		return new_layer

"" "" "" "" ""
"" "" "" ""
"" "" ""
"" ""
""

if __name__ == "__main__":
	color = Mtx_Image((640, 480), Mtx_Color("sRGB hex", "335577"))
	color.add_checkerboard_layer((480, 250), (386, 286), (12, 10), Mtx_Color("sRGB", (0, 255, 0)), Mtx_Color("sRGB", (0, 0, 255), 35))
	color.layers[1].color_swap(Mtx_Color("sRGB", (0, 255, 0)), Mtx_Color("sRGB", (255, 0, 0)))
	color.layers[1].rotate(55)
	color._Mtx_Image__preview_regen()
	color.add_text_layer((20, 20), "0123456789", "C:/Windows/Fonts/8514oem.fon", Mtx_Color("sRGB", (255, 0, 0)), 32, line_gap=6, aliasing=True, rendering="custom", centering="right")
	#color.add_new_layer_from_image((7, 200), "random.png")
	#color.layers[1].cache.save("./preview2.png")
	color.export("./preview.png")

	#one_o_one = Mtx_Image((640, 400), Mtx_Color("sRGB hex", "0000aa"))
	#one_o_one.add_new_layer_from_image((0, 0), "./mediatrix/1985.png")
	#one_o_one.layers[1].visible = False
	#one_o_one.add_text_layer((252, 224), "Microsoft Windows\nVersion 1.011", "./mediatrix/PxPlus_IBM_CGA-2y.ttf", Mtx_Color("sRGB", (255, 0, 0)), 16, 2, "center")
	#one_o_one.export("./mediatrix/preview3.png")

	"""from matplotlib import font_manager
	from PIL import Image, ImageDraw, ImageFont

	font = font_manager.FontProperties(family='Times New Roman', weight='normal')
	file = font_manager.findfont(font)

	# Load a font
	font = ImageFont.truetype(file, size=16)

	# Create an image
	image = Image.new("RGBA", (200, 100), color="#00000000")
	draw = ImageDraw.Draw(image)
	draw.fontmode = "L"
	draw.rectangle(font.getbbox("Hello, World!"), fill="#FFFFFF")
	#draw.text((0, 2), "Hello, World!", font=font, fill="black")
	draw.fontmode = "1"

	# Draw text
	draw.text((0, 2), "Hello, World!", font=font, fill="black")

	image.show()"""
