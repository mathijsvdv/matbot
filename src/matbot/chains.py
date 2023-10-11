from typing import Any, Dict, List, Optional

import aiohttp
import requests
from langchain.callbacks.manager import AsyncCallbackManagerForChainRun, CallbackManagerForChainRun
from langchain.chains.base import Chain
from pydantic import Extra


class APICallingChain(Chain):
    """
    Chain that calls an API to answer a question.
    """

    api_url: str
    """URL to make the API calls to"""
    input_key: str = "content"
    output_key: str = "result"

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Will be whatever keys the prompt expects.

        :meta private:
        """
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Will always return text key.

        :meta private:
        """
        return [self.output_key]

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        response = requests.post(self.api_url, json=inputs, timeout=10)
        response_json = response.json()

        # If you want to log something about this run, you can do so by calling
        # methods on the `run_manager`, as shown below. This will trigger any
        # callbacks that are registered for that event.
        if run_manager:
            run_manager.on_text("Log something about this run")

        return {self.output_key: response_json["result"]}

    async def _acall(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=inputs, timeout=10) as response:
                response_json = await response.json()

        # If you want to log something about this run, you can do so by calling
        # methods on the `run_manager`, as shown below. This will trigger any
        # callbacks that are registered for that event.
        if run_manager:
            await run_manager.on_text("Log something about this run")

        return {self.output_key: response_json["result"]}

    @property
    def _chain_type(self) -> str:
        return "api_calling_chain"
