# extensions\utils.py
import json
import os
from datetime import datetime, time as dt_time
# import httpx
# from openai import OpenAI
import requests
from extensions import jalali
from django.utils import timezone
from django.core.mail import send_mail as send
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from google import genai
from typing import Optional
import re


def extract_json_block(text):
    # اگر داخل بلاک کد Markdown باشه (```...```)
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)

    # اگر فقط یه JSON خالص باشه
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        return match.group(1)

    return None


def fix_nested_response_format(cleaned):
    try:
        parsed = json.loads(cleaned)
        if "responses" in parsed:
            fixed = []
            for item in parsed["responses"]:
                if isinstance(item, str):
                    fixed.append(item)
                elif isinstance(item, list):
                    # تبدیل به رشته اگر داخل لیست باشه
                    fixed.append(" ".join(str(sub)
                                 for sub in item if isinstance(sub, str)))
                elif isinstance(item, dict):
                    # اگر به اشتباه dict باشه هم نادیده گرفته بشه یا stringify بشه
                    fixed.append(str(item))
            parsed["responses"] = fixed
        return parsed
    except Exception as e:
        print("Fix failed:", e)
        return {"error": "Response format error."}



def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def send_pattern_sms(phoneNumber, code, pattern=None):
    username = 'XXXXXXXX'
    password = "XXXXXXXXXXXXXX"
    if pattern:
        message_code = pattern
    else:
        message_code = "XXXXXX"
    # message_code = 323070 #temp

    print(f"Verification code for {phoneNumber}: {code}")

    try:
        response = requests.post(
            'https://rest.payamak-panel.com/api/SendSMS/BaseServiceNumber',
            headers={
                'Content-Type': 'application/json',
            },
            json={
                'username': username,
                'password': password,
                'text': code,
                'to': phoneNumber,
                # 'to': "09107647361",
                'bodyId': message_code
            }
        )

        data = response.json()

        if response.ok:
            # Check if the sending was successful based on returned values
            if data.get('RetStatus') == 1 or data.get('StrRetStatus') == "OK":
                return {"success": True, "message": "پیامی به شماره همراه شما ارسال گردید لطفا کد ارسال شده را در کادر وارد نمایید"}
            else:
                # Handle different errors based on returned code or message
                error_message = 'خطا در ارسال پیامک'
                value = data.get('Value')

                if value == '6':
                    error_message = 'خطای داخلی با پشتیبانی پنل تماس بگیرید'
                elif value == '5':
                    error_message = 'متن ارسالی توسط کاربر دستکاری شده است.'
                elif value == '4':
                    error_message = 'کد متن ارسالی صحیح نمی باشد'
                elif value == '3':
                    error_message = 'خط مشخص شده در سیستم موجود نمی باشد'
                elif value == '2':
                    error_message = 'اعتبار پنل پیامکی کافی نیست'
                elif value == '0':
                    error_message = 'نام کاربری یا رمز عبور صحیح نیست'
                elif value == '1':
                    error_message = 'این سرویس برای شما غیر فعال می باشد'
                elif value == '7':
                    error_message = 'متن حاوی کلمات فیلتر شده می باشد'
                elif value == '10':
                    error_message = 'حساب کاربری پنل پیامکی شما فعال نمی باشد'
                elif value == '11':
                    error_message = 'ارسال نشد'
                elif value == '12':
                    error_message = 'مدارک احراز پنل پیامکی شما کامل نمی باشد'

                return {"success": False, "message": error_message}
        else:
            return {"success": False, "message": 'خطا در فراخوانی سرویس پیامک'}

    except Exception as error:
        print(f'SMS API error: {error}')
        return {"success": False, "message": 'خطا در ارتباط با سرویس پیامک'}


