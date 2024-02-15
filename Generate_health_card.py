from PIL import ImageFont, ImageDraw, Image  

image = Image.open("HEALTH_CARD.png")  

draw = ImageDraw.Draw(image)  

font = ImageFont.truetype("arial.ttf", 15)  

draw.text((10, 250), "Name: Ajay Ladkat", font=font, fill='#000000')  
draw.text((10, 280), "Adress: 911, Bhawani Peth", font=font, fill='#000000')  
draw.text((10, 310), "Date of Birth: 30/01/1993", font=font, fill='#000000')  
draw.text((10, 340), "Mobile: 9028768103", font=font, fill='#000000')  
draw.text((10, 370), "Email: ajayladkat123@gmail.com", font=font, fill='#000000')  
draw.text((10, 400), "Health Insurance Number : 80518051", font=font, fill='#000000')  
draw.text((10, 430), "Adhar Card number : 123456789012", font=font, fill='#000000')  
draw.text((10, 480), "", font=font, fill='#000000')  

image = image.convert('RGB')
image.save('report.pdf')
