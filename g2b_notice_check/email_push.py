import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os 
from g2b_notice_check.g2b_notice import g2b_notice_collection
from g2b_notice_check.g2b_preparation import g2b_preparation_collection

def html_write(html_content, ai_list, check_list, notice_type, notice_type_eng):
    html_content += "<h3>{}: AI관련 공고 {}건, 확인이 필요한 공고 {}건이 올라왔습니다.</h3>".format(notice_type, len(ai_list), len(check_list))

    if len(ai_list) > 0:
        html_content += "<h4>AI관련 공고 {}건</h4>".format(len(ai_list))
        html_content += """
        <table border='1' style='border-collapse: collapse; width: 100%; margin-bottom: 20px;'>
            <tr>
                <th style='padding: 10px; width: 30%; text-align: center;'>공고명</th>
                <th style='padding: 10px; width: 30%; text-align: center;'>공고 기간</th>
                <th style='padding: 10px; width: 15%; text-align: center;'>공고 기관</th>
                <th style='padding: 10px; width: 15%; text-align: center;'>수요 기관</th>
                <th style='padding: 10px; width: 10%; text-align: center;'>링크</th>
            </tr>
        """
        for i in ai_list:
            html_content += "<tr>"
            html_content += "<td style='padding: 10px; width: 30%; text-align: center;'>{}</td>".format(i['{}_title'.format(notice_type_eng)])
            html_content += "<td style='padding: 10px; width: 30%; text-align: center;'>{} - {}</td>".format(i['{}_start_date'.format(notice_type_eng)], i['{}_end_date'.format(notice_type_eng)])
            html_content += "<td style='padding: 10px; width: 15%; text-align: center;'>{}</td>".format(i['publishing_agency'])
            html_content += "<td style='padding: 10px; width: 15%; text-align: center;'>{}</td>".format(i['requesting_agency'])
            html_content += "<td style='padding: 10px; width: 10%; text-align: center;'><a href='{}'>바로가기</a></td>".format(i['{}_link'.format(notice_type_eng)])
            html_content += "</tr>"
        html_content += "</table>"

    if len(check_list) > 0:
        html_content += "<h4>확인이 필요한 공고 {}건</h4>".format(len(check_list))
        html_content += """
        <table border='1' style='border-collapse: collapse; width: 100%; margin-bottom: 20px;'>
            <tr>
                <th style='padding: 10px; width: 30%; text-align: center;'>공고명</th>
                <th style='padding: 10px; width: 30%; text-align: center;'>공고 기간</th>
                <th style='padding: 10px; width: 15%; text-align: center;'>공고 기관</th>
                <th style='padding: 10px; width: 15%; text-align: center;'>수요 기관</th>
                <th style='padding: 10px; width: 10%; text-align: center;'>링크</th>
            </tr>
        """
        for i in check_list:
            html_content += "<tr>"
            html_content += "<td style='padding: 10px; width: 30%; text-align: center;'>{}</td>".format(i['{}_title'.format(notice_type_eng)])
            html_content += "<td style='padding: 10px; width: 30%; text-align: center;'>{} - {}</td>".format(i['{}_start_date'.format(notice_type_eng)], i['{}_end_date'.format(notice_type_eng)])
            html_content += "<td style='padding: 10px; width: 15%; text-align: center;'>{}</td>".format(i['publishing_agency'])
            html_content += "<td style='padding: 10px; width: 15%; text-align: center;'>{}</td>".format(i['requesting_agency'])
            html_content += "<td style='padding: 10px; width: 10%; text-align: center;'><a href='{}'>바로가기</a></td>".format(i['{}_link'.format(notice_type_eng)])
            html_content += "</tr>"
        html_content += "</table>"
    html_content += "<hr style='border: 1px solid black; margin: 20px 0;'>"
    return html_content

def email_sending():
    print('나라장터 공고를 찾습니다.')
    ai_notice_list, check_notice_list = g2b_notice_collection()
    ai_preparation_list, check_preparation_list = g2b_preparation_collection()
    gmail_user = 'jh.belab@gmail.com'
    gmail_password = os.getenv("gmail_password")
    print('이메일을 보내겠습니다.')

    sender_email = 'jh.belab@gmail.com'
    receiver_email_list = ['jh.noh@belab.co.kr']
    # receiver_email = 'jh.noh@belab.co.kr'
    subject = '나라장터에 새로운 ISP 공고가 올라왔습니다.'
    if len(ai_notice_list) > 0 or len(check_notice_list) > 0 or len(ai_preparation_list) > 0 or len(check_preparation_list) > 0:
        html_content = '<h2>나라장터에 새로 올라온 ISP공고가 있습니다. 확인 부탁드립니다.</h2>'
        if len(ai_notice_list) > 0 or len(check_notice_list) > 0:
            html_content = html_write(html_content, ai_notice_list, check_notice_list, '입찰 공고', 'notice')
            
        if len(ai_preparation_list) > 0 or len(check_preparation_list) > 0:
            html_content = html_write(html_content, ai_preparation_list, check_preparation_list, '사전 규격', 'preparation')

            for receiver_email in receiver_email_list:
                message = MIMEMultipart('alternative')
                message['Subject'] = subject
                message['From'] = sender_email
                message['To'] = receiver_email

                part1 = MIMEText(html_content, 'html')
                message.attach(part1)

                try:
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(gmail_user, gmail_password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                    server.quit()
                    print("메일이 성공적으로 발송되었습니다.")
                except Exception as e:
                    print(f"메일 발송 중 오류 발생: {e}")
    else:
        print('새로운 공고가 없습니다.')

# email_sending()
