#!/usr/bin/env python3
import requests
import time
'''
Quora-Formkey: This is obtained by logging in to Quora.com, viewing the page source, and finding the "formkey" dictionary key (Normally line 14). Use its value in the Quora-Formkey field.
Cookie: 'm-b=xxxx' - This is the value of the cookie with the key m-b, which is present in the list of cookies used on Quora.com (not poe.com), you can simply inspect cookies in Chrome (F12-Application-cookie) to get it.
'''
class poe:
    def __init__(self, formkey, cookie, bot="capybara") -> None:
        self.bot = bot
        self.url = "https://www.quora.com/poe_api/gql_POST"
        self.headers = {
            "Host": "www.quora.com",
            "Accept": "*/*",
            "apollographql-client-version": "1.1.6-65",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Poe 1.1.6 rv:65 env:prod (iPhone14,2; iOS 16.2; en_US)",
            "apollographql-client-name": "com.quora.app.Experts-apollo-ios",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Quora-Formkey":formkey,
            "Cookie":cookie,
        }
        _data = {
            "operationName": "ChatViewQuery",
            "query": "query ChatViewQuery($bot: String!) {\n  chatOfBot(bot: $bot) {\n    __typename\n    ...ChatFragment\n  }\n}\nfragment ChatFragment on Chat {\n  __typename\n  id\n  chatId\n  defaultBotNickname\n  shouldShowDisclaimer\n}",
            "variables": {"bot": self.bot},
        }
        _response = requests.post(self.url, headers=self.headers, json=_data)
        self.chat_id = _response.json()["data"]["chatOfBot"]["chatId"]

    def clear_context(self):
        _data = {
            "operationName": "AddMessageBreakMutation",
            "query": "mutation AddMessageBreakMutation($chatId: BigInt!) {\n  messageBreakCreate(chatId: $chatId) {\n    __typename\n    message {\n      __typename\n      ...MessageFragment\n    }\n  }\n}\nfragment MessageFragment on Message {\n  id\n  __typename\n  messageId\n  text\n  linkifiedText\n  authorNickname\n  state\n  vote\n  voteReason\n  creationTime\n  suggestedReplies\n}",
            "variables": {"chatId": self.chat_id},
        }
        _ = requests.post(self.url, headers=self.headers, json=_data)

    def send_message(self, message):
        _data = {
            "operationName": "AddHumanMessageMutation",
            "query": "mutation AddHumanMessageMutation($chatId: BigInt!, $bot: String!, $query: String!, $source: MessageSource, $withChatBreak: Boolean! = false) {\n  messageCreate(\n    chatId: $chatId\n    bot: $bot\n    query: $query\n    source: $source\n    withChatBreak: $withChatBreak\n  ) {\n    __typename\n    message {\n      __typename\n      ...MessageFragment\n      chat {\n        __typename\n        id\n        shouldShowDisclaimer\n      }\n    }\n    chatBreak {\n      __typename\n      ...MessageFragment\n    }\n  }\n}\nfragment MessageFragment on Message {\n  id\n  __typename\n  messageId\n  text\n  linkifiedText\n  authorNickname\n  state\n  vote\n  voteReason\n  creationTime\n  suggestedReplies\n}",
            "variables": {
                "bot": self.bot,
                "chatId": self.chat_id,
                "query": message,
                "source": None,
                "withChatBreak": False,
            },
        }
        _ = requests.post(self.url, headers=self.headers, json=_data)

    def get_latest_message(self):
        _data = {
            "operationName": "ChatPaginationQuery",
            "query": "query ChatPaginationQuery($bot: String!, $before: String, $last: Int! = 10) {\n  chatOfBot(bot: $bot) {\n    id\n    __typename\n    messagesConnection(before: $before, last: $last) {\n      __typename\n      pageInfo {\n        __typename\n        hasPreviousPage\n      }\n      edges {\n        __typename\n        node {\n          __typename\n          ...MessageFragment\n        }\n      }\n    }\n  }\n}\nfragment MessageFragment on Message {\n  id\n  __typename\n  messageId\n  text\n  linkifiedText\n  authorNickname\n  state\n  vote\n  voteReason\n  creationTime\n}",
            "variables": {"before": None, "bot": self.bot, "last": 1},
        }
        _author_nickname = ""
        _state = "incomplete"
        while True:
            time.sleep(1)
            _response = requests.post(self.url, headers=self.headers, json=_data)
            _response_json = _response.json()
            _state = _response_json["data"]["chatOfBot"]["messagesConnection"]["edges"][
                -1
            ]["node"]["state"]
            _author_nickname = _response_json["data"]["chatOfBot"]["messagesConnection"][
                "edges"
            ][-1]["node"]["authorNickname"]
            if _author_nickname == self.bot and _state == "complete":
                _text = _response_json["data"]["chatOfBot"]["messagesConnection"][
                    "edges"
                ][-1]["node"]["text"]
                break
            else:
                print("Thinking...")
        return _text


if __name__ == "__main__":
    poe = poe("","m-b=",bot="capybara")
    while True:
        try:
            text = input(">说点什么：")
            if text == "clear":
                poe.clear_context()
            else:
                poe.send_message(text)
                print(poe.get_latest_message())
        except Exception as error:
            print(error)