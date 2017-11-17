
from optical_flow_functions import *
from basic_packages import *



def main():
	# setup video capture
	vidcap = cv2.VideoCapture('../Datasets/Easy/TheMartian.mp4')
	success = True
	# the previous img
	pre_img = None

	# the feature_x and feature_y in previous img  
	startX = None 
	startY = None
	while success:
		success,cur_img = vidcap.read()
	    #convert to gray scale
  		# first image 
  		if(pre_img is None):
  			cur_gray = cv2.cvtColor(cur_img, cv2.COLOR_BGR2GRAY)
			cur_gray = np.asarray(cur_gray)
  			bbox = detectFace(cur_gray)
			startXs, startYs = getFeatures(cur_gray,bbox)
			pre_img = cur_img

		# after second image
		else:
			# change the previous img into gray 
			pre_gray = cv2.cvtColor(pre_img, cv2.COLOR_BGR2GRAY)
			pre_gray = np.asarray(pre_gray)
			
			pre_gradient_x, pre_gradient_y = np.gradient(pre_gray)

			# change the currnet img into gray 
  			cur_gray = cv2.cvtColor(cur_img, cv2.COLOR_BGR2GRAY)
			cur_gray = np.asarray(cur_gray)

			newX, newY = estimateFeatureTranslation(startXs[0], startYs[0], pre_gradient_x, pre_gradient_y, pre_gray, cur_gray)


			# plt.figure()
			# plt.subplot(2,2,1),plt.imshow(pre_img_gx, cmap='gray')
			# plt.subplot(2,2,2),plt.imshow(pre_img_gy, cmap='gray')
			# plt.axis('off')
			# plt.show()			

			break

  		if cv2.waitKey(10) == 27:  # exit if Escape is hit
			break
	
if __name__ == "__main__":
	main()