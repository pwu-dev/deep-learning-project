import glob
import PIL
from PIL import Image
import numpy as np
import os


#Pour l'augmentation des données, il suffit de rajouter les couches suivantes dans notre modèle
""" 
    layers.RandomFlip("horizontal",input_shape=(img_height,img_width,3)),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
) """

CLASSES = ["beurre", "cremes-dessert", "eaux", "fromages", "haricots-verts", 
           "huiles-cuisson", "jus-fruits", "lait", "mais", "oeufs", 
           "pates", "petits-pois", "poissons", "riz", "sodas", 
           "soupes", "viandes-rouges", "volailles", "yaourts-laitiers"]

def load_data(data_path, classes, image_size=64):

	num_images = 0
	for i in range(len(classes)):
		dirs = sorted(os.listdir(data_path + '/' + classes[i]))
		num_images += len(dirs)
                                
	x = np.zeros((num_images, image_size, image_size, 3))
	y = np.zeros((num_images, 1))
    
	current_index = 0
    
    # Parcours des différents répertoires pour collecter les images
	for idx_class in range(len(classes)):
		dirs = sorted(os.listdir(data_path + '/' + classes[idx_class]))
		num_images += len(dirs)
    
        # Chargement des images, 
		for idx_img in range(len(dirs)):
			item = dirs[idx_img]
			if os.path.isfile(data_path + '/' + classes[idx_class] + '/' + item):
                # Ouverture de l'image
				img = Image.open(data_path + '/' + classes[idx_class] + '/' + item)
                # Conversion de l'image en RGB
				img = img.convert('RGB')

                # Change la taille de l'image de telle façon à ce qu'elle soit un carré en remplissant les pixels manquant par du blanc
				x_size, y_size = img.size
				size = max(x_size, y_size)
				new_im = Image.new('RGB', (size, size), (255, 255, 255))
				new_im.paste(img, (int((size - x_size) / 2), int((size - y_size) / 2)))

                # Redimensionnement de l'image et écriture dans la variable de retour x 
				img = new_im.resize((image_size,image_size))
				x[current_index] = np.asarray(img)
                # Écriture du label associé dans la variable de retour y
				y[current_index] = idx_class
				current_index += 1

	return x, y