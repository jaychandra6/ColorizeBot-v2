import praw
import config
import time
import requests
import json
import prawcore

try:
    print("* Logging into Reddit Account")
    reddit = praw.Reddit(client_id=config.client_id,
                         client_secret=config.client_secret,
                         password=config.password,
                         user_agent='ColorizeBot-v2 by /u/_jaypatel',
                         username=config.username)
    print("* Login successful")

except:
    print("Login Failed")

def colorize(imgUrl):
    try:
        r = requests.post("https://api.deepai.org/api/colorizer",
                          data={
                          'image': imgUrl,
                          },
                          headers={
                          'api-key': '0ea33250-d4e6-47ca-a342-f91b5ad373b3'
                          }
                          )

        content=json.loads(r.content)
        print(content)
        if content["output_url"] is None:
            pass
        else:
            return content["output_url"]
    except Exception as e:
        print("Something went wrong")
        print(e)

cache=["fsz42z9","ft27f8f","ft2apj0"]

def main():
    try:
        for mention in reddit.inbox.stream():
            commentId=mention.id
            author=str(mention.author)
            print(commentId)
            submissionId=reddit.comment(commentId).submission.id
            submissionUrl=reddit.submission(submissionId).url
            print(submissionUrl)
            time.sleep(2)
            if ".jpg" or ".png" in submissionUrl and submissionUrl not in cache:
                colorizedImgUrl = colorize(submissionUrl)
                time.sleep(3)
                print("replying to author")
                imgUrlStr = "[click here to get the image]({s})".format(s=colorizedImgUrl)
                msg="Here is the colorized image.\n\n" + imgUrlStr + "\n\n[^wanna ^know ^how ^i ^made ^this? ^click ^here!](https://www.youtube.com/channel/UCgyk3P2xuDT3aT4oJ8t0XSg)" + "\n\n^^^I'm ^^^a ^^^bot. ^^^pm ^^^me ^^^and ^^^a ^^^human ^^^will ^^^reply."
                mention.reply(msg)
                print("reply successful")
                cache.append(submissionUrl)
                time.sleep(60)
            else:
                print("Invalid Image")

            if len(cache) > 10:
                for i in range(9):
                    cache.pop()


    except prawcore.exceptions.ServerError as e:
        print("something went wrong!")
        print(e)
        time.sleep(60)

    except praw.exceptions.ClientException as e:
        print("Client error occured")
        print(e)
        time.sleep(10)

    except praw.exceptions.APIException as e:
        print("API error occured")
        print(e)
        time.sleep(60)

    except praw.exceptions.PRAWException as e:
        print("PRAW error occured")
        print(e)
        time.sleep(20)

    except prawcore.exceptions.RequestException as e:
        print("RequestException occured")
        print(e)
        time.sleep(20)

if __name__ == "__main__":
    main()
