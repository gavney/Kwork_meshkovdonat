# -*- coding: utf-8 -*-
import vk_api
import json
import time
import random


def captcha_handler(captcha):

    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    return captcha.try_again(key)


def upload_config():

    with open("config.json", "r", encoding='utf-8') as jsonfile:
        return json.load(jsonfile) 
        

def init_account(login, password):
    
    vk_session = vk_api.VkApi(
        login, password, app_id=2685278,
        captcha_handler=captcha_handler
    )

    vk_session.auth()
    
    print("Авторизация прошла успешно")
    return vk_session.get_api()


def get_last_post(vk, group_id):
    
    last_post_id = vk.wall.get(
        owner_id = -group_id,
        count = 1
    ).get("items")[0]
    
    return last_post_id.get("id")


def main():

    data = upload_config()
    settings = data.get("settings")

    text = settings.get("text")
    delay = settings.get("delay")
    delay_comment = settings.get("delay_comment")

    login = settings.get("login")
    password = settings.get("password")

    group_id = settings.get('group_id')

    vk = init_account(
        login=login,
        password=password
    )

    last_post_id = get_last_post(vk, group_id)

    while True:
        
        time.sleep(delay)
        new_post = get_last_post(vk, group_id)
        
        if new_post != last_post_id:
            
            last_post_id = new_post
            print("Новый пост в группе ", group_id)

            vk.wall.addLike(
                owner_id = -group_id,
                post_id = last_post_id
            )

            time.sleep(delay_comment)

            vk.wall.createComment(
                owner_id = -group_id,
                post_id = last_post_id,
                message = random.choice(text)
            )
            
        
if __name__ == "__main__":
    main()