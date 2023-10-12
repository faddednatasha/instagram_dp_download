from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup as bs
import random
import os.path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('insta_index.html')

@app.route('/download', methods=['GET'])
def download_profile_pic():
    username = request.args.get('username')

    insta_url = 'https://www.instagram.com'
    response = requests.get(f"{insta_url}/{username}/")  # Fixed typo: `inta_username` -> `username`
    
    if response.ok:
        html = response.text
        bs_html = bs(html, features="lxml")
        bs_html = bs_html.text
        index = bs_html.find('profile_pic_url_hd') + 21
        remaining_text = bs_html[index:]
        remaining_text_index = remaining_text.find('requested_by_viewer') - 3
        string_url = remaining_text[:remaining_text_index].replace("\\u0026", "&")

        while True:
            filename = 'pic' + str(random.randint(1, 100000)) + '.jpg'
            file_exists = os.path.isfile(filename)

            if not file_exists:
                with open(filename, 'wb+') as handle:
                    response = requests.get(string_url, stream=True)
                    if not response.ok:
                        print(response)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
            else:
                continue
            break
        print("\n downloading completed ..............")

        # Assuming the profile pictures are hosted at URLs like this:
        profile_pic_url = f'https://example.com/{username}/profile_pic.jpg'

        try:
            response = requests.get(profile_pic_url)
            response.raise_for_status()  # Check if the request was successful
            return send_file(
                response.content,
                mimetype='image/jpg',
                as_attachment=True,
                attachment_filename=f'{username}_profile_pic.jpg'
            )
        except requests.exceptions.HTTPError as errh:
            return f"HTTP Error: {errh}"
        except requests.exceptions.RequestException as err:
            return f"Error: {err}"

if __name__ == '__main__':
    app.run(debug=True)
