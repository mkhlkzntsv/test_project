import uiautomator2 as u2
import hcaptcha
import helpers
import time
import random
import requests
import dict as dicton
import configparser, argparse

TIMEOUT = 20



class Nox:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.device = u2.connect(address)


    def cleaner(self):
        self.device.app_clear('com.discord')
        self.device.app_clear('com.android.browser')


    def swiper(self, query1, query2):
        pos1 = self.device.xpath(query1).rect
        pos2 = self.device.xpath(query2).rect
        for i in range(random.randint(6,9)):
            self.device.swipe(pos1[0]+5, pos1[1]+5, pos2[0]+5, pos2[1]+pos2[3]-5, 0.1)
            time.sleep(1)


    def hcapcha(self):
        old_task = ''
        ind = 0
        self.device.xpath('//*[@text="hCaptcha"]//android.widget.TextView[1]').wait(timeout=60)
        while True:
            print('hcaptcha')
            time.sleep(3)
            if not 'hcaptcha' in self.device.dump_hierarchy():
                print('cap exit')
                break

            task = self.device.xpath('//*[@text="hCaptcha"]//android.widget.TextView[1]').get_text()
            for iter, img in enumerate(self.device.xpath('//android.widget.ToggleButton').all()):
                image = img.screenshot()
                image.save(f"./model/1-{iter}.jpg")
            resp = hcaptcha.getMethod('elephant', 1,
                                      task) if 'истья' in task or 'leaves' in task else hcaptcha.getMethod('other', 1,
                                                                                                           task)
            print(resp)
            for point in resp.split(','):
                self.device.xpath(f'//android.widget.ToggleButton[{int(point) + 1}]').click()
            self.device.xpath('//android.widget.Button').all()[-1].click()
            time.sleep(2)

    def setProxy(self, ip, port, login_proxy, password_proxy):
        self.device.app_stop("org.proxydroid")
        self.device.app_start("org.proxydroid", use_monkey=True)
        self.device.xpath('//*[@resource-id="android:id/switch_widget"]').wait()
        c = self.device.xpath(
            '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]/android.widget.TextView[2]').get_text()
        if c != ip:
            if login_proxy != None:
                self.device.swipe(50, 500, 50, 100, 0, 15)
                time.sleep(2)
                self.device.xpath(
                    '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[7]/android.widget.LinearLayout[1]/android.widget.CheckBox[1]').click()
                time.sleep(1)
                self.device.xpath(
                    '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[8]/android.widget.RelativeLayout[1]').click()
                self.device.xpath('//*[@resource-id="android:id/edit"]').set_text(login_proxy)
                self.device.xpath('//*[@resource-id="android:id/button1"]').click()
                self.device.xpath(
                    '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[9]/android.widget.RelativeLayout[1]').click()
                self.device.xpath('//*[@resource-id="android:id/edit"]').set_text(password_proxy)
                self.device.xpath('//*[@resource-id="android:id/button1"]').click()
                self.device.swipe(50, 100, 50, 500, 0, 15)
                time.sleep(2)
            self.device.xpath(
                '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]').click()
            self.device.xpath('//*[@resource-id="android:id/edit"]').set_text(ip)
            self.device.xpath('//*[@resource-id="android:id/button1"]').click()
            self.device.xpath(
                '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[5]/android.widget.RelativeLayout[1]').click()
            self.device.xpath('//*[@resource-id="android:id/edit"]').set_text(port)
            self.device.xpath('//*[@resource-id="android:id/button1"]').click()
        self.device.xpath('//*[@resource-id="android:id/switch_widget"]').click()
        time.sleep(5)


