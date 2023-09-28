# Resources
This page contains some resources that may help developers maintaining this code.  

## Gradio for the User Interface
We are using Gradio for the UI.  If you wish to change UI elements, the Gradio documentation will be helpful.  
+ [Gradio website](https://www.gradio.app/)
+ [Gradio documentation](https://www.gradio.app/docs/blocks)

This guide was helpful for deploying a Gradio app into Azure: https://datasciencedojo.com/blog/web_app_for_gradio/.  But, there were a few additional tweaks beyond this article that were needed to deploy successfully, so please follow the steps documented in the [README](README.md).  

There is a [known bug](https://github.com/jennifermarsman/AIforChildhoodHunger/issues/26) to continue the questionnaire in the same language as the previous tab.  Some resources that might help to fix this problem are:
+ https://github.com/gradio-app/gradio/issues/2412 (and the other links on this page)
+ https://www.gradio.app/docs/tab 

## Prompt Engineering
Langchain debugging: https://python.langchain.com/docs/guides/debugging
