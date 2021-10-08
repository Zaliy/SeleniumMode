import email
import imaplib
import os
import traceback
import time
import yaml

class Tools:

    @classmethod
    def read_file(cls, filename: str):
        lines = []
        if os.path.isfile(filename):
            fi = None
            try:
                fi = open(filename, encoding="UTF-8")
                text = fi.readline()
                while text is not None and text != "":
                    lines.append(text.strip())
                    text = fi.readline()
            except:
                print("Read File Error.")
            finally:
                if fi is not None:
                    fi.close()
        return lines

    @classmethod
    def read_yaml(cls, config_file: str):
        if os.path.isfile(config_file):
            fi = None
            try:
                fi = open(config_file, encoding="UTF-8")
                return yaml.full_load(fi)
            except:
                print("Read Config Error.")
            finally:
                if fi is not None:
                    fi.close()
        return None


class EmailHandler:
    @classmethod
    def __regex_match(cls, text, reg_list):
        try:
            import re
            for reg in reg_list:
                result = re.search(reg, text)
                if result is not None:
                    return True, result.group(1)
        except:
            print(traceback.print_exc())
        return False, ""

    @classmethod
    def __encode_email_header(cls, mail, header):
        try:
            decode_header = email.header.decode_header(mail.get(header))
            if decode_header[0][1] is None:
                return decode_header[0][0]
            else:
                return decode_header[0][0].decode(decode_header[0][1])
        except:
            print(traceback.print_exc())
            return None

    @classmethod
    def __get_imap_setting(cls, email: str):
        hotmail_imap_setting = {"host": "outlook.office365.com", "port": 993}
        yahoo_imap_setting = {"host": "imap.mail.yahoo.com", "port": 993}
        domain = email.split("@")[1]
        if domain == "hotmail.com":
            return hotmail_imap_setting
        elif domain == "yahoo.com":
            return yahoo_imap_setting
        else:
            return {"host": "new.showcloud.top", "port": 993}

    @classmethod
    def __imap_login(cls, username: str, password: str):
        try:
            settings = cls.__get_imap_setting(username)
            imap = imaplib.IMAP4_SSL(host=settings["host"], port=settings["port"])
            imap.login(username, password)
            return imap, ""
        except Exception as ex:
            print(traceback.print_exc())
            return None, ex

    @classmethod
    def __imap_get_mail(cls, imap, email_from, email_subject, reg_list):
        try:
            imap.select("INBOX")
            flag, data = imap.search(None, 'FROM \"{0}\"'.format(email_from))
            mails = data[0].split()
            total_count = len(mails)
            rtn = False
            result = None
            print("Total Email:{0}".format(total_count))
            for i in range(0, total_count):
                try:
                    flag, data = imap.fetch(mails[total_count - 1 - i], '(RFC822)')
                    mail = email.message_from_string(data[0][1].decode('utf-8'))
                    print("From:{0} To:{1} Subject:{2}".format(cls.__encode_email_header(mail, 'from'),
                                                               cls.__encode_email_header(mail, 'to'),
                                                               cls.__encode_email_header(mail, 'subject')))

                    if (cls.__encode_email_header(mail, 'from').find(email_from) >= 0 and
                            cls.__encode_email_header(mail, 'subject').find(email_subject) >= 0):
                        if mail.is_multipart():
                            if len(reg_list) == 0:
                                import re
                                from bs4 import BeautifulSoup
                                try:
                                    enclosure = mail.get_payload(1)
                                    link = str(enclosure).replace("3D", "")
                                    soup = BeautifulSoup(link, 'html.parser')
                                    # html = soup.find_all('a')[3]
                                    html = soup.find_all('span')[3]
                                    return True, re.search('(\d{8}|\d{6})', str(html.text)).group(1)
                                    # return True, html['href'].replace("\n","")
                                except:
                                    print(traceback.print_exc())
                                    return False, "不存在匹配邮件"
                            else:
                                for part in mail.get_payload():
                                    rtn, result = cls.__regex_match(part.get_payload(decode=True).decode('utf-8'), reg_list)
                                    if rtn:
                                        break
                        else:
                            rtn, result = cls.__regex_match(mail.get_payload(decode=True).decode('utf-8'), reg_list)

                    imap.store(mails[total_count - 1 - i], "+FLAGS", '\\Deleted')
                    if rtn:
                        print("Match:#{0}".format(result))
                        imap.expunge()
                        return rtn, result
                except:
                    print(traceback.print_exc())
            imap.expunge()
            return False, "不存在匹配邮件"
        except Exception as ex:
            print(traceback.print_exc())
            return False, ex

    @classmethod
    def __imap_logout(cls, imap):
        try:
            if imap is not None:
                imap.close()
                imap.logout()
        except:
            print(traceback.print_exc())

    @classmethod
    def get_mail_imap(cls, username, password, is_check, email_form='', email_subject='', reg_list=[]):
        imap = None
        try:
            imap, reason = cls.__imap_login(username, password)
            if imap is None:
                return False, reason
            if is_check:
                return True, ""
            rtn, reason = False, ""
            tryTime = 0
            while not rtn and tryTime < 3:
                tryTime += 1
                print("Try {0} time(s)".format(tryTime))
                rtn, reason = cls.__imap_get_mail(imap, email_form, email_subject, reg_list)
                if not rtn and tryTime < 3:
                    time.sleep(30)
            return rtn, reason
        except Exception as ex:
            print(traceback.print_exc())
            return False, ex
        finally:
            cls.__imap_logout(imap)

if __name__ == "__main__":
    is_check = False
    email_form = "security@facebookmail.com"   # 获取验证码
    username = "xxxx@hotmail.com"
    password = "xxxxxxx"
    # email_form = "notification@facebookmail.com"   # 获取验证地址
    # email_subject = "is your Facebook account recovery code"   # 获取验证码
    email_subject = ""   # 获取验证码
    # email_subject = "Confirm your business email address"   # 获取验证地址
    reg_list = ["Your security code is: (\\d{8}).", "您的安全代码是：(\\d{8}) 。", "あなたのセキュリティ コードは次のとおりです。(\\d{8}) 。"]   # 获取验证码
    # reg_list = []   # 获取验证地址
    code = EmailHandler.get_mail_imap(username, password, is_check, email_form, email_subject, reg_list)
    print(code)
