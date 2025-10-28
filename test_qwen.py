import dashscope
dashscope.api_key = 'sk-ef9da958302f488b946da484bb824de3'

from dashscope import Generation
response = Generation.call(
    model="qwen-max",
    prompt="Hello, what is 2+2?"
)
print(response)