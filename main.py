from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import system
from time import sleep


link = "https://kissanime.ru/Anime/"

def submit_idpass(BROWSER):
	with open('idpass.txt', 'r') as f:
		kissmanga_credentials = f.read().splitlines()
		username_area = BROWSER.find_element_by_id('username')
		username_area.send_keys(kissmanga_credentials[0])
		password_area = BROWSER.find_element_by_id('password')
		password_area.send_keys(kissmanga_credentials[1])
		submit_button = BROWSER.find_element_by_id('btnSubmit')
		submit_button.click()
		BROWSER.switch_to.window(BROWSER.window_handles[1])
		BROWSER.close()
		BROWSER.switch_to.window(BROWSER.window_handles[0])
		if BROWSER.current_url.find('kissanime') == -1:
			BROWSER.execute_script("window.history.go(-1)")
	return

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
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--start-maximized")
	vid = link + name_of_anime.replace(' ','-')+'?'
	driver = webdriver.Chrome(options=chrome_options)
	driver.get('https://kissanime.ru/login')
	sleep(6)
	submit_idpass(driver)
	driver.get(vid)
	system('cls')
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
