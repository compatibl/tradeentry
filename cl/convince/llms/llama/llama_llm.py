# Copyright (C) 2023-present The Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC
from dataclasses import dataclass
from cl.convince.llms.llm import Llm


@dataclass(slots=True, kw_only=True)
class LlamaLlm(Llm, ABC):
    """Abstract base to cloud provider implementations of the LLAMA API, includes settings shared by all providers."""

    @classmethod
    def create_prompt_from_messages_v2(cls, messages: list[dict]) -> str:
        """
        Transforms list of messages in the following format:
        [
            {"role": "system", "content": "System Prompt"},
            {"role": "user", "content": "What is 2 + 2?"},
            {"role": "assistant", "content": "2+2 is equals to 4"},
            {"role": "user", "content": "Answer only with resulting number"},
        ]
        Into format supported by llama2:
        <s><<SYS>>System Prompt<</SYS>>
        [INST]What is 2 + 2?[/INST]
        2+2 is equals to 4
        </s>
        <s>[INST]Answer only with resulting number[/INST]</s>
        """
        system_prompt = None
        user_messages = []
        assistant_messages = []
        for message in messages:
            if message.role == "system":
                system_prompt = message.content
            elif message.role == "user":
                user_messages.append(message.content)
            elif message.role == "assistant":
                assistant_messages.append(message.content)

        if len(assistant_messages) < len(user_messages):
            assistant_messages.append("")
        message_pairs = list(zip(user_messages, assistant_messages))
        if system_prompt is not None:
            pair = message_pairs[0]
            message_pairs[0] = (f"<<SYS>>\n{system_prompt}<</SYS>>\n\n" + pair[0], pair[1])
        message_pairs = [f"[INST] {pair[0]}[/INST]" + pair[1] for pair in message_pairs]
        prompt = "<s>" + "</s>\n<s>".join(message_pairs)
        return prompt

    @classmethod
    def create_prompt_from_messages(cls, messages: list[dict]) -> str:
        """
        Transforms list of messages in the following format:
        [
            {"role": "system", "content": "System Prompt"},
            {"role": "user", "content": "What is 2 + 2?"},
            {"role": "assistant", "content": "2+2 is equals to 4"},
            {"role": "user", "content": "Answer only with resulting number"},
        ]
        Into format supported by llama3:
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>

        You are a helpful AI assistant<|eot_id|>
        <|start_header_id|>user<|end_header_id|>

        What is 2 + 2?<|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>

        2+2 is equals to 4<|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        Answer only with resulting number<|eot_id|>
        """
        system_prompt = None
        user_messages = []
        assistant_messages = []
        for message in messages:
            if message.role == "system":
                system_prompt = message.content
            elif message.role == "user":
                user_messages.append(message.content)
            elif message.role == "assistant":
                assistant_messages.append(message.content)

        if len(assistant_messages) < len(user_messages):
            assistant_messages.append("")
        prompt = "<|begin_of_text|>"
        if system_prompt is not None:
            prompt += f"<|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|>\n"
        for user, assistant in zip(user_messages, assistant_messages):
            prompt += f"<|start_header_id|>user<|end_header_id|>\n\n{user}<|eot_id|>\n"
            prompt += f"<|start_header_id|>assistant<|end_header_id|>"
            if assistant != "":
                prompt += f"\n\n{assistant}<|eot_id|>\n"
        return prompt
