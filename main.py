import sys
import json
import requests
from PIL import ImageGrab
from PIL import Image
import base64
import random
import string
import os
import pyperclip

# 무작위 문자열 생성
def generate_random_name(length=20):
    characters = string.ascii_letters + string.digits
    random_name = ''.join(random.choice(characters) for _ in range(length))
    return random_name


# ============================================
# JSON DATA Import Steps

# JSON 파일 경로
file_path = "personal_data.json"

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"{file_path} File not found.")
        return "None"

def create_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"{file_path} Created file. Please fill the file with information and run it again.")

# JSON 파일 읽어오기 시도
loaded_data = read_json_file(file_path)

if loaded_data == "None":
    new_data = {"github_user_name": "value1", "github_token": "value2", "gaac_repo_name": "value3"}
    create_json_file(file_path, new_data)
    os.system('pause')
    

github_headers = {
    "Authorization": f"token {loaded_data['github_token']}",
    "Accept": "application/vnd.github.v3+json"  # GitHub API 버전 지정
}

print("============================================")
print(f"Hello!! {loaded_data['github_user_name']}")
print("============================================\n")




# ============================================
# Select Folder Steps
response = requests.get(f"https://api.github.com/repos/{loaded_data['github_user_name']}/{loaded_data['gaac_repo_name']}/contents/uploads", headers=github_headers)

if response.status_code == 200:
    contents = response.json()
    print(f"***** List of your folders in repo *****\n")
    for index, item in enumerate(contents):
        if item["type"] == "dir":
            print(f"[{index}] : {item['name']}")
    print(f"\n****************************************\n")
else:
    print(f"API request failed: {response.status_code}")
    print("Check the token again!!")
    os.system('pause')

while True:
    try:
        selectedFolder_num = int(input("Select a folder ..NUMBER.. to upload: "))
        break
    except ValueError:
        print("Enter ..NUMBER.. PLZ")



# ============================================
# MAIN
while True:
    print("\n")
    print("============================================\n")
    print(f"Current location : {loaded_data['gaac_repo_name']} / {contents[selectedFolder_num]['name']}")
    print("\n")
    print("1. Copy the image to the clipboard. <Crtl + C>")
    print("2. ENTER!! in the console window")
    print("   <exit> : exit APP\n")

    isEnter = input("R U Ready? : ")
    if isEnter == "exit": sys.exit(0)

    clipboard_data = ImageGrab.grabclipboard()
    print(clipboard_data)
    print("\n")

    if clipboard_data and isinstance(clipboard_data, Image.Image):
        imageName = generate_random_name()

        # 스크린샷 폴더에 사진 저장 후 불러오기  (스크린샷 폴더: C:\Users\{user_name}\Pictures\Screenshots)
        save_name = f"{imageName}.png"
        Screenshot_folder = os.path.join("C:\\Users", os.getlogin(), "Pictures/Screenshots")
        img_path = os.path.join(Screenshot_folder, save_name)
        clipboard_data.save(img_path)
        
        with open(img_path, "rb") as file:
            image = file.read()
            image_base64 = base64.b64encode(image).decode("utf-8")

        # GitHub API
        api_url = f"https://api.github.com/repos/{loaded_data['github_user_name']}/{loaded_data['gaac_repo_name']}/contents/uploads/{contents[selectedFolder_num]['name']}/{imageName}.png"
        data = {"message": "new img", "content": image_base64}
        
        # 이미지를 GitHub 리포지토리에 업로드
        response = requests.put(api_url, headers=github_headers, json=data)
        
        if response.status_code == 201:
            pyperclip.copy(f"https://raw.githubusercontent.com/radic2682/blog_images_repo/main/uploads/{contents[selectedFolder_num]['name']}/{imageName}.png")
            
            print("*****************************************")
            print("The image has been successfully uploaded.")
            pyperclip.copy(f"[이미지](https://raw.githubusercontent.com/radic2682/blog_images_repo/main/uploads/{contents[selectedFolder_num]['name']}/{imageName}.png)")
            print("(Copy to clipboard.)\n")
            print("*****************************************")
        else:
            print(f"API request failed: {response.status_code}")




    elif clipboard_data and isinstance(clipboard_data, list):

        for data in clipboard_data:
            with open(data, "rb") as file:
                image = file.read()
                image_base64 = base64.b64encode(image).decode("utf-8")

            imageName = generate_random_name()
            extension = data[data.rfind(".") + 1:]

            # GitHub API
            api_url = f"https://api.github.com/repos/{loaded_data['github_user_name']}/{loaded_data['gaac_repo_name']}/contents/uploads/{contents[selectedFolder_num]['name']}/{imageName}.{extension}"
            data = {"message": "new img", "content": image_base64}
            
            # 이미지를 GitHub 리포지토리에 업로드
            response = requests.put(api_url, headers=github_headers, json=data)
            
            if response.status_code == 201:
                pyperclip.copy(f"[이미지](https://raw.githubusercontent.com/radic2682/blog_images_repo/main/uploads/{contents[selectedFolder_num]['name']}/{imageName}.{extension})") 
                print("*****************************************")
                print("The image has been successfully uploaded.")
                print(f"https://raw.githubusercontent.com/radic2682/blog_images_repo/main/uploads/{contents[selectedFolder_num]['name']}/{imageName}.{extension}")
                print("(Copy to clipboard.)\n")
                print("*****************************************")
            else:
                print(f"API request failed: {response.status_code}")


    else:
        print("클립보드에 이미지가 없습니다.")

