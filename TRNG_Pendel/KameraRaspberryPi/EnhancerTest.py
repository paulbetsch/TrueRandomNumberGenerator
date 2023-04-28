from PIL import Image, ImageEnhance

for i in range(129):
	image = Image.open('PiPictures/Image' + str(i) + '.jpg')

	image = image.convert('L')

	enhancer = ImageEnhance.Contrast(image)
	image = enhancer.enhance(1.31)

	enhancer = ImageEnhance.Brightness(image)
	image = enhancer.enhance(60.5)

	#Kontrast
	enhancer = ImageEnhance.Contrast(image)
	enhanced_image = enhancer.enhance(5.5)

	image.save('EnhancedPictures/enhanced_image' + str(i) + '.jpg')
