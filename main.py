from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import system
from time import sleep
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re


link = "https://kissanime.ru"
EPISODE_BEGIN = '<table class="listing">\n                            <tbody><tr>\n                                <th width="85%">\n                                    Episode name\n                                </th>\n                                <th width="15%">\n                                    Day Added\n                                </th>\n                            </tr>\n                            <tr style="height: 10px">\n                            </tr>\n                            \n'
EPISODE_BEGIN = re.escape(EPISODE_BEGIN).split('\\\n')
EPISODE_BEGIN = '\s*\\\n\s*'.join(EPISODE_BEGIN)
EPISODE_END = '</tbody></table>\n                        \n                    </div>\n                </div>\n            </div>\n'
EPISODE_END = re.escape(EPISODE_END).split('\\\n')
EPISODE_END = '\s*\\\n\s*'.join(EPISODE_END)

def closeAd(BROWSER):
	if len(BROWSER.window_handles) > 1:
		BROWSER.switch_to.window(BROWSER.window_handles[1])
		BROWSER.close()
	BROWSER.switch_to.window(BROWSER.window_handles[0])
	if BROWSER.current_url.find('kissanime') == -1:
		BROWSER.execute_script("window.history.go(-1)")
	return	

def submit_idpass(BROWSER):
	with open('idpass.txt', 'r') as f:
		kissmanga_credentials = f.read().splitlines()
		username_area = BROWSER.find_element_by_id('username')
		username_area.send_keys(Keys.CONTROL, "a")
		username_area.send_keys(kissmanga_credentials[0])
		password_area = BROWSER.find_element_by_id('password')
		password_area.send_keys(Keys.CONTROL, "a")
		password_area.send_keys(kissmanga_credentials[1])
		submit_button = BROWSER.find_element_by_id('btnSubmit')
		submit_button.click()
		closeAd(BROWSER)
		if password_area == '' or username_area == '':
			submit_idpass()
	return

def afterCaptcha(BROWSER):
	for i in range(30):
		if 'AreYouHuman2' in BROWSER.current_url:
			sleep(2)
		elif i == 30:
			exit()
		elif 'kissanime' in BROWSER.current_url:
			sleep(4)
			break
		else:
			continue

	closeAd(BROWSER)

	close_ad = BROWSER.find_element_by_class_name('glx-close.glx-close-with-text')
	close_ad.click()
	sleep(1)
	play_button = BROWSER.find_element_by_class_name('vjs-big-play-button')
	play_button.click()

	closeAd(BROWSER)
	sleep(1)
	fullscreen_button = BROWSER.find_element_by_class_name('vjs-fullscreen-control.vjs-control')
	fullscreen_button.click()
	if len(BROWSER.window_handles) > 1:
		BROWSER.switch_to.window(BROWSER.window_handles[1])
		BROWSER.close()
		BROWSER.switch_to.window(BROWSER.window_handles[0])
		fullscreen_button.click()

	while True:
		sleep(5)
		raw_data = BROWSER.page_source
		soup = BeautifulSoup(raw_data,'html.parser')
		progress = soup.find('div',{'role':"slider"})['aria-valuenow']
		if(progress == '100'):
			break
	try:
		next_button = BROWSER.find_element_by_id('btnNext')
	except NoSuchElementException:
		keyboard.press(Key.escape)
		keyboard.release(Key.escape)
		return
	next_button.click()	
	afterCaptcha(BROWSER)

def showMenu():
	print("1. Start watching")
	print("2. Show list")
	print("3. Add list")
	print("4. Delete list")
	print("5. exit")
	return

def startWatching():
	showList()
	with open("Anime List.txt","r+") as f:
		lists = f.read().splitlines()
		while True:
			try:
				index = int(input("enter the number of the anime you want to watch:('0' to cancel)"))
			except ValueError:
				system('cls')
				showList()
				print("please input the correct value")
				continue
			if index == 0:
				system('cls')
				main()

			elif index > len(lists):
				system('cls')
				showList()
				print("please input the correct value")
				continue	
			else:
				system('cls')
				break
	print('processing....')
	sleep(2)						
	name_of_anime = lists[index-1]
	#start opening chrome
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--start-maximized")
	vid = link + '/Anime/' + name_of_anime.replace(' ','-')
	driver = webdriver.Chrome(options=chrome_options)
	driver.get(link+'/login')
	sleep(6)

	submit_idpass(driver)
	driver.get(vid)
	system('cls')
	#opening the last viewed episode
	raw_data = driver.page_source
	anime_list_raw = re.search(EPISODE_BEGIN+'([\s\S]*?)'+EPISODE_END, raw_data).group(1)
	episode_iter = re.finditer('<a '+'([\s\S]*?)'+'</a>', anime_list_raw)
	for matched_sentence in episode_iter:
		matched_sentence = matched_sentence.group(1)
		link_append = re.search('href="'+'([\s\S]*?)'+'" title=',matched_sentence).group(1)
		if 'class="episodeVisited"' in matched_sentence:
			break
		else:
			continue		
	driver.get(link+link_append)
	system('cls')
	afterCaptcha(driver)
	return

def showList():
	system('cls')
	with open("Anime List.txt","r") as f:
		content = f.readlines()
		for i, item in enumerate(content,1):
			print(i,'.',item)
	return

def showList2():
	showList();
	system('pause')
	system('cls')
	return

def deleteList():
	showList()
	with open("Anime List.txt","r+") as f:
		if f is None:
			system('cls')
			print("the list is empty! returning to main page...")
			sleep(2)
			system('cls')
			return

		lists = f.read().splitlines()
		while True:
			try:
				index = int(input("enter the number of the anime you want to delete: ('0' to cancel)"))
			except ValueError:
				system('cls')
				showList()
				print("please input the correct value")
				continue
			if index == 0:
				system('cls')
				main()	
			elif index > len(lists):
				system('cls')
				showList()
				print("please input the correct value")
				continue	
			else:
				system('cls')
				confirmation = input("are you sure? y/n ")
				if confirmation == 'y' or  confirmation == 'Y':
					lists.pop(index-1)
					break
				elif confirmation == 'n' or confirmation == 'N':
					system('cls')
					deleteList()
				else:	
					system('cls')
					print("input error! back to delete page")
					sleep(2)
					deleteList()
	with open("Anime List.txt","w+") as f:
		for i in lists:
			f.write(i+'\n')
	system('cls')
	print("deleted successfully!")
	sleep(1.5)
	system('cls')
	return


def addList():
	name = input("please insert the name correctly: (type 'c' to cancel) ")
	if(name == 'c'):
		system('cls')
		print("canceled!")
		sleep(1)
		system('cls')
		return
	with open("Anime List.txt", "r") as f:
		lists = f.read().splitlines()
		for i in lists:
			if i == name:
				print("the anime has been listed already!")
				sleep(1.5)
				system('cls')
				return	
	with open("Anime List.txt", "a+") as f:
		f.write(name+"\n")
	system('cls')	
	print("Added successfully")
	sleep(1)
	system('cls')
	return


def processAnswer1(argument):
	switcher = {
		1: startWatching,
		2: showList2,
		3: addList,
		4: deleteList,
		5: exit,
	}
	temp = switcher.get(argument)
	return temp()


def main():
	while True:
		showMenu()
		while True:
			try:
				input1 = int(input("what do you want to do? "))
			except ValueError:
				system('cls')
				showMenu()
				print("please re enter value")
				continue
			if input1 >=6 or input1 <= 0:
				system('cls')
				showMenu()
				print("please re enter value")
				continue
			else:
				break;
		system('cls')			
		processAnswer1(input1)


if __name__ == "__main__":
	main()
