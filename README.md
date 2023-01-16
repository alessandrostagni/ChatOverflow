# ChatOverflow
ChatGPT driven technical support search engine.

## Use the search engine

Go to [chatoverflow.io](https://chatoverflow.io)

## Extract and index your own conversations
If you want to contribute to our ChatOverflow, you can upload your chats with ChatGPT, which needs to be EXCLUSIVELY about coding.
Follow this steps:
1) Install [Save ChatGPT](https://chrome.google.com/webstore/detail/save-chatgpt/iccmddoieihalmghkeocgmlpilhgnnfn) extension on your Google Chrome browser.
<br/>
2) From Chrome click on the "Extension" button at the top right corner of the browser. Then "Save ChatGPT".
<br/>
3) Save the file locally in ".txt" format.
<br/>
4) Go to [search engine website](https://chatoverflow.io) and click on "Upload your conversation".
<br/>
5) You will need a password to access the upload page: Contact us at ![name](./img/email.png).
<br/>
6) Upload your file. The format must be ".txt" and needs to be in the same output format of the extension.

## How to deploy

Clone the code on your machine.
Make sure you have a compatible version of Python and Pip compatible with the requirements for each lambda.
Run the `deploy.sh` script against the AWS account you want to deploy the stack in.


## Roadmap
- [ ]Terraform state remotely stored
- [x]Deployment instructions
- [x]Chunk driven Indexing
- [x]Capability of seeing full conversation
- [x]Better Testing UI
- [x]Deploy search website online
- [x]Show partial conversation text. Link to full conversation.
- [ ]User login and metadata on user who uploads.