def main(path):
    config = configparser.ConfigParser()
    config.read(path)
    token = config['DEFAULT']['email_token']
    sms_token = config['DEFAULT']['phone_token']
    COUNTRY = config['DEFAULT']['country']
    thr = config['DEFAULT']['thread']
    proxy = config['proxy']['proxy'].split(':')
    user_generate = config['path'].getboolean('generate')
    thread = config['DEFAULT']['thread']

    a = Nox(config['NOX']['name'], config['NOX']['address'])

    username, password = config['path']['nicknames'] if user_generate else helpers.get_username(), \
                         helpers.get_password()
    email, email_id = helpers.get_email(token)
    a.cleaner()
    if len(proxy) == 2:
        a.setProxy(proxy[0], proxy[1])
    else:
        a.setProxy(proxy[0],proxy[1],proxy[2],proxy[3])
    a.device.app_start('com.discord')

    a.device.xpath('//*[@resource-id="com.discord:id/auth_landing_register"]').click()
    a.device.xpath('//*[@resource-id="com.discord:id/auth_register_identity_second_segment_card"]').click()
    a.device.xpath('//*[@resource-id="com.discord:id/phone_or_email_main_input"]').set_text(email)
    a.device.xpath('//*[@resource-id="com.discord:id/auth_register_identity_button"]').click()

    a.device.xpath('//*[@resource-id="com.discord:id/textinput_placeholder"]').set_text(username)
    a.device.xpath('//*[@resource-id="com.discord:id/auth_register_account_information_password_wrap"]').set_text(password)

    a.device.xpath('//*[@resource-id="com.discord:id/loading_button_button"]').click()
    a.device.xpath('//*[@resource-id="com.discord:id/auth_register_birthday"]').click()
    a.swiper('//*[@text="2011"]','//*[@text="2013"]')
    time.sleep(1)
    a.device.xpath('//*[@resource-id="com.discord:id/dialog_date_picker_done"]').click()
    a.device.xpath('//*[@resource-id="com.discord:id/auth_register_button"]').click()
    a.device.xpath('//*[@resource-id="com.discord:id/captcha_verify"]').click()
    a.hcapcha()
    attemp = 0
    while True:
        try:
            if a.device.xpath('//*[@resource-id="com.discord:id/menu_contact_sync_skip"]').exists:
                a.device.xpath('//*[@resource-id="com.discord:id/menu_contact_sync_skip"]').click()

            if a.device.xpath('//*[@resource-id="com.discord:id/nux_guild_template_action_join"]').exists:
                a.device\
                    .xpath(f'//*[@resource-id="com.discord:id/recycler_view"]/androidx.cardview.widget.CardView[{random.randint(1,7)}]')\
                    .click()

            if a.device.xpath('//*[@resource-id="com.discord:id/creation_intent_second_option"]').exists:
                a.device.xpath('//*[@resource-id="com.discord:id/creation_intent_second_option"]').click()

            if a.device.xpath('//*[@resource-id="com.discord:id/guild_create_button"]').exists:
                a.device.xpath('//*[@resource-id="com.discord:id/guild_create_button"]').click()

            if a.device.xpath('//*[@resource-id="com.discord:id/guild_invite_empty_suggestions_invite_share_btn"]')\
                    .exists:
                print('ok')
                a.device.xpath('//*[@resource-id="com.discord:id/action_bar_toolbar"]/android.widget.ImageButton')\
                    .click()

            if a.device.xpath('//*[@resource-id="com.discord:id/discord_hub_email_no"]').exists:
                a.device.xpath('//*[@resource-id="com.discord:id/discord_hub_email_no"]').click()

            if a.device.xpath('//*[@resource-id="com.discord:id/nuf_channel_prompt_cta_button"]').exists:
                a.device.xpath('//*[@resource-id="com.discord:id/nuf_channel_prompt_topic_wrap"]').set_text('Hello!')
                a.device.xpath('//*[@resource-id="com.discord:id/nuf_channel_prompt_cta_button"]').click()

            if a.device.xpath('//*[@resource-id="com.discord:id/widget_chat_list"]').exists:
                if attemp == 0:
                    attemp += 1
                    time.sleep(2)
                    continue
                if attemp == 1:
                    break
        except:
            print('Ошибка')
    a.device.xpath('//*[@resource-id="com.discord:id/action_bar_toolbar"]/android.widget.ImageButton').click()
    a.device.xpath('//*[@resource-id="com.discord:id/channel_actions_view"]').click()
    a.device.xpath('//*[@resource-id="com.discord:id/tabs_host_bottom_nav_user_settings_item"]').click()
    a.device.xpath('//*[@resource-id="com.discord:id/account"]').click()
    time.sleep(3)
    while True:
        if a.device.xpath('//*[@resource-id="com.discord:id/settings_account_verification"]').exists:
            a.device.xpath('//*[@resource-id="com.discord:id/settings_account_verification_button"]').click()
        if a.device.xpath('//*[@resource-id="com.discord:id/alert_verify_email_anchor"]/android.widget.FrameLayout[2]')\
                .exists:
            try:
                url = helpers.get_code(email_id, '8648a47839902a44adac6d0a16808f78')
                a.device.app_start('com.android.browser')
                a.device.xpath('//*[@resource-id="com.android.browser:id/url"]').set_text(url)
                a.device.press("enter")
                time.sleep(10)
                a.device.app_start('com.discord')
                time.sleep(5)
            except:
                a.device.app_start('com.discord')
                email, email_id = helpers.get_email(token)
                a.device.xpath(
                    '//*[@resource-id="com.discord:id/alert_verify_email_anchor"]/android.widget.FrameLayout[2]').click()
                a.device.xpath('//*[@resource-id="com.discord:id/alert_verify_email_change_email"]').set_text(email)
                a.device.xpath('//*[@resource-id="com.discord:id/alert_verify_email_change_password"]').set_text(
                    password)
                a.device.xpath('//*[@resource-id="com.discord:id/alert_verify_email_change"]').click()
        if a.device.xpath('//*[@resource-id="com.discord:id/settings_account_phone_text"]').exists:
            if a.device.xpath('//*[@resource-id="com.discord:id/settings_account_phone_text"]').get_text() == '':
                a.device.xpath('//*[@resource-id="com.discord:id/settings_account_phone_text"]').click()

                a.device.xpath('//*[@resource-id="com.discord:id/phone_or_email_country_code_wrap"]').click()
                number, number_id = helpers.get_number(sms_token, dicton.number_ids[COUNTRY])

                a.device.xpath(
                    '//*[@resource-id="com.discord:id/phone_country_code_search"]/android.widget.FrameLayout[1]')\
                    .set_text(COUNTRY)
                time.sleep(1)
                a.device.xpath('//*[@resource-id="com.discord:id/phone_country_code_recycler"][1]').click()
                a.device.xpath('android.widget.EditText[1]').wait()
                code = len(a.device.xpath('//android.widget.EditText[1]').get_text().split(',')[0].replace('+', ''))
                a.device.xpath('//*[@resource-id="com.discord:id/phone_or_email_main_input_wrap"]')\
                    .set_text(number[code:])
                a.device.xpath('//*[@resource-id="com.discord:id/user_phone_add_next"]').click()
                a.device.xpath('//*[@resource-id="com.discord:id/captcha_verify"]').click()
                a.hcapcha()
                try:
                    sms = helpers.get_sms(sms_token, number_id)
                except:
                    a.device.xpath('//*[@resource-id="com.discord:id/close_button"]').click()
                    a.device.press('back')
                    time.sleep(3)
                    helpers.set_status_number(token, number_id, 8)
                    continue
                a.device.xpath('//*[@resource-id="com.discord:id/layout"]/android.widget.TextView[1]').click()
                for iter, i in enumerate(list(sms)):
                    a.device.send_keys(i)
                a.device.xpath('//*[@resource-id="com.discord:id/edit_account_password_wrap"]').set_text(password)
                a.device.xpath('//*[@resource-id="com.discord:id/settings_account_save"]').click()
                time.sleep(10)
                print(f"OUTPUT:{email}|{password}")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Path for reger")
    parser.add_argument("path")
    args = parser.parse_args()
    main(args.path)