class SendEmail(object):
    @classmethod
    def send_mail_admin(cls, subject, recipient_list, template, context):
        html_message = render_to_string(template, context)
        message = strip_tags(html_message)
        try:
            send(
                subject, message, "admin@toupchee.ir", recipient_list, auth_user="admin@toupchee.ir",
                auth_password="Hamid1063", html_message=html_message
            )
            return message
        except Exception:
            return ""

    @classmethod
    def send_mail_info(cls, subject, recipient_list, template, context):
        html_message = render_to_string(template, context)
        message = strip_tags(html_message)
        try:
            send(
                subject, message, "info@toupchee.ir", recipient_list, auth_user="info@toupchee.ir",
                auth_password="Hamid1063", html_message=html_message
            )
            return message
        except Exception:
            return ""

    @classmethod
    def send_mail_customer(cls, subject, recipient_list, template, context):
        html_message = render_to_string(template, context)
        message = strip_tags(html_message)
        try:
            send(
                subject, message, "customer@toupchee.ir", recipient_list, auth_user="customer@toupchee.ir",
                auth_password="Hamid1063", html_message=html_message
            )
            return message
        except Exception:
            return ""

    @classmethod
    def send_mail(cls, subject, from_email, recipient_list, auth_user, auth_password, template, context):
        html_message = render_to_string(template, context)
        message = strip_tags(html_message)
        try:
            send(
                subject, message, from_email, recipient_list, auth_user=auth_user,
                auth_password=auth_password, html_message=html_message
            )
            return message
        except Exception:
            return ""


def persian_numbers_converter(string):
    numbers = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }

    for e, p in numbers.items():
        string = string.replace(e, p)

    return string


def num_to_month(month_str):
    month_str = int(month_str)
    month_list = [
        "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
        "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
    ]
    return month_list[month_str - 1]


def jalali_converter(time):
    time = timezone.localtime(time)
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    mon = time_to_tuple[1] if time_to_tuple[1] > 9 else "0" + \
        str(time_to_tuple[1])
    day = time_to_tuple[2] if time_to_tuple[2] > 9 else "0" + \
        str(time_to_tuple[1])
    hou = time.hour if time.hour > 9 else "0" + str(time.hour)
    min = time.minute if time.minute > 9 else "0" + str(time.minute)
    sec = time.second if time.second > 9 else "0" + str(time.second)
    output = f"{time_to_tuple[0]}/{mon}/{day} "
    output += f" ساعت {hou}:{min}:{sec} "

    return persian_numbers_converter(output)


def jalali_converter_date(date_obj):
    naive_date = datetime.combine(date_obj, dt_time.min)
    aware_date = timezone.make_aware(naive_date)
    local = timezone.localtime(aware_date)
    time_to_str = f"{local.year},{local.month},{local.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    mon = str(time_to_tuple[1]).zfill(2)
    day = str(time_to_tuple[2]).zfill(2)
    output = f"{time_to_tuple[0]}/{mon}/{day}"

    return persian_numbers_converter(output)


def jalali_get_day(time):
    time = timezone.localtime(time)
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    output = f"{time_to_tuple[2]}"

    return persian_numbers_converter(output)


def jalali_get_month(time):
    time = timezone.localtime(time)
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    output = f"{num_to_month(time_to_tuple[1])}"

    return persian_numbers_converter(output)


def jalali_get_year(time):
    time = timezone.localtime(time)
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    output = f"{time_to_tuple[0]}"

    return persian_numbers_converter(output)


def date_comper(date_1, date_2):
    """Get Tow Date And if Date_1 Is Bigger Than Date_2 Return True Else Return False"""
    date_1 = timezone.localtime(date_1)
    date_2 = timezone.localtime(date_2)
    d_1 = datetime(
        year=date_1.year,
        month=date_1.month,
        day=date_1.day,
        hour=date_1.hour,
        minute=date_1.minute,
        second=date_1.second,
    )
    d_2 = datetime(
        year=date_2.year,
        month=date_2.month,
        day=date_2.day,
        hour=date_2.hour,
        minute=date_2.minute,
        second=date_2.second,
    )
    if d_1 > d_2:
        return True
    return False


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
