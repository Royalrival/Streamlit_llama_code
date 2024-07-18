import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="🦙💬 Domain-Specific Llama 2 Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 Domain-Specific Llama 2 Chatbot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)

# Predefined context
context = """
The financial services industry (FSI) is in a time of transition from traditional on-premises data center installations to a cloud-based model. One of the drivers for this migration is that companies have seen increased efficiency and lower costs by adopting the cloud for their processing needs; the benefits of elastic infrastructure scalability are evident versus the traditional model of having capacity on hand to meet demanding periodic workloads. For many use cases, firms have realized reductions in real estate and power consumption by moving their services over to the cloud.

However, some workload migrations to the cloud are proving more challenging than others. For example, FIX and Swift, two services that are both widely used by financial institutions, have traditionally been a challenge to migrate to the cloud due to their on-prem appliance and connectivity requirements. In an effort to help customers solve this challenge, Bloomberg has recently made both FIX and Swift available natively in the cloud to customers on AWS.

Bloomberg and AWS PrivateLink
Bloomberg is a global leader in business and financial information, delivering trusted data, news, and insights that bring transparency, efficiency, and fairness to markets. The company helps connect influential communities across the global financial ecosystem via reliable technology solutions that enables customers to make more informed decisions and foster better collaboration. With the industry’s ongoing migration to the cloud, Bloomberg has been at the forefront of meeting customers wherever they are, becoming the first financial data provider to make real-time data accessible on the cloud with AWS in 2018, adding Data License content a few years later and most recently by making FIX and Swift connectivity available to customers on AWS.

Since financial service workloads can be demanding and require scalability, reliability, and resilience, Bloomberg has implemented a multi-availability zone and multi-region approach to their service offerings. More importantly, this connectivity from Bloomberg to their AWS customers is provided over AWS PrivateLink, which is a secure and scalable mechanism for connectivity that does so without ever leaving the AWS network.

A diagram showing how Bloomberg network is connected to AWS via AWS Direct Connect and then to customer VPCs via AWS PrivateLink
Figure 1 – Bloomberg Connectivity via AWS PrivateLink

FIX Connectivity via Bloomberg
FIX (Financial Information eXchange) is a free and open protocol for electronic trading that is widely used in capital markets across asset classes and different stages of the trade lifecycle. FIX is used from order placement to post-trade processing and monitoring, and even for reporting trade activity to regulators. FIX communication has historically taken place primarily over physical networks, which required customers to maintain dedicated infrastructure in their datacenters. Many of the reasons for this are less relevant in 2024 as network security and cloud capabilities have advanced significantly.

Bloomberg pioneered supporting secure FIX connectivity over the Internet, freeing customers from some of these legacy burdens. As customers now move more electronic trading workloads to the AWS cloud, Bloomberg is ready to meet these customers there.

With Bloomberg’s release of FIX protocol services on AWS, customers are now able to connect their cloud-hosted electronic trading applications directly to the Bloomberg FIX network. This service is available as an AWS PrivateLink endpoint in the customer’s own VPC and provides the industry leading level of service customers have come to expect from Bloomberg’s cloud offerings.

Bloomberg’s SWIFT Service Bureau
In addition to its FIX offering, Bloomberg also addressed the need for another critical offering by providing connectivity to the Swift network for mutual clients of Bloomberg and AWS. Bloomberg’s SWIFT Service Bureau provides users with access to 11,500 institutions on the SWIFT network. This managed connectivity service provides customers with a cost-effective, scalable infrastructure, monitoring tools, access to SWIFT expertise, and Global service teams. Similar to the FIX connectivity solution, the Bloomberg Swift Service Bureau allows users to focus on their own operations while Bloomberg hosts, manages, and supports users’ connectivity to the Swift network.

Diagram showing how customer applications connect via Bloomberg to SWIFT
Figure 2- SWIFT Connectivity Overview

 

In comparison to FIX, Swift can be more challenging to integrate. Establishing and maintaining infrastructure to the Swift network can be costly, require specialist personnel, and thus need ongoing investment. Additionally, Swift requires specialized software that provides firms the ability to connect with the network. Having a trusted and reliable partner providing connectivity to the Swift network helps alleviate those overheads, as connectivity to the Swift network can be crucial for an institution’s day to day activity.

Included in the service is Bloomberg’s Enterprise Console which provides a web-based platform for monitoring, alerting and approving of Swift message workflows. Privileged users can step into Swift message workflows to view the latest status of messages as well as action a number of other message related features.

Two screenshots of the Bloomberg Enterprise Console showing SWIFT related information
Figure 3 – Bloomberg Enterprise Console

Bloomberg has helped hundreds of institutions connect to the Swift network over the last two decades, enabling them to benefit from:

Reduced Infrastructure Costs — Bloomberg helps manage the technology lift with a fully-hosted solution, enabling firms to minimize the cost of Swift infrastructure, along with yearly upgrades required to connect to Swift.
Scalability and Readiness – As businesses grow and markets change, Bloomberg helps customers be future ready, for events such as T+1 shortened settlement cycles.
Industry Leading Support – Open service requests directly from Bloomberg’s Enterprise Console and benefit from 24/7 global assistance.
Rapid Onboarding – Swift implementation experts help customers get live quickly.
Custom Integrations – Bloomberg’s managed integration services support custom integrations from internal and third party systems into the Swift Service Bureau. A number of workflows, connectivity types, and message types can be supported by Bloomberg’s integration platform – such as MT to MX message conversion.
Conclusion
FIX and Swift connectivity have traditionally required on-prem appliances or solutions which introduce challenges for companies looking to migrate some of their workloads to the cloud. With the service offerings provided by Bloomberg to AWS customers on the cloud, those roadblocks are removed and the cloud journey can continue.
"""

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'. Use the following context to answer questions:\n\n" + context + "\n\n"
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)